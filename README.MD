Here’s a `README.md` template for your **Files Cloner** project. You can adjust it based on any additional features or changes you may have made to the script.

---

# Files Cloner

A simple Python script to monitor a source folder and automatically copy new or modified files to a target folder. It can also delete files from the target folder if they are removed from the source. The script supports an optional regex filter for file types, recursion, and can be packaged as a standalone executable for Windows.

## Features

- **Automatic file synchronization**: Automatically copy new and modified files from a source directory to a target directory.
- **Delete files**: Optionally remove files from the target directory when they are deleted from the source.
- **Regex file filter**: Only copy files that match a given regular expression.
- **Recursion support**: Copy files from subdirectories (optional).
- **Cross-platform**: Can be run on both Linux and Windows, and built into a Windows executable.

## Requirements

- Python 3.x
- `watchdog` library for monitoring the source folder.
- `colorama` library for colored output in the terminal.

## Installation

1. **Clone this repository** or download the script.

2. **Install the required Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional**: To create a standalone executable for Windows, follow the instructions below.

## Usage

### Running the Script

To run the script, use the following command in your terminal:

```bash
python files_cloner.py --source <source_folder> --target <target_folder> [--recursive] [--filter <regex>]
```

#### Arguments:
- **`--source`**: The folder to monitor for changes. (Required)
- **`--target`**: The folder where files will be copied. (Required)
- **`--recursive`**: If specified, the script will monitor subdirectories as well. (Optional)
- **`--filter`**: A regular expression to filter the types of files to copy (e.g., `\\.txt$` to copy only `.txt` files). (Optional)

#### Example Usage:

1. Monitor a source folder and copy all `.txt` files to the target folder (without recursion):
   ```bash
   python files_cloner.py --source /path/to/source --target /path/to/target --filter "\.txt$"
   ```

2. Monitor a source folder with recursion and copy all files:
   ```bash
   python files_cloner.py --source /path/to/source --target /path/to/target --recursive
   ```

### Packaging as a Standalone Executable for Windows

To build a standalone Windows executable, use **PyInstaller**:

1. Install **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --console --name "files_cloner" files_cloner.py
   ```

3. The executable will be created in the `dist/` folder.

4. You can now run `files_cloner.exe` on a Windows machine without requiring Python to be installed.

## Features and Limitations

- **Supported Platforms**: The script works on both Linux and Windows. On Linux, it uses `inotify` for file monitoring, while on Windows, it uses `ReadDirectoryChangesW`.
- **Regex File Filter**: You can filter the files to be copied using regular expressions.
- **Delete Functionality**: Deleting files from the source folder will not automatically delete them from the target folder unless you modify the code or uncomment the `_delete_file()` function.

## Troubleshooting

- **Missing Dependencies**: Ensure all dependencies are installed via `pip install -r requirements.txt`.
- **Permissions**: Make sure that the script has the necessary permissions to access the source and target directories, especially when working on Windows.
- **File Path Lengths on Windows**: Windows has limitations on file path lengths. Ensure your paths are not too long if you're encountering issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
