import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict

from .note import Note


class Storage(ABC):

    @abstractmethod
    def save(self, notes: Dict[int, Note]) -> None:
        pass

    @abstractmethod
    def load(self) -> Dict[int, Note]:
        pass

    @property
    @abstractmethod
    def info(self) -> Dict[str, str]:
        pass


class JSONFile(Storage):

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, "w", encoding="utf-8") as file:
                pass

    def save(self, notes: Dict[int, Note]) -> None:
        """Saves the data to the file."""
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump({str(key): val.as_dict() for key, val in notes.items()}, file, indent=4)

    def load(self) -> Dict[int, Note]:
        """Returns the data from the file."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                data: Dict[str, Dict[str, str]] = json.load(file)
                if not isinstance(data, dict):
                    return {}
                return self._fix_mismatch({int(key): Note.from_dict(val) for key, val in data.items() if self.__is_valid(key, val)})
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(data, file)
            return data

    def __is_valid(self, key: str, val: Dict[str, str]) -> bool:
        """Private function to check if the key-value pair is a proper `Note`."""
        try:
            key = int(key.strip())
            if not isinstance(val, dict):
                return False
        except ValueError:
            return False
        return True

    def _fix_mismatch(self, data: Dict[int, Note], match="note"):
        """Loops through the data to see if any key is different than the id of its `Note`.

        `match` can be `"note"` or `"key"`:
        - `"note"` changes the key to the `Note`'s id
        - `"key"` changes the `Note`'s id to the key
        - else removes it

        Returns the fixed data, mutating it."""
        match = match.lower().strip()
        for key, val in data.items():
            if key != val.id:
                if match == "key":
                    data[key] = Note(key, val.text, val.created_date)
                elif match == "note":
                    data[val.id] = Note.copy(val)
                    data.pop(key)
                else:
                    data.pop(key)
        return data

    def info(self) -> Dict[str, str]:
        return {"file_name": self.file_name}




