import os


class FileSystemHandler:
    """
    A class to handle file system operations for a given path.
    """

    def __init__(self, path: str):
        """
        Initialize the FileSystemHandler with a file or folder path.

        Args:
            path (str): The path to the file or folder.
        """
        self.path = os.path.normpath(path)

    def is_valid_path(self) -> bool:
        """
        Check if the given path is valid.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(self.path)

    def get_name(self) -> str:
        """
        Get the name of the file or folder.

        Returns:
            str: The name of the file or folder.
        """
        return os.path.basename(self.path)

    def is_file(self) -> bool:
        """
        Check if the path points to a file.

        Returns:
            bool: True if it's a file, False otherwise.
        """
        return os.path.isfile(self.path)

    def is_folder(self) -> bool:
        """
        Check if the path points to a folder.

        Returns:
            bool: True if it's a folder, False otherwise.
        """
        return os.path.isdir(self.path)

    def list_contents(self) -> list[str] | None:
        """
        List the contents of the folder if the path is a directory.

        Returns:
            Union[List[str], None]: A list of file/folder names in the directory,
                                    or None if the path is not a valid directory.
        """
        if self.is_folder():
            try:
                return os.listdir(self.path)
            except PermissionError:
                print(f"Permission denied: Unable to list contents of {self.path}")
                return None
        else:
            print(f"{self.path} is not a directory.")
            return None
