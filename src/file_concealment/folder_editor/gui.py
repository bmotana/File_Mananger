from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.file_concealment.folder_editor.powershell_runner import PowerShellRunner
from src.file_concealment.folder_editor.file_system_handler import FileSystemHandler
from src.file_concealment.folder_editor.json_editor import JsonEditor
from PIL import Image, ImageTk  # You'll need to install pillow: pip install pillow
from src.file_concealment.folder_concealer import FolderHider


class FileManagerApp(tk.Tk):
    """Main application class for the File Manager GUI."""

    def __init__(self, json_file: str, json_key: str, powershell_script: str, icon_path: str = None):
        super().__init__()

        self.title("File Manager")
        self.geometry("450x300")

        self.json_editor = JsonEditor(json_file)
        self.json_key = json_key
        self.paths = self.json_editor.get_entry(self.json_key) or []
        self.powershell_runner = PowerShellRunner(powershell_script)
        self.folder_hider = FolderHider(json_file)

        self.set_window_icon(icon_path)
        self.create_widgets()

    def set_window_icon(self, icon_path: str) -> None:
        """Set the window icon."""
        if icon_path:
            try:
                if icon_path.lower().endswith('.ico'):
                    self.iconbitmap(icon_path)
                else:
                    icon = Image.open(icon_path)
                    icon = ImageTk.PhotoImage(icon)
                    self.iconphoto(True, icon)
            except Exception as e:
                print(f"Error setting icon: {e}")

    def create_widgets(self) -> None:
        """Create and place all widgets in the main window."""
        # Frame for the list of paths
        self.path_frame = ttk.Frame(self)
        self.path_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox to display paths
        self.path_listbox = tk.Listbox(self.path_frame)
        self.path_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(self.path_frame, orient=tk.VERTICAL, command=self.path_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.path_listbox.config(yscrollcommand=scrollbar.set)

        # Populate the listbox
        self.update_path_list()

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill=tk.X)

        # Run Folder Hider button
        run_script_btn = ttk.Button(button_frame, text="Run Folder Hider", command=self.run_folder_hider)
        run_script_btn.pack(side=tk.LEFT, padx=5)

        # Check paths button
        check_paths_btn = ttk.Button(button_frame, text="Check Paths", command=self.check_paths)
        check_paths_btn.pack(side=tk.LEFT, padx=5)

        # Add path button
        add_path_btn = ttk.Button(button_frame, text="Add Path", command=self.add_path)
        add_path_btn.pack(side=tk.LEFT, padx=5)

        # Delete path button
        delete_path_btn = ttk.Button(button_frame, text="Delete Path", command=self.delete_path)
        delete_path_btn.pack(side=tk.LEFT, padx=5)

    def update_path_list(self) -> None:
        """Update the listbox with current paths."""
        self.path_listbox.delete(0, tk.END)
        for path in self.paths:
            self.path_listbox.insert(tk.END, path)

    def run_powershell_script(self) -> None:
        """Run the PowerShell script."""
        stdout, stderr, return_code = self.powershell_runner.run_script()
        if return_code == 0:
            messagebox.showinfo("PowerShell Script", f"Script executed successfully.\nOutput: {stdout}")
        else:
            messagebox.showerror("PowerShell Script Error", f"Script failed with error code {return_code}.\nError: {stderr}")

    def run_folder_hider(self) -> None:
        """Run folder hider."""
        result, message = self.folder_hider.run()
        if result:
            messagebox.showinfo("Folder Hider", f" Runner executed successfully.\nOutput: {message}")
        else:
            messagebox.showerror("Folder Hider Error", f" Opps, something went wrong \nError: {message}")

    def check_paths(self) -> None:
        """Check if all paths are valid using FileSystemHandler."""
        invalid_paths = []
        for path in self.paths:
            handler = FileSystemHandler(path)
            if not handler.is_valid_path():
                invalid_paths.append(path)

        if invalid_paths:
            messagebox.showwarning("Invalid Paths", f"The following paths are invalid:\n{', '.join(invalid_paths)}")
        else:
            messagebox.showinfo("Path Check", "All paths are valid.")

    def add_path(self) -> None:
        """Open a dialog to add a new path."""
        new_path = filedialog.askdirectory()
        if new_path:
            self.json_editor.append_to_list(self.json_key, new_path)
            self.paths = self.json_editor.get_entry(self.json_key)
            self.update_path_list()
        else:
            messagebox.showwarning("Add Path", "No path was entered.")


    def delete_path(self) -> None:
        """Delete the selected path from the list."""
        selection = self.path_listbox.curselection()
        if selection:
            index = selection[0]
            path_to_remove = self.paths[index]
            self.json_editor.remove_from_list(self.json_key, path_to_remove)
            self.paths = self.json_editor.get_entry(self.json_key)
            self.update_path_list()
        else:
            messagebox.showwarning("Delete Path", "Please select a path to delete.")

    # method where you can turn on the automtic powershell script execution on Task Schedular


# TODO:
# set-up
# make github ready
    # make an executable by click and not from the ternimal
    # make a setup.py maybe
    # put it in zipfile of something
# have an emppt json file
# make more compaitable
# sort of end to end
#using relative files and not absolute
