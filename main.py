from src.file_concealment.folder_editor.gui import FileManagerApp

if __name__ == "__main__":
    import sys

    # Use command-line argument for JSON file path if provided, otherwise use default
    json_file_path = sys.argv[1] if len(sys.argv) > 1 else r"config/folder paths.JSON"
    json_key = sys.argv[2] if len(sys.argv) > 2 else "hidden_folders"
    powershell_script = sys.argv[3] if len(
        sys.argv) > 3 else r"file_concealment/folder concealer.ps1"
    icon_path = sys.argv[4] if len(
        sys.argv) > 3 else r"assets/bugatti_logo_1.png"

    try:
        app = FileManagerApp(json_file_path, json_key,powershell_script, icon_path)
        app.mainloop()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully...")
        app.destroy()  # Ensure all tkinter windows are closed
        sys.exit(0)  # Exit with a success status code
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit with an error status code


