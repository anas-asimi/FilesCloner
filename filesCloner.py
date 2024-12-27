from pathlib import Path
import time
import os
import shutil
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style
import re


class MyHandler(FileSystemEventHandler):
    def __init__(self, source_folder, target_folder, recursive, filter_pattern):
        """
        Initialize the event handler.
        :param source_folder: Source directory to monitor.
        :param target_folder: Target directory for copying files.
        :param recursive: Boolean indicating if subdirectories should be monitored.
        :param filter_pattern: Compiled regex pattern for file filtering.
        """
        self.source_folder = os.path.abspath(source_folder)
        self.target_folder = os.path.abspath(target_folder)
        self.recursive = recursive
        self.filter_pattern = re.compile(filter_pattern) if filter_pattern else None
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
        """Synchronize all files from the source folder to the target folder at startup."""
        print("Performing initial synchronization...")
        for root, _, files in os.walk(self.source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                self._copy_file(src_path)
            if not self.recursive:
                break
        print(Fore.YELLOW + "Initial synchronization complete." + Style.RESET_ALL)

    def _copy_file(self, src_path):
        """Copy a file from the source folder to the target folder."""
        if self.filter_pattern and not self.filter_pattern.search(src_path):
            print(f"{Fore.BLUE}Skipped (no match):{Style.RESET_ALL} {src_path}")
            return

        try:
            relative_path = os.path.relpath(src_path, self.source_folder)
            target_path = os.path.join(self.target_folder, relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            # Copy file with metadata
            shutil.copy2(src_path, target_path)
            print(f"{Fore.GREEN}Copied:{Style.RESET_ALL} {src_path} -> {target_path}")
        except Exception as e:
            print(f"{Fore.RED}Error copying file {src_path}: {e}{Style.RESET_ALL}")

    def _delete_file(self, src_path):
        """Delete file from the target folder."""
        if self.filter_pattern and not self.filter_pattern.search(src_path):
            print(f"{Fore.BLUE}Skipped (no match):{Style.RESET_ALL} {src_path}")
            return
        print(f"{Fore.RED}Deleted (not synced):{Style.RESET_ALL} {src_path}")
        return
        try:
            relative_path = os.path.relpath(src_path, self.source_folder)
            target_path = os.path.join(self.target_folder, relative_path)
            if os.path.exists(target_path):
                os.remove(target_path)
                print(f"{Fore.RED}Deleted:{Style.RESET_ALL} {target_path}")
        except Exception as e:
            print(f"{Fore.RED}Error deleting file {src_path}: {e}{Style.RESET_ALL}")


def filesCloner(source, target, recursive, filter_pattern):
    # Verify folders
    if not os.path.exists(source) or not os.path.isdir(source):
        print(
            f"{Fore.RED}Error: Source path '{source}' is not a directory.{Style.RESET_ALL}"
        )
        return
    if not os.path.exists(target) or not os.path.isdir(target):
        print(
            f"{Fore.RED}Error: Target path '{target}' is not a directory.{Style.RESET_ALL}"
        )
        return

    # Convert paths to absolute if not already
    source = Path(source).resolve()
    target = Path(target).resolve()

    # Start the observer
    print(f"Watching folder: {source}")
    print(f"Duplicating files to: {target}")

    event_handler = MyHandler(source, target, recursive, filter_pattern)
    observer = Observer()
    observer.schedule(event_handler, path=source, recursive=recursive)
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
    )

    parser.add_argument(
        "--source", type=str, help="Source folder to watch", required=True
    )
    parser.add_argument(
        "--target", type=str, help="Target folder to copy files to", required=True
    )
    parser.add_argument("--recursive", action="store_true", help="Enable recursion")
    parser.add_argument(
        "--filter",
        type=str,
        help="Regex filter for files (e.g., '\\.txt$' to match .txt files)",
    )
    args = parser.parse_args()

    # Validate regex filter if provided
    if args.filter:
        try:
            re.compile(args.filter)
        except re.error as e:
            print(f"{Fore.RED}Invalid regex pattern: {e}{Style.RESET_ALL}")
            exit(1)

    filesCloner(args.source, args.target, args.recursive, args.filter)
