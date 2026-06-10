import sys
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

from core import Note, JSONFile, Notebook
from datetime import date


kb = KeyBindings()

@kb.add('escape', 'enter')
def _(event):
    event.current_buffer.insert_text('\n')

@kb.add('enter')
def _(event):
    event.current_buffer.validate_and_handle()


class ConsoleApp:

    def __init__(self):
        self.__notebook = Notebook(JSONFile("notes.json"))
        self.commands = {
            "1": self.__show_notes,
            "2": self.__show_note,
            "3": self.__add_note,
            "4": self.__update_note,
            "5": self.__delete_note,
            "6": self.__save,
            "m": self.__show_menu,
            "q": self.__quit
        }
        self.is_saved = True

    def run(self) -> None:
        print(self.__show_menu())
        while True:
            choice = input("Choice: ")
            command = self.commands.get(choice.strip().lower())
            if command:
                command()
            else:
                print("Invalid choice")
            print("")            

    def __show_notes(self) -> None:
        print(("\n"+32*"-"+"\n").join(i.row() for i in self.__notebook.get_notes().values()))

    def __show_note(self) -> None:
        note_id = self._input_id()
        note = self.__notebook.get_note(note_id)
        if note is not None:
            print(note.row())
        else:
            print("Note not found")

    def _input_id(self):
        """Inputs the id."""
        while True:
            try:
                note_id = int(input("Enter note id: "))
            except ValueError:
                print("note_id must be a positive integer!")
                continue
            if note_id >= 0:
                break
        return note_id

    def __add_note(self) -> None:
        note_id = self.__notebook.generate_id()
        print("Enter text: ")
        text = prompt("> ", multiline=True, key_bindings=kb)
        self.__notebook.add_note(Note(note_id, text, date.today()))
        self.is_saved = False

    def __update_note(self) -> None:
        note_id = self._input_id()
        print("Enter new text: ")
        new_text = prompt("> ", multiline=True, key_bindings=kb)
        result = self.__notebook.update_note(
            Note(note_id, new_text,
                  date.today() # date will not be updated anyway
            )
        )
        if not result:
            print("note_id not found in the list. New note was added instead of updating.")
        self.is_saved = False

    def __delete_note(self) -> None:
        note_id = self._input_id()
        d = self.__notebook.delete_note(note_id)
        if d is None:
            print("Nothing was deleted, id not found.")
        else:
            print(f"Deleted note: {d}")
            self.is_saved = False
    
    def __save(self) -> None:
        self.__notebook.save()
        print("Changes are saved to the file")
        self.is_saved = True

    def __show_menu(self) -> None:
        print("""
1. Show all notes
2. Show note details
3. Write new note
4. Update existing note
5. Delete existing note
6. Save changes to the file
m. Show menu again
q. Quit application
TIP: Alt+Enter for a new line
""")

    def __quit(self) -> None:
        if not self.is_saved:
            s = input("There are changes that are not saved to the file,\n do you want to save them (Y/n) or cancel exitting (c) ?\n (Y/n/c ; default=c) ").strip().lower()
            if s == "y":
                self.__notebook.save()
            elif s == "n":
                sys.exit()
        else:
            sys.exit()



if __name__ == "__main__":
    app = ConsoleApp()
    app.run()

