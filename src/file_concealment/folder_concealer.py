import json
import os
import stat
import subprocess
import winreg
from src.file_concealment.folder_editor.json_editor import JsonEditor


class FolderHider:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.json_content = JsonEditor(json_file_path).json_data

    @staticmethod
    def set_hidden(path):
        if os.name == 'nt':  # For Windows
            subprocess.call(['attrib', '+H', path])
        elif os.name == 'posix':  # For Unix-like systems
            current = os.stat(path)
            os.chmod(path, current.st_mode | stat.S_IRUSR)

    def hide_folders(self):
        for folder in self.json_content['hidden_folders']:
            for root, dirs, files in os.walk(folder):
                for item in dirs + files:
                    path = os.path.join(root, item)
                    self.set_hidden(path)

            # Set the main folder as hidden
            self.set_hidden(folder)

    @staticmethod
    def set_registry_value(key_path, value_name, value_data):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        except WindowsError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
        winreg.CloseKey(key)

    def update_registry(self):
        if os.name == 'nt':
            self.set_registry_value(r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", 2)
            self.set_registry_value(r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowSuperHidden",
                                    0)

    def run(self):
        try:
            self.hide_folders()
            self.update_registry()
            return True, "Folders hidden!"
        except Exception as e:
            return False, f"Error hiding folders: {e}"

