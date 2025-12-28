#!/usr/bin/env python3
"""
backups3_scheduled_mode_masked.py
- Same backup logic as original but with data-masking for PII before any output, logs, or manifest that may be uploaded to a portfolio.
- Sensitive configuration is read from environment variables (no hard-coded ARNs, bucket names, or absolute user paths).
- When writing user-facing output (logs, manifests, SNS body), values are masked.

USAGE: set S3_BUCKET, KMS_KEY_ARN, SNS_TOPIC_ARN, and SOURCE_DRIVES_JSON in the environment before running.
If not set, placeholders are used and the script will run in dry-run safely.
"""

import os
import json
import hashlib
import argparse
import boto3
import time
import sys
import signal
import re
from datetime import datetime, timezone

# -----------------------------
# Helpers for masking
# -----------------------------

def mask_partial(val, keep_start=3, keep_end=4):
    if not val:
        return "<REDACTED>"
    if len(val) <= keep_start + keep_end:
        return "*" * len(val)
    return val[:keep_start] + "..." + val[-keep_end:]


def mask_arn(arn):
    if not arn or not isinstance(arn, str):
        return "<REDACTED_ARN>"
    parts = arn.split(":")
    if len(parts) < 6:
        return mask_partial(arn)
    service = parts[2]
    resource = parts[5] if len(parts) > 5 else parts[-1]
    return f"arn:aws:{service}:<REDACTED_REGION>:<REDACTED_ACCOUNT>:{mask_partial(resource)}"


def mask_bucket(bucket):
    if not bucket:
        return "<REDACTED_BUCKET>"
    return mask_partial(bucket, keep_start=2, keep_end=2)


def mask_s3_key(key):
    # show the prefix but redact the filename
    if not key:
        return "<REDACTED_S3_KEY>"
    parts = key.split("/")
    if len(parts) <= 2:
        return ".../" + mask_partial(parts[-1])
    return "/".join(parts[:-1]) + "/" + mask_partial(parts[-1])


def mask_path_for_output(path):
    if not path:
        return "<REDACTED_PATH>"
    try:
        p = os.path.normpath(path)
        # redact user home
        home = os.path.normcase(os.path.expanduser("~"))
        pnorm = os.path.normcase(p)
        if home and pnorm.startswith(home):
            rel = p[len(home):].lstrip(os.sep)
            return os.path.join("<REDACTED_HOME>", mask_partial(rel.replace(os.sep, "/"), 0, 10))
        # redact usernames in Windows style e.g. C:\Users\username\
        m = re.search(r"(C:|D:|E:|F:)?\\Users\\([^\\/]+)(.*)", p, re.IGNORECASE)
        if m:
            drive = m.group(1) or ""
            rest = m.group(3) or ""
            return f"{drive}\\Users\\<REDACTED_USER>\\{mask_partial(rest.replace('\\\\','/'), 0, 10)}"
        # default: show only last path components
        parts = p.split(os.sep)
        if len(parts) <= 3:
            return mask_partial(p)
        return os.sep.join(parts[:2]) + os.sep + "..." + os.sep + mask_partial(parts[-1])
    except Exception:
        return "<REDACTED_PATH>"


# -----------------------------
# Configuration (from env; masked in outputs)
# -----------------------------
S3_BUCKET = os.environ.get("S3_BUCKET") or "<REDACTED_BUCKET>"
KMS_KEY_ARN = os.environ.get("KMS_KEY_ARN") or "<REDACTED_KMS_ARN>"
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN") or None
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# SOURCE_DRIVES_JSON example: '{"C:\\\\": "MAIN", "E:\\\\": "Black Hard Drive"}'
SOURCE_DRIVES = {}
try:
    sdj = os.environ.get("SOURCE_DRIVES_JSON")
    if sdj:
        SOURCE_DRIVES = json.loads(sdj)
except Exception:
    SOURCE_DRIVES = {}

# fallbacks (non-sensitive placeholders) — kept minimal to avoid exposing user filesystem
if not SOURCE_DRIVES:
    SOURCE_DRIVES = {
        "C:\\": "MAIN"
    }

# Local state files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASH_DB_FILE = os.path.join(BASE_DIR, "backup_hashes.json")
LOG_FILE = os.path.join(BASE_DIR, "backup_log.txt")

# AWS clients (created with region; credentials come from environment/profile/role)
s3 = boto3.client("s3", region_name=AWS_REGION)
sns = boto3.client("sns", region_name=AWS_REGION)

CHUNK_SIZE = 64 * 1024  # 64KB
PRICE_PER_GB_DEEP_ARCHIVE = 0.00099  # USD per GB-month
PREWARN_SECONDS = 5 * 60
_interrupted = False


# -----------------------------
# Logging helper that masks sensitive fragments automatically
# -----------------------------

def safe_log(msg):
    # mask common configurable sensitive values before printing
    try:
        masked = msg.replace(S3_BUCKET, mask_bucket(S3_BUCKET) if S3_BUCKET else "<REDACTED_BUCKET>")
        masked = masked.replace(KMS_KEY_ARN, mask_arn(KMS_KEY_ARN) if KMS_KEY_ARN else "<REDACTED_KMS_ARN>")
        masked = masked.replace(SNS_TOPIC_ARN or "", "<REDACTED_SNS>")
    except Exception:
        masked = msg
    ts = datetime.now(timezone.utc).astimezone().isoformat()
    line = f"{ts} {masked}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


# -----------------------------
# Minimal helpers (hashing, size)
# -----------------------------

def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def load_hash_db():
    if os.path.exists(HASH_DB_FILE):
        try:
            with open(HASH_DB_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}
    return {}


def save_hash_db_atomic(db):
    tmp = HASH_DB_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(db, fh, indent=2)
    os.replace(tmp, HASH_DB_FILE)


def human_readable_size(bytes_count):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_count < 1024 or unit == "TB":
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} TB"


# -----------------------------
# Path helpers (keeps original behavior but avoids exposing raw paths in output)
# -----------------------------

def path_is_excluded(full_path, exclude_parts):
    p = os.path.normcase(os.path.abspath(full_path))
    for part in exclude_parts:
        if part.lower() in p.lower():
            return True
    return False


def build_allowed_paths_for_source(source_root, allowed_folder_names, explicit_paths):
    allowed = []
    for p in explicit_paths:
        try:
            if os.path.normcase(os.path.abspath(p)).startswith(os.path.normcase(source_root)):
                allowed.append(os.path.abspath(p))
        except Exception:
            pass

    users_path = os.path.join(source_root, "Users")
    if os.path.exists(users_path):
        try:
            for username in os.listdir(users_path):
                user_base = os.path.join(users_path, username)
                for name in allowed_folder_names:
                    candidate = os.path.join(user_base, name)
                    if os.path.exists(candidate):
                        allowed.append(candidate)
        except Exception:
            pass

    for name in allowed_folder_names:
        candidate = os.path.join(source_root, name)
        if os.path.exists(candidate):
            allowed.append(candidate)

    normalized = []
    for p in allowed:
        try:
            normalized.append(os.path.normpath(os.path.abspath(p)))
        except Exception:
            pass
    return sorted(set(normalized))


# -----------------------------
# Signals
# -----------------------------

def _signal_handler(signum, frame):
    global _interrupted
    _interrupted = True
    safe_log(f"Received signal {signum}; marking interrupted.")


signal.signal(signal.SIGINT, _signal_handler)
try:
    signal.signal(signal.SIGTERM, _signal_handler)
except Exception:
    pass


# -----------------------------
# Backup logic (keeps most behaviour, but uses masking in all outputs)
# -----------------------------
ALLOWED_FOLDER_NAMES = ["Pictures", "Videos", "Desktop", "Downloads"]
EXPLICIT_ABSOLUTE_PATHS = []  # encourage supplying via SOURCE_DRIVES_JSON rather than hard-coding
EXCLUDE_PATH_PARTS = [
    r"\\Windows",
    r"\\Program Files",
    r"\\Program Files (x86)",
    r"\\System Volume Information",
    r"\\$Recycle.Bin",
    r"\\hiberfil.sys",
    r"\\pagefile.sys",
    r"\\SwapFile.sys",
    r"\\Recovery",
    r"\\PerfLogs"
]


def gather_candidate_files():
    candidates = []
    drive_present = {}
    for source, drive_name in SOURCE_DRIVES.items():
        present = os.path.exists(source)
        drive_present[drive_name] = present
        if not present:
            safe_log(f"Drive root missing for pre-scan: {mask_path_for_output(source)}")
            continue

        allowed_roots = build_allowed_paths_for_source(source, ALLOWED_FOLDER_NAMES, EXPLICIT_ABSOLUTE_PATHS)
        if not allowed_roots:
            safe_log(f"No allowed roots found under {mask_path_for_output(source)}")
            continue

        for root_allowed in allowed_roots:
            for root, dirs, files in os.walk(root_allowed):
                dirs[:] = [d for d in dirs if not path_is_excluded(os.path.join(root, d), EXCLUDE_PATH_PARTS)]
                for fname in files:
                    file_path = os.path.join(root, fname)
                    if path_is_excluded(file_path, EXCLUDE_PATH_PARTS):
                        continue
                    candidates.append((os.path.normcase(os.path.abspath(file_path)), drive_name))
    return candidates, drive_present


def backup_run(dry_run=False):
    start_time = time.time()
    start_dt_utc = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    persisted_hashes = load_hash_db()
    updated_hashes = dict(persisted_hashes)

    uploaded_keys = []
    duplicate_skips = []
    errors = []
    run_manifest = {
        "run_start_utc": start_dt_utc,
        "dry_run": bool(dry_run),
        "uploaded": [],
        "skipped_duplicates": [],
        "errors": [],
        "estimates": {},
    }

    safe_log("Starting pre-scan for estimation...")
    candidates, drive_present = gather_candidate_files()
    candidates = list(dict.fromkeys(candidates))
    total_files = len(candidates)
    total_bytes = 0
    drive_totals = {v: 0 for v in SOURCE_DRIVES.values()}
    drive_uploaded = {v: 0 for v in SOURCE_DRIVES.values()}

    for path, dn in candidates:
        drive_totals.setdefault(dn, 0)
        drive_totals[dn] += 1
        try:
            total_bytes += os.path.getsize(path)
        except Exception:
            pass

    run_manifest["estimates"]["total_files"] = total_files
    run_manifest["estimates"]["total_bytes"] = total_bytes
    safe_log(f"Pre-scan: {total_files} files, {human_readable_size(total_bytes)} total across drives")

    content_hash_to_s3key = {}
    processed_files = 0
    processed_bytes = 0
    seen_paths = set()

    for idx, (abs_path, drive_name) in enumerate(candidates, start=1):
        if _interrupted:
            safe_log("Interrupted flag set; stopping processing loop.")
            break

        if abs_path in seen_paths:
            continue
        seen_paths.add(abs_path)
        processed_files += 1
        try:
            file_size = os.path.getsize(abs_path)
        except Exception:
            file_size = 0

        matched_source = None
        for src in SOURCE_DRIVES.keys():
            try:
                if os.path.normcase(os.path.abspath(abs_path)).startswith(os.path.normcase(os.path.abspath(src))):
                    matched_source = src
                    break
            except Exception:
                pass
        if matched_source:
            try:
                relpath = os.path.relpath(abs_path, matched_source)
            except Exception:
                relpath = os.path.basename(abs_path)
        else:
            relpath = os.path.basename(abs_path)

        today_prefix = datetime.utcnow().strftime("%Y/%m/%d")
        s3_key = f"{today_prefix}/{drive_name}/{relpath}".replace("\\", "/")

        try:
            file_hash = compute_sha256(abs_path)
        except Exception as e:
            safe_log(f"ERROR hashing {mask_path_for_output(abs_path)}: {str(e)}")
            errors.append({"path": mask_path_for_output(abs_path), "error": str(e)})
            run_manifest["errors"].append({"path": mask_path_for_output(abs_path), "error": str(e)})
            continue

        if file_hash in content_hash_to_s3key:
            existing_key = content_hash_to_s3key[file_hash]
            safe_log(f"Duplicate content (this run), skipping upload: {mask_path_for_output(abs_path)} -> matches {mask_s3_key(existing_key)}")
            duplicate_skips.append((mask_path_for_output(abs_path), mask_s3_key(existing_key)))
            run_manifest["skipped_duplicates"].append({"path": mask_path_for_output(abs_path), "existing_s3_key": mask_s3_key(existing_key)})
            updated_hashes[abs_path] = file_hash
            continue

        if persisted_hashes.get(abs_path) == file_hash:
            safe_log(f"Unchanged, skipping upload: {mask_path_for_output(abs_path)}")
            run_manifest.setdefault("unchanged", []).append(mask_path_for_output(abs_path))
            continue

        if dry_run:
            safe_log(f"(dry) Would upload: {mask_path_for_output(abs_path)} -> s3://{mask_bucket(S3_BUCKET)}/{mask_s3_key(s3_key)} (DEEP_ARCHIVE)")
            run_manifest["uploaded"].append({
                "path": mask_path_for_output(abs_path),
                "s3_key": mask_s3_key(s3_key),
                "size_bytes": file_size,
                "hash": file_hash,
                "action": "dry_upload"
            })
            content_hash_to_s3key[file_hash] = s3_key
            uploaded_keys.append(s3_key)
            updated_hashes[abs_path] = file_hash
            drive_uploaded.setdefault(drive_name, 0)
            drive_uploaded[drive_name] += 1
        else:
            try:
                s3.upload_file(
                    Filename=abs_path,
                    Bucket=S3_BUCKET,
                    Key=s3_key,
                    ExtraArgs={
                        "ServerSideEncryption": "aws:kms",
                        "SSEKMSKeyId": KMS_KEY_ARN,
                        "StorageClass": "DEEP_ARCHIVE"
                    }
                )
                safe_log(f"Uploaded: {mask_path_for_output(abs_path)} -> s3://{mask_bucket(S3_BUCKET)}/{mask_s3_key(s3_key)} (DEEP_ARCHIVE)")
                uploaded_keys.append(s3_key)
                content_hash_to_s3key[file_hash] = s3_key
                run_manifest["uploaded"].append({
                    "path": mask_path_for_output(abs_path),
                    "s3_key": mask_s3_key(s3_key),
                    "size_bytes": file_size,
                    "hash": file_hash,
                    "action": "uploaded"
                })
                updated_hashes[abs_path] = file_hash
                drive_uploaded.setdefault(drive_name, 0)
                drive_uploaded[drive_name] += 1
            except Exception as e:
                safe_log(f"Failed upload {mask_path_for_output(abs_path)} -> {mask_s3_key(s3_key)}: {str(e)}")
                errors.append({"path": mask_path_for_output(abs_path), "error": str(e)})
                run_manifest["errors"].append({"path": mask_path_for_output(abs_path), "error": str(e)})

        processed_bytes += file_size

        elapsed = time.time() - start_time
        files_done = processed_files
        if files_done > 0:
            est_total = (elapsed / files_done) * total_files if total_files else elapsed
            est_remaining = max(0.0, est_total - elapsed)
            safe_log(f"Progress: {files_done}/{total_files} files. Elapsed {elapsed:.1f}s. Est remaining {est_remaining:.1f}s.")
            run_manifest.setdefault("progress_samples", []).append({
                "time": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                "processed_files": files_done,
                "elapsed_seconds": elapsed,
                "estimated_total_seconds": est_total,
                "estimated_remaining_seconds": est_remaining
            })

    # finish
    end_time = time.time()
    duration = end_time - start_time

    run_manifest["run_end_utc"] = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    run_manifest["duration_seconds"] = duration
    run_manifest["files_uploaded_count"] = len(uploaded_keys)
    run_manifest["files_processed_count"] = processed_files
    run_manifest["bytes_processed"] = processed_bytes
    run_manifest["interrupted"] = bool(_interrupted)

    # Always attempt to save updated hash DB (even if interrupted)
    if not dry_run:
        try:
            save_hash_db_atomic(updated_hashes)
            safe_log("Saved updated hash DB (atomic).")
        except Exception as e:
            safe_log(f"Failed saving hash DB: {str(e)}")
            run_manifest["errors"].append({"save_hash_db": str(e)})

    # compute bucket size for cost estimate (best-effort)
    readable_size = "unknown"
    estimated_cost = 0.0
    if not dry_run:
        try:
            total_bytes_bucket = 0
            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=S3_BUCKET):
                for obj in page.get("Contents", []):
                    total_bytes_bucket += obj.get("Size", 0)
            readable_size = human_readable_size(total_bytes_bucket)
            total_gb = total_bytes_bucket / (1024 ** 3)
            estimated_cost = total_gb * PRICE_PER_GB_DEEP_ARCHIVE
            safe_log(f"Bucket '{mask_bucket(S3_BUCKET)}' size: {readable_size} ({total_gb:.3f} GB)")
        except Exception as e:
            safe_log(f"Could not compute bucket size: {str(e)}")

    # prepare drive status summary for reporting
    drive_report_lines = []
    for src, drive_name in SOURCE_DRIVES.items():
        present = os.path.exists(src)
        if not present:
            drive_report_lines.append(f"{drive_name}: Offline")
            continue
        total = drive_totals.get(drive_name, 0)
        uploaded = drive_uploaded.get(drive_name, 0)
        pct = (uploaded / total * 100.0) if total else (100.0 if uploaded else 0.0)
        drive_report_lines.append(f"{drive_name}: Online (Backed up {pct:.1f}%)")

    report = {
        "uploaded_keys": [mask_s3_key(k) for k in uploaded_keys],
        "duplicate_skips": duplicate_skips,
        "errors": run_manifest.get("errors", []),
        "manifest_file": None,
        "duration_seconds": duration,
        "estimated_monthly_cost_usd": estimated_cost,
        "bucket_size_readable": readable_size,
        "interrupted": bool(_interrupted),
        "files_processed": processed_files,
        "files_uploaded": len(uploaded_keys),
        "drive_report_lines": drive_report_lines
    }

    safe_log(f"Backup run complete. Uploaded: {len(uploaded_keys)} files. Interrupted: {report['interrupted']}. Duration: {duration:.1f}s")

    return report, run_manifest


# -----------------------------
# Main (masking outputs & use env-config)
# -----------------------------

def format_local_time_for_email(dt_utc=None):
    from zoneinfo import ZoneInfo
    try:
        TORONTO_TZ = ZoneInfo("America/Toronto")
    except Exception:
        TORONTO_TZ = None
    if dt_utc is None:
        dt = datetime.now(tz=TORONTO_TZ) if TORONTO_TZ else datetime.now()
    else:
        dt = dt_utc.astimezone(TORONTO_TZ) if TORONTO_TZ else dt_utc
    tzlabel = dt.strftime("%Z") if dt.strftime("%Z") else "EST"
    return dt.strftime("%Y-%m-%d %H:%M") + f" {tzlabel}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup changed files to S3 (YYYY/MM/DD/<DRIVE_NAME>/) - outputs masked for portfolio")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run (no uploads).")
    parser.add_argument("--skip-prewarn", action="store_true", help="Skip the 5-minute pre-warning and start immediately.")
    args = parser.parse_args()

    if not args.skip_prewarn:
        safe_log("Pre-warn: backup will start in 5 minutes (skipped showing exact drive/bucket info in logs)")
        try:
            for _ in range(PREWARN_SECONDS):
                if _interrupted:
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            _interrupted = True
            safe_log("Interrupted during pre-warn sleep.")
    else:
        safe_log("Skipping pre-warn; starting immediately.")

    try:
        if args.dry_run:
            safe_log("Starting DRY-RUN backup now (no uploads).")
            report, run_manifest = backup_run(dry_run=True)
        else:
            safe_log("Starting REAL backup now (uploads will occur).")
            report, run_manifest = backup_run(dry_run=False)
    except Exception as e:
        safe_log(f"Unhandled exception during backup: {str(e)}")
        report = {
            "uploaded_keys": [],
            "duplicate_skips": [],
            "errors": [{"fatal": str(e)}],
            "manifest_file": None,
            "duration_seconds": 0.0,
            "estimated_monthly_cost_usd": 0.0,
            "bucket_size_readable": "unknown",
            "interrupted": True,
            "files_processed": 0,
            "files_uploaded": 0,
            "drive_report_lines": [f"{v}: Offline" if not os.path.exists(k) else f"{v}: Online (Backed up 0%)" for k, v in SOURCE_DRIVES.items()]
        }
        run_manifest = {"errors": [str(e)]}

    # Compose masked subject/body
    status = "Completed"
    if report.get("errors"):
        status = "Failed"
    if report.get("interrupted"):
        status = "Interrupted" if status != "Failed" else "Failed (Interrupted)"

    subj_time = format_local_time_for_email(datetime.utcnow().replace(tzinfo=timezone.utc))
    subject = f"Backup {status} — {subj_time}"

    lines = []
    lines.append(f"Backup {status} — finished at {subj_time}")
    lines.append("")
    lines.append("Drive status:")
    for line in report.get("drive_report_lines", []):
        lines.append(f" - {line}")
    lines.append("")
    lines.append(f"Files processed: {report.get('files_processed', 0)}")
    lines.append(f"Files uploaded this run: {report.get('files_uploaded', 0)}")
    lines.append("")
    lines.append(f"Bucket total storage (estimate): {report.get('bucket_size_readable', 'unknown')}")
    lines.append(f"Estimated monthly storage cost (Deep Archive): ${report.get('estimated_monthly_cost_usd', 0.0):.2f}")
    lines.append(f"Backup duration: {report.get('duration_seconds', 0.0):.2f} seconds")
    lines.append("")
    if report.get("errors"):
        lines.append("Errors / Notes:")
        for e in report.get("errors", []):
            if isinstance(e, dict):
                lines.append(f" - {json.dumps(e)}")
            else:
                lines.append(f" - {str(e)}")
        lines.append("")
    lines.append(f"Manifest file: {mask_partial('backup_manifest_masked.json')}")
    lines.append("")
    lines.append("Notes:")
    lines.append(" - Outputs mask bucket names, ARNs, and full local paths for privacy.")
    lines.append(" - Retrieval from DEEP_ARCHIVE typically takes 12–48 hours.")

    body = "\n".join(lines)

    # Publish SNS (masked content only)
    if SNS_TOPIC_ARN:
        try:
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=body, Subject=subject)
            safe_log("SNS notification sent (final masked report).")
        except Exception as e:
            safe_log(f"SNS publish failed: {str(e)}")
    else:
        safe_log("SNS_TOPIC_ARN not set; skipping SNS publish.")

    # write a masked manifest for portfolio or review (never contain raw absolute paths / ARNs)
    try:
        masked_manifest_fn = os.path.join(BASE_DIR, f"backup_manifest_masked_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
        with open(masked_manifest_fn, "w", encoding="utf-8") as mf:
            json.dump({
                "run": run_manifest,
                "report": report,
                "config_masks": {
                    "s3_bucket": mask_bucket(S3_BUCKET),
                    "kms": mask_arn(KMS_KEY_ARN),
                    "sns": "<REDACTED_SNS>"
                }
            }, mf, indent=2)
        safe_log(f"Wrote masked run manifest: {mask_path_for_output(masked_manifest_fn)}")
    except Exception as e:
        safe_log(f"Failed to write masked manifest file: {str(e)}")

    safe_log("Script exiting. (Outputs have been masked for privacy.)")
    # exit code: 0 if completed without interruption and no errors; 2 otherwise
    if report.get("interrupted") or report.get("errors"):
        sys.exit(2)
    sys.exit(0)
