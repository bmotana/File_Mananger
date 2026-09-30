# File Manager

A small Windows desktop app for keeping a list of folders and marking their contents as hidden in Windows Explorer. The app uses a Tkinter interface and stores the folder list in a JSON configuration file.

> **Note:** The app changes Windows hidden attributes and Explorer's hidden-file display settings. Hidden files are not encrypted or protected; anyone who enables hidden items can still view them. Keep backups of important files.

## Requirements

- Windows
- Python 3.10 or newer
- Tkinter (included with most Windows Python installations)
- Pillow

## Setup

1. Clone or download this repository and open a terminal in the project folder.
2. (Recommended) Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, open Command Prompt and run `.venv\Scripts\activate.bat`, or use `.venv\Scripts\python.exe` directly.

3. Install the Python dependency:

   ```powershell
   py -m pip install Pillow
   ```

4. Start the app:

   ```powershell
   py main.py
   ```

## Use

- **Add Path** opens a folder picker and adds the selected folder to the list.
- **Delete Path** removes the selected entry from the list. It does not delete the folder or its contents.
- **Check Paths** reports whether the listed paths currently exist.
- **Run Folder Hider** applies the Windows hidden attribute to the listed folders and their contents. Review the paths before running it.

The folder list is stored in `config/folder_paths.JSON` under the `hidden_folders` key. The checked-in file starts with an empty list. You can also edit it directly, using valid JSON, for example:

```json
{
  "hidden_folders": [
    "C:\\Users\\Example\\Documents\\Archive"
  ]
}
```

## Command-line options

Run `py main.py --help` to see the available options:

| Option | Default | Purpose |
| --- | --- | --- |
| `-j`, `--json-file` | `config/folder_paths.JSON` | Configuration file containing folder paths |
| `-k`, `--json-key` | `hidden_folders` | JSON key containing the list of paths |
| `-p`, `--powershell-script` | `scripts/folder concealer.ps1` | PowerShell script path passed to the app |
| `-i`, `--icon-path` | `assets/bugatti_logo_1.png` | Window icon path |

## Project contents

- `main.py` — application entry point
- `src/` — GUI and file handling code
- `config/folder_paths.JSON` — starter configuration
- `assets/` — application images
- `scripts/` — PowerShell-related files

## Troubleshooting

- If the app cannot start, confirm that Python is installed and that `python -m tkinter` opens a test window.
- If the icon does not load, check that the asset exists; the app can still run without an icon by passing an empty value for `--icon-path`.
- If a path check fails, confirm that the folder still exists and that the current Windows account can access it.
