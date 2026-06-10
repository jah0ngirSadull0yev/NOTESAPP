from typing import Dict

from .note import Note
from .storage import Storage


class Notebook:
    
    def __init__(self, storage: Storage) -> None:
        self.__storage = storage
        self.notes: Dict[int, Note] = self.__storage.load()

    def add_note(self, note: Note) -> None:
        """"Adds the given Note object into the existing list of notes.
        
        Results in updating if the `note` already exists."""
        self.notes[note.id] = note

    def update_note(self, note: Note) -> Note|None:
        """Updates the note with the `Note` in the list that has the same `id` as the `note` to the `note`, and returns the old value. 
    
        Results in adding the item and returning `None` if the `note_id` does not exist.

        The `created_date` does not get updated."""
        old = self.notes.get(note.id)
        if old is not None:
            note = Note(note.id, note.text, old.created_date)
        self.notes[note.id] = note
        return old

    def delete_note(self, note_id: int) -> Note|None:
        """Deletes the note with the given `note_id` from the list of notes, and returns the deleted `Note` object.
        
        Returns `None` if the `note_id` does not exist."""
        return self.notes.pop(note_id, None)

    def get_notes(self) -> Dict[int, Note]:
        """Returns the dictionary of notes."""
        return self.notes

    def get_note(self, note_id: int) -> Note|None:
        """Returns the `Note` object with matching id or `None`."""
        return self.notes.get(note_id)

    def save(self) -> None:
        """Saves the internal dictionary to the storage. 
        
        Do not call relentlessly, as this might slow down the program."""
        self.__storage.save(self.notes)

    def generate_id(self) -> int:
        """Generates an `id` for a new `Note`"""
        return max(1, max(self.notes)+1) if len(self.notes) > 0 else 1



if __name__ == "__main__":
    notebook1 = Notebook()
    print(notebook1.notes)


