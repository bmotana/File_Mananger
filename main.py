import argparse
import logging
from pathlib import Path
from typing import Optional
import json
from src.file_concealment.folder_editor.gui import FileManagerApp

def parse_arguments():
    parser = argparse.ArgumentParser(description="File Manager Application")
    parser.add_argument("-j", "--json-file", default="config/folder paths.JSON", help="Path to the JSON file")
    parser.add_argument("-k", "--json-key", default="hidden_folders", help="Key for the JSON data")
    parser.add_argument("-p", "--powershell-script", default="scripts/folder concealer.ps1", help="Path to the PowerShell script")
    parser.add_argument("-i", "--icon-path", default="assets/bugatti_logo_1.png", help="Path to the application icon")
    return parser.parse_args()

def load_configuration(config_file: Path) -> Optional[dict]:
    try:
        with config_file.open("r") as f:
            import json
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration file: {e}")
    return None

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    args = parse_arguments()
    config = load_configuration(Path(args.json_file))

    if config is None:
        logging.error("Failed to load configuration. Exiting...")
        return

    try:
        app = FileManagerApp(args.json_file, args.json_key, args.powershell_script, args.icon_path)
        app.mainloop()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting gracefully...")
        app.destroy()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()

