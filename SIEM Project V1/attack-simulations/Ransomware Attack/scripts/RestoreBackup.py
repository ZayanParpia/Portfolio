<<<<<<< HEAD
import shutil
import tempfile
from pathlib import Path

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
=======
import os
import shutil
from pathlib import Path

import gdown
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa


# ============================================================
# CONFIGURATION
# ============================================================

<<<<<<< HEAD
# The ID of the shared folder (from the URL:
# https://drive.google.com/drive/folders/<THIS_PART>?usp=sharing)
DRIVE_FOLDER_ID = "1W0Ti8DK2-kFQid1BPrjDky_9ho7GVl5f"

LOCAL_FOLDER = Path(
    r"/home/endpoint4/Documents"
)

# Path to the OAuth client secrets file you download from
# Google Cloud Console (APIs & Services -> Credentials ->
# OAuth client ID -> Desktop app -> Download JSON).
# Resolved relative to this script's own folder, so it works
# no matter what directory you launch the script from.
SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = str(SCRIPT_DIR / "client_secret_92787663520-e5gm4tp5e298mdp8vfdr85rnjqpvehjd.apps.googleusercontent.com.json")

# Where PyDrive2 will cache your OAuth token after the first
# login, so you don't have to re-authenticate every run.
SAVED_CREDS_FILE = str(SCRIPT_DIR / "saved_credentials.json")


# ============================================================
# AUTH
# ============================================================

def authenticate():
    """
    Authenticate with the Google Drive API using OAuth.

    Because this uses YOUR account's credentials (not an
    anonymous/public request like gdown), it can access any
    file you own or have been shared, regardless of whether
    that file individually has "Anyone with the link" turned
    on. This is what fixes the permission errors gdown hit.
    """

    gauth = GoogleAuth()

    gauth.LoadClientConfigFile(CLIENT_SECRETS_FILE)
    gauth.LoadCredentialsFile(SAVED_CREDS_FILE)

    if gauth.credentials is None:
        # No local browser available on headless Ubuntu/CLI, so
        # print a URL to open elsewhere and paste back the code.
        gauth.CommandLineAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()

    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(SAVED_CREDS_FILE)

    return GoogleDrive(gauth)
=======
DRIVE_FOLDER_URL = (
    "https://drive.google.com/drive/folders/"
    "1W0Ti8DK2-kFQid1BPrjDky_9ho7GVl5f?usp=sharing"
)

LOCAL_FOLDER = Path(
    r"C:\Users\ikepa\OneDrive\Pictures\SIEM system"
    r"\\attack-simulations\\Ransomwhere Attack\\scripts"
)
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa


# ============================================================
# REMOVE OLD FILE/FOLDER
# ============================================================

def remove_existing(path):
    """
    Remove an existing file or folder.
    """

    if not path.exists():
        return

    if path.is_file() or path.is_symlink():
        path.unlink()
<<<<<<< HEAD

=======
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
    elif path.is_dir():
        shutil.rmtree(path)


# ============================================================
<<<<<<< HEAD
# RECURSIVELY DOWNLOAD A DRIVE FOLDER
# ============================================================

def download_folder_recursive(drive, folder_id, destination, stats, depth=0):
    """
    Recursively download every file and every subfolder (at any
    depth) under folder_id into destination, using authenticated
    API calls (no public-link permission required).

    stats is a dict used to accumulate counts of successes and
    failures across the whole recursive walk, so a bad file
    somewhere deep in the tree never stops the rest of the
    folder from downloading.
    """

    destination.mkdir(parents=True, exist_ok=True)

    indent = "  " * depth

    query = (
        f"'{folder_id}' in parents and trashed=false"
    )

    file_list = drive.ListFile({
        "q": query,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
        "corpora": "allDrives",
    }).GetList()

    if not file_list:
        print(f"{indent}(empty folder)")
        return

    # Process subfolders first, then files, purely for readable output.
    subfolders = [
        f for f in file_list
        if f["mimeType"] == "application/vnd.google-apps.folder"
    ]
    files = [f for f in file_list if f not in subfolders]

    for item in subfolders:
        item_name = item["title"]
        item_path = destination / item_name

        print(f"{indent}[dir] {item_name}/")
        download_folder_recursive(
            drive, item["id"], item_path, stats, depth + 1
        )

    for item in files:
        item_name = item["title"]
        item_path = destination / item_name

        print(f"{indent}Downloading: {item_name}")

        try:
            item.GetContentFile(str(item_path))
            print(f"{indent}  OK")
            stats["succeeded"].append(str(item_path))

        except Exception as error:
            print(f"{indent}  FAILED: {error}")
            stats["failed"].append((str(item_path), str(error)))


# ============================================================
# MAIN RESTORE FLOW
=======
# DOWNLOAD GOOGLE DRIVE FOLDER
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
# ============================================================

def download_drive_folder():

    print("=" * 60)
<<<<<<< HEAD
    print("Google Drive Restore (authenticated)")
    print("=" * 60)

    print("\nGoogle Drive folder ID:")
    print(DRIVE_FOLDER_ID)

    print("\nLocal destination:")
    print(LOCAL_FOLDER)

    print("\nAuthenticating...")
    drive = authenticate()

    LOCAL_FOLDER.mkdir(parents=True, exist_ok=True)

    temp_folder = Path(
        tempfile.mkdtemp(prefix="google_drive_restore_")
    )

    print("\nTemporary download location:")
    print(temp_folder)

    print("\nDownloading assets (recursing into every subfolder)...")
    print("-" * 60)

    stats = {"succeeded": [], "failed": []}

    try:
        download_folder_recursive(drive, DRIVE_FOLDER_ID, temp_folder, stats)

    except Exception as error:
=======
    print("Google Drive Restore")
    print("=" * 60)

    print(f"\nGoogle Drive folder:")
    print(DRIVE_FOLDER_URL)

    print(f"\nLocal destination:")
    print(LOCAL_FOLDER)

    LOCAL_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Temporary download location.
    temp_folder = LOCAL_FOLDER / "_google_drive_restore"

    # Start with a clean temporary folder.
    if temp_folder.exists():
        print("\nRemoving previous temporary download...")
        remove_existing(temp_folder)

    temp_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\nDownloading assets...")
    print("-" * 60)

    try:

        downloaded = gdown.download_folder(
            url=DRIVE_FOLDER_URL,
            output=str(temp_folder),
            quiet=False,
            use_cookies=False
        )

    except Exception as error:

>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
        print("\nDOWNLOAD FAILED")
        print("-" * 60)
        print(error)

<<<<<<< HEAD
        remove_existing(temp_folder)
        return False

    print("\n" + "-" * 60)
    print(f"Downloaded: {len(stats['succeeded'])}   Failed: {len(stats['failed'])}")

    if stats["failed"]:
        print("\nThe following items failed and were skipped:")
        for path, error in stats["failed"]:
            print(f"  - {path}: {error}")

    downloaded_items = list(temp_folder.iterdir())

    if not downloaded_items:
        print("\nDOWNLOAD FAILED")
        print("The temporary folder is empty.")

        remove_existing(temp_folder)
=======
        if temp_folder.exists():
            remove_existing(temp_folder)

>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
        return False

    print("\nDownload finished.")
    print("-" * 60)

    # ========================================================
<<<<<<< HEAD
    # RESTORE FILES
=======
    # FIND THE DOWNLOADED FOLDER
    # ========================================================

    downloaded_items = list(temp_folder.iterdir())

    if not downloaded_items:

        print("No files were downloaded.")

        remove_existing(temp_folder)

        return False

    # gdown normally creates the Drive folder inside output.
    # If there is exactly one directory, use it.
    if len(downloaded_items) == 1 and downloaded_items[0].is_dir():

        source_folder = downloaded_items[0]

    else:

        source_folder = temp_folder

    # ========================================================
    # REPLACE EXISTING FILES/FOLDERS
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
    # ========================================================

    print("\nRestoring files...")
    print("-" * 60)

<<<<<<< HEAD
    for source in temp_folder.iterdir():
=======
    for source in source_folder.iterdir():
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa

        destination = LOCAL_FOLDER / source.name

        print(f"\nRestoring: {source.name}")

<<<<<<< HEAD
        if destination.exists():
            print("  Replacing existing item...")
            remove_existing(destination)

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
=======
        # Remove existing item with the same name.
        if destination.exists():

            print("  Replacing existing item...")

            remove_existing(destination)

        # Copy folder.
        if source.is_dir():

            shutil.copytree(
                source,
                destination
            )

        # Copy file.
        else:

            shutil.copy2(
                source,
                destination
            )
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa

        print("  Restored successfully.")

    # ========================================================
    # CLEAN UP
    # ========================================================

    print("\nCleaning temporary files...")
<<<<<<< HEAD
=======

>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
    remove_existing(temp_folder)

    print("\n" + "=" * 60)
    print("RESTORE COMPLETE")
    print("=" * 60)

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    success = download_drive_folder()

    if success:
<<<<<<< HEAD
        print("\nAll Google Drive assets have been restored.")
    else:
=======

        print("\nAll Google Drive assets have been restored.")

    else:

>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
        print("\nRestore failed.")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()

>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa
