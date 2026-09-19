# Ransomware Detection & Automated Response — Project Outline

**Goal:** Simulate a ransomware attack in a controlled lab, detect it in Wazuh via
File Integrity Monitoring (FIM) + auditd process tracking, and trigger a SOAR
response that kills the offending process, deletes the executable, and restores
affected files from a snapshot backup.

**MITRE ATT&CK mapping:** T1486 — Data Encrypted for Impact (Impact tactic)

Supporting techniques referenced in the writeup:
- T1059 — Command and Scripting Interpreter (execution of the encryptor)
- T1489 — Service Stop (optional — relevant if security/backup services are stopped first)
- T1490 — Inhibit System Recovery (optional — relevant if shadow-copy/backup deletion is simulated before the defense stops it)

**Atomic Red Team tests referenced for validation** (grounds detections in a known framework, not just the custom script):
- T1486 — the available atomics are PowerShell/Windows-focused; for this Linux lab they're noted for technique alignment, since the simulator itself is custom-built and Linux-native
- T1490 — includes tests for deleting Volume Shadow Copies/backups, relevant if backup-tampering detection is added later

---

## Phase 1: Building the Attack (Days 1–3)

**The simulator.** A Fernet-based Python script (`cryptography` library) is the
core artifact of the attack side of the lab. It recursively encrypts files in
the target user's Documents and Pictures directories and drops a
`ransom_note.txt` in each affected folder. It's self-contained, with a matching
decrypt function built in so the environment can be reset between test runs
rather than rebuilt from scratch.

Two execution paths are in scope: running it locally on the victim host, and
pushing/executing it via a reverse shell from Kali, which gives the lab a more
realistic initial-access → execution chain rather than just a local script run.

**Snapshot backups.** A cron job (every 15–30 min) rsyncs the target folders to
a timestamped backup directory (`/backup/snapshots/<timestamp>/`). This is the
"previous version" the SOAR response later restores from.

---

## Phase 2: Detection (Days 4–7)

**FIM + auditd.** Wazuh `syscheck` provides real-time monitoring on the target
directories, catching mass file changes. An auditd watch rule on the same
paths (`-w /path -p wa -k ransomware_watch`) captures the `exe=` field (the
actual binary responsible) and PID. Wazuh's audit log collector needs to be
confirmed as ingesting these events.

**Correlation rule.** `local_rules.xml` defines a high-severity alert
condition: a burst of FIM modify/rename events against the same directory in
a short window (e.g. 20+ changes in 10 seconds), correlated with the matching
auditd event so the alert payload carries the offending process's `exe` path
and PID — the data the active response script will act on.

**End-to-end validation.** Once wired up, the detection path is validated by
triggering the simulator and confirming the correlation rule fires (rather
than just individual FIM events), the alert includes exe path and PID rather
than a generic "files changed," and the time from first encrypted file to
alert firing is captured as a metric for the writeup.

---

## Phase 3: Response (Days 8–11)

**Kill + delete + restore.** A Wazuh Active Response script, triggered by the
rule, is responsible for killing the PID, deleting or quarantining the
executable at the `exe` path from the alert, and rsyncing the most recent
clean snapshot back over the target folders. A copy of the simulator is kept
outside the target directory (e.g. in git), since the delete step will remove
it from the target path as part of correct behavior.

**SOAR notification.** A Wazuh webhook feeds Shuffle (or n8n), which sends a
Slack/email alert summarizing what was killed (PID, exe path), what was
deleted, and which snapshot was restored and when — with an optional
auto-created case/ticket for the "incident."

---

## Phase 4: Documentation (Days 12–14)

Portfolio documentation covers the MITRE ATT&CK mapping (T1486 plus supporting
techniques), a note on the Atomic Red Team tests referenced for validation, an
architecture diagram (attacker → victim → Wazuh → SOAR → notification),
before/after screenshots (encrypted files → process killed → files restored),
a short demo video/GIF of the full detect → respond → restore loop, and a
README with setup steps for reproducibility.

---

## Kali Linux Tools (delivery/execution simulation)

- **Netcat / Metasploit (`msfvenom`)** — used to establish a reverse shell to
  the victim for remote execution of the simulator, simulating a realistic
  execution-after-compromise chain
- **Atomic Red Team** — optional, for running standardized technique tests
  alongside the custom simulator to validate detections