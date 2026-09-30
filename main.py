import argparse
import json
import logging
from pathlib import Path

from src.file_concealment.folder_editor.gui import FileManagerApp

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="File Manager Application")
    parser.add_argument("-j", "--json-file", default="config/folder_paths.JSON", help="Path to the JSON file")
    parser.add_argument("-k", "--json-key", default="hidden_folders", help="Key for the JSON data")
    parser.add_argument("-p", "--powershell-script", default="scripts/folder concealer.ps1", help="Path to the PowerShell script")
    parser.add_argument("-i", "--icon-path", default="assets/bugatti_logo_1.png", help="Path to the application icon")
    return parser.parse_args()

def load_configuration(config_file: Path) -> dict | None:
    try:
        with config_file.open("r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Error loading configuration file: %s", e)
    return None

# main.py
def main():
    """
    Main entry point of the application.

    This function handles the following tasks:
    1. Configures the logging system.
    2. Parses command-line arguments.
    3. Loads the application configuration.
    4. Initializes and runs the File Manager application.
    5. Handles keyboard interrupts and unexpected exceptions.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    args = parse_arguments()
    config = load_configuration(Path(args.json_file))

    if config is None:
        logger.error("Failed to load configuration. Exiting...")
        return

    try:
        app = FileManagerApp(args.json_file, args.json_key, args.powershell_script, args.icon_path)
        app.mainloop()
    except Exception:
        logger.exception("An unexpected error occurred")
        print("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()

