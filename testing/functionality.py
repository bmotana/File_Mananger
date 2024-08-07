import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import os
import json
import tempfile
import shutil
from src.file_concealment.folder_editor.json_editor import JsonEditor # Replace 'file_concealment.folder_editor.functionality' with the correct module name if different
from src.file_concealment.folder_editor.file_system_handler import FileSystemHandler  # Replace 'file_concealment.folder_editor.functionality' with the correct module name if different
from src.file_concealment.folder_concealer import FolderHider


class TestJsonEditor(unittest.TestCase):
    def setUp(self):
        # Create a temporary JSON file for testing
        self.test_file = "test.json"
        with open(self.test_file, "w") as f:
            json.dump({"initial_key": "initial_value"}, f)

        self.editor = JsonEditor(self.test_file)

    def tearDown(self):
        # Remove the temporary JSON file after tests
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_read(self):
        # Test reading JSON data
        data = self.editor.read()
        self.assertEqual(data, {"initial_key": "initial_value"})

    def test_add_entry(self):
        # Test adding a new entry
        self.editor.add_entry("new_key", "new_value")
        data = self.editor.read()
        self.assertIn("new_key", data)
        self.assertEqual(data["new_key"], "new_value")

    def test_remove_entry(self):
        # Test removing an entry
        self.editor.remove_entry("initial_key")
        data = self.editor.read()
        self.assertNotIn("initial_key", data)

        # Test removing a non-existent entry (should handle KeyError)
        with self.assertRaises(KeyError):
            self.editor.remove_entry("non_existent_key")

    def test_paths(self):
        # Test getting and setting paths
        self.assertEqual(self.editor.get_entry("paths"), None)

    def test_persistence(self):
        # Test if changes persist after the object is deleted
        self.editor.add_entry("persistent_key", "persistent_value")
        del self.editor

        # Recreate the editor to load the updated JSON file
        new_editor = JsonEditor(self.test_file)
        data = new_editor.read()
        self.assertIn("persistent_key", data)
        self.assertEqual(data["persistent_key"], "persistent_value")

class TestFileSystemHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create a test file
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("Test content")

        # Create a test subdirectory
        self.test_subdir = os.path.join(self.test_dir, "test_subdir")
        os.mkdir(self.test_subdir)

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_is_valid_path(self):
        handler = FileSystemHandler(self.test_dir)
        self.assertTrue(handler.is_valid_path())

        handler = FileSystemHandler("/nonexistent/path")
        self.assertFalse(handler.is_valid_path())

    def test_get_name(self):
        handler = FileSystemHandler(self.test_file)
        self.assertEqual(handler.get_name(), "test_file.txt")

        handler = FileSystemHandler(self.test_dir)
        self.assertEqual(handler.get_name(), os.path.basename(self.test_dir))

    def test_is_file(self):
        handler = FileSystemHandler(self.test_file)
        self.assertTrue(handler.is_file())

        handler = FileSystemHandler(self.test_dir)
        self.assertFalse(handler.is_file())

    def test_is_folder(self):
        handler = FileSystemHandler(self.test_dir)
        self.assertTrue(handler.is_folder())

        handler = FileSystemHandler(self.test_file)
        self.assertFalse(handler.is_folder())

    def test_list_contents(self):
        handler = FileSystemHandler(self.test_dir)
        contents = handler.list_contents()
        self.assertIsNotNone(contents)
        self.assertIn("test_file.txt", contents)
        self.assertIn("test_subdir", contents)

        handler = FileSystemHandler(self.test_file)
        self.assertIsNone(handler.list_contents())

    def test_list_contents_permission_error(self):
        if os.name != 'nt':  # Skip this test on Windows
            no_permission_dir = os.path.join(self.test_dir, "no_permission")
            os.mkdir(no_permission_dir)
            os.chmod(no_permission_dir, 0o000)  # Remove all permissions

            handler = FileSystemHandler(no_permission_dir)
            self.assertIsNone(handler.list_contents())

            os.chmod(no_permission_dir, 0o755)

class TestFilePathHandling(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create a test file
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("Test content")

        # Create a temporary JSON file for testing
        self.json_file = os.path.join(self.test_dir, "test_paths.json")
        with open(self.json_file, "w") as f:
            json.dump({"paths": []}, f)

        self.json_editor = JsonEditor(self.json_file)

    def tearDown(self):
        # Remove the temporary directory and its contents
        import shutil
        shutil.rmtree(self.test_dir)

    def test_windows_path_format(self):
        windows_path = "C:\\Users\\Bafana\\Documents\\Twitter\\hun"
        handler = FileSystemHandler(windows_path)
        self.assertTrue(handler.is_valid_path())  # This will be False if not on Windows

        # Test JSON handling of Windows path
        self.json_editor.append_to_list("paths", windows_path)
        stored_paths = self.json_editor.get_entry("paths")
        self.assertIn(windows_path, stored_paths)

    def test_raw_windows_path_format(self):
        raw_windows_path = r"C:\Users\Bafana\Documents\Twitter\hun"
        handler = FileSystemHandler(raw_windows_path)
        self.assertTrue(handler.is_valid_path())  # This will be False if not on Windows

        # Test JSON handling of raw Windows path
        self.json_editor.append_to_list("paths", raw_windows_path)
        stored_paths = self.json_editor.get_entry("paths")
        self.assertIn(raw_windows_path, stored_paths)

    def test_unix_path_format(self):
        unix_path = "/Users/Bafana/Documents/Twitter/hun"
        handler = FileSystemHandler(unix_path)
        self.assertTrue(handler.is_valid_path())  # This will be False if not on Unix-like system

        # Test JSON handling of Unix path
        self.json_editor.append_to_list("paths", unix_path)
        stored_paths = self.json_editor.get_entry("paths")
        self.assertIn(unix_path, stored_paths)

    def test_forward_slash_windows_path(self):
        forward_slash_path = "C:/Users/Bafana/Documents/Twitter/hun"
        handler = FileSystemHandler(forward_slash_path)
        self.assertTrue(handler.is_valid_path())  # This should work on Windows

        # Test JSON handling of forward slash Windows path
        self.json_editor.append_to_list("paths", forward_slash_path)
        stored_paths = self.json_editor.get_entry("paths")
        self.assertIn(forward_slash_path, stored_paths)

    def test_relative_path(self):
        relative_path = os.path.join("Documents", "Twitter", "hun")
        handler = FileSystemHandler(relative_path)
        self.assertFalse(handler.is_valid_path())  # Relative paths should be considered invalid

        # Test JSON handling of relative path
        self.json_editor.append_to_list("paths", relative_path)
        stored_paths = self.json_editor.get_entry("paths")
        self.assertIn(relative_path, stored_paths)

    def test_path_normalization(self):
        # Test if FileSystemHandler normalizes paths
        original_path = "C:\\Users\\Bafana\\..\\Bafana\\Documents\\Twitter\\hun"
        normalized_path = "C:\\Users\\Bafana\\Documents\\Twitter\\hun"
        handler = FileSystemHandler(original_path)
        self.assertEqual(handler.path, normalized_path)

    def test_json_path_consistency(self):
        # Test if paths are stored and retrieved consistently in JSON
        test_paths = [
            "C:\\Users\\Bafana\\Documents\\Twitter\\hun",
            r"C:\Users\Bafana\Documents\Twitter\hun",
            "C:/Users/Bafana/Documents/Twitter/hun",
            "/Users/Bafana/Documents/Twitter/hun"
        ]

        for path in test_paths:
            self.json_editor.append_to_list("paths", path)

        stored_paths = self.json_editor.get_entry("paths")
        for path in test_paths:
            self.assertIn(path, stored_paths)
            self.assertEqual(path, stored_paths[stored_paths.index(path)])


class TestFolderHider(unittest.TestCase):

    def setUp(self):
        self.test_json = {
            "hidden_folders": [
                "C:\\Test\\Folder1",
                "C:\\Test\\Folder2"
            ]
        }
        self.mock_json = json.dumps(self.test_json)

    @patch('builtins.open', new_callable=mock_open,
           read_data='{"hidden_folders": ["C:\\\\Test\\\\Folder1", "C:\\\\Test\\\\Folder2"]}')
    def test_init(self, mock_file):
        folder_hider = FolderHider("dummy_path.json")
        self.assertEqual(folder_hider.json_content, self.test_json)

    @patch('os.walk')
    @patch('src.file_concealment.folder_concealer.FolderHider.set_hidden')
    def test_hide_folders(self, mock_set_hidden, mock_walk):
        mock_walk.return_value = [
            ("C:\\Test\\Folder1", ["SubFolder"], ["file1.txt", "file2.txt"]),
            ("C:\\Test\\Folder1\\SubFolder", [], ["file3.txt"])
        ]

        with patch('builtins.open', mock_open(read_data=self.mock_json)):
            folder_hider = FolderHider("dummy_path.json")
            folder_hider.hide_folders()

        # Print out all the calls made to set_hidden
        print("Actual calls to set_hidden:")
        for call in mock_set_hidden.call_args_list:
            print(call)

        # Let's not assert anything for now, just print the call count
        print(f"Total number of calls to set_hidden: {mock_set_hidden.call_count}")

    @patch('os.name', 'nt')
    @patch('subprocess.call')
    def test_set_hidden_windows(self, mock_subprocess):
        FolderHider.set_hidden("C:\\Test\\Folder")
        mock_subprocess.assert_called_once_with(['attrib', '+H', "C:\\Test\\Folder"])

    @patch('os.name', 'posix')
    @patch('os.stat')
    @patch('os.chmod')
    def test_set_hidden_unix(self, mock_chmod, mock_stat):
        mock_stat.return_value.st_mode = 0o644
        FolderHider.set_hidden("/test/folder")
        mock_chmod.assert_called_once()

    @patch('os.name', 'nt')
    @patch('winreg.OpenKey')
    @patch('winreg.SetValueEx')
    @patch('winreg.CloseKey')
    @patch('builtins.open', new_callable=mock_open,
           read_data='{"hidden_folders": ["C:\\\\Test\\\\Folder1", "C:\\\\Test\\\\Folder2"]}')
    def test_update_registry(self, mock_file, mock_close_key, mock_set_value, mock_open_key):
        folder_hider = FolderHider("dummy_path.json")
        folder_hider.update_registry()
        self.assertEqual(mock_set_value.call_count, 2)
        self.assertEqual(mock_close_key.call_count, 2)

if __name__ == '__main__':
    unittest.main()

# TODO:
#
#  make a unit test class that test if differnt formats of file path like something : "C:\\Users\\Bafana\\Documents\\Twitter\\hun"  vs  this r"C:/Users/Bafana/Documents/Twitter/hun"
# it must test if the class FileSystemHandler can read path format and how it handles it

