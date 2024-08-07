import json
from typing import Dict, Any, Union


class JsonEditor:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.json_data = None
        try:
            with open(self.json_file) as f:
                self.json_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")


    def save(self) -> None:
        """Save the JSON data to the file."""
        try:
            with open(self.json_file, "w") as f:
                json.dump(self.json_data, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving JSON file: {e}")

    def read(self) -> Dict[str, Any]:
        """
        Read and return the JSON data.

        Returns:
            Dict[str, Any]: The JSON data as a dictionary.
        """
        return self.json_data

    def add_entry(self, key: str, value: Any) -> None:
        """
        Add a new entry to the JSON data.

        Args:
            key (str): The key for the new entry.
            value (Any): The value for the new entry.
        """
        self.json_data[key] = value
        self.save()

    def get_entry(self, key: str) -> Union[Any, None]:
        """
        Get the value of an entry in the JSON data.
        """
        return self.json_data.get(key)

    def remove_entry(self, key: str) -> None:
        """
        Remove an entry from the JSON data.

        Args:
            key (str): The key of the entry to remove.
        """
        if key in self.json_data:
            del self.json_data[key]
            self.save()
        else:
            raise KeyError(f"Key {key} not found.")

    def append_to_list(self, key: str, value: Any) -> None:
        """
        Append a value to a list in the JSON data.

        Args:
            key (str): The key of the list.
            value (Any): The value to append.
        """
        if key not in self.json_data:
            self.json_data[key] = []
        self.json_data[key].append(value)
        self.save()

    def remove_from_list(self, key: str, value: Any) -> None:
        """
        Remove a value from a list in the JSON data.

        Args:
            key (str): The key of the list.
            value (Any): The value to remove.
        """
        if key in self.json_data and isinstance(self.json_data[key], list):
            self.json_data[key] = [item for item in self.json_data[key] if item != value]
            self.save()
