from pathlib import Path
import time
import os
import shutil
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style


class MyHandler(FileSystemEventHandler):
    def __init__(self, source_folder, target_folder):
        self.source_folder = os.path.abspath(source_folder)
        self.target_folder = os.path.abspath(target_folder)
        self._initial_sync()

    def on_created(self, event):
        if event.is_directory:
            return
        self._copy_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._copy_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._delete_file(event.src_path)

    def _initial_sync(self):
        """Synchronize source folder to target folder when script starts."""
        print("Performing initial synchronization...")
        for root, _, files in os.walk(self.source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                self._copy_file(src_path)
        print(Fore.YELLOW + "Initial synchronization complete.")

    def _copy_file(self, src_path):
        """Copy file from source to target folder."""
        relative_path = os.path.relpath(src_path, self.source_folder)
        target_path = os.path.join(self.target_folder, relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(src_path, target_path)  # Copy file with metadata
        print(f"{Fore.GREEN}Copied:{Style.RESET_ALL} {src_path} -> {target_path}")

    def _delete_file(self, src_path):
        """Delete file from the target folder."""
        print(f"{Fore.RED}Deleted (not synced):{Style.RESET_ALL} {src_path}")
        return
        relative_path = os.path.relpath(src_path, self.source_folder)
        target_path = os.path.join(self.target_folder, relative_path)
        if os.path.exists(target_path):
            os.remove(target_path)
            print(f"Deleted: {target_path}")


def filesCloner(source, target):
    # Verify folders
    if not os.path.exists(source):
        print(f"Error: Source folder '{source}' does not exist.")
        return
    if not os.path.exists(target):
        print(f"Error: target folder '{source}' does not exist.")
        return

    # Convert paths to absolute if not already
    source = Path(source).resolve()
    target = Path(target).resolve()

    # Start the observer
    print(f"Watching folder: {source}")
    print(f"Duplicating files to: {target}")

    event_handler = MyHandler(source, target)
    observer = Observer()
    observer.schedule(event_handler, path=source, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped watching.")
    observer.join()


if __name__ == "__main__":
    # Fetches the current script name dynamically
    script_name = os.path.basename(__file__)
    # Parse command-line arguments or prompt the user for input
    parser = argparse.ArgumentParser(
        description="Watch a folder and duplicate changes to another folder.",
        usage=f"{script_name} --source <source_folder> --target <target_folder>",
    )

    parser.add_argument("--source", type=str, help="Source folder to watch")
    parser.add_argument("--target", type=str, help="Target folder to copy files to")
    args = parser.parse_args()

    if args.source and args.target:
        filesCloner(args.source, args.target)
    else:
        print(f"usage: {script_name} --source <source_folder> --target <target_folder>")
