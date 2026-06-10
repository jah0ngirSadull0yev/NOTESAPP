from __future__ import annotations

from datetime import datetime, date
from typing import Dict, Tuple


class Note:

    def __init__(self, id: int|str, text: str, created_date: date|str) -> None:
        self._id = abs(int(id))
        self.text = text
        self._created_date: date = datetime.fromisoformat(created_date).date() if isinstance(created_date, str) else created_date

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def created_date(self) -> date:
        return self._created_date
    
    @classmethod
    def copy(cls, note: Note):
        """Returns a copy of the `note`."""
        return cls(note.id, note.text, note.created_date)

    @classmethod
    def from_dict(cls, values: Dict[str, str]) -> Note|None:
        """Custom constructor from dictionary. Returns `None` if any of the keys are not found."""
        note_id = values.get("id")
        text = values.get("text")
        created_date = values.get("created_date")
        if any(i is None for i in (note_id, text, created_date)):
            return None
        return cls(note_id, text, created_date)

    @classmethod
    def from_tuple(cls, values: Tuple[str, str, str]) -> Note:
        """Custom constructor from tuple. Calls the default constructor unpacking the tuple."""
        return cls(*values)

    def as_dict(self) -> Dict[str, str]:
        """Returns dictionary with the properties as the keys and values as the values."""
        return {"id": str(self._id), "text": self.text, "created_date": str(self._created_date)}

    def as_tuple(self) -> Tuple[str, str, str]:
        """Returns a tuple from `Note`."""
        return (str(self._id), self.text, str(self._created_date))

    def __repr__(self) -> str:
        return f"Note(id={self._id}, text={self.text!r}, created_date={self._created_date!r})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def row(self):
        """Returns a formatted version of the `Note` for printing."""
        return f"id={self._id}\t created_date={self._created_date}\ntext:\n{self.text}"
    



if __name__ == "__main__":
    n1 = Note(1, "text", "")
    n2 = Note.from_dict({"id": 1, "text": "", "created_at": ""})
    print(n1)
    print(n2)

