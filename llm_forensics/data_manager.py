"""Defines the data manager class"""

# Standard libraries
import json

# Third-party libraries
from pydantic import BaseModel, Field

# Project libraries
from llm_forensics.constants import COMMAND_LIST_PATH, NOTE_LIST_PATH
from llm_forensics.tools.models import AnalystNote, CommandRecord


class DataManager(BaseModel):
    command_list: list[CommandRecord] = Field(default_factory=list, init=False)
    note_list: list[AnalystNote] = Field(default_factory=list, init=False)

    def model_post_init(self, __context):
        if COMMAND_LIST_PATH.exists():
            self.load_history_from_file()
        if NOTE_LIST_PATH.exists():
            self.load_note_from_file()

    def dump_history_to_file(self):
        with open(file=COMMAND_LIST_PATH, mode="w", encoding="utf-8") as command_file:
            json.dump(
                [record.model_dump() for record in self.command_list],
                command_file,
            )

    def load_history_from_file(self):
        with open(file=COMMAND_LIST_PATH, encoding="utf-8") as command_file:
            for command_record_dict in json.load(command_file):
                self.command_list.append(CommandRecord.model_validate(command_record_dict))

    def dump_note_to_file(self):
        with open(file=NOTE_LIST_PATH, mode="w", encoding="utf-8") as note_file:
            json.dump(
                [note.model_dump() for note in self.note_list],
                note_file,
            )

    def load_note_from_file(self):
        with open(file=NOTE_LIST_PATH, encoding="utf-8") as note_file:
            for note_dict in json.load(note_file):
                self.note_list.append(AnalystNote.model_validate(note_dict))

    def add_command(self, command_record: CommandRecord) -> CommandRecord:
        self.command_list.append(command_record)
        self.dump_history_to_file()
        return command_record

    def add_note(self, note: AnalystNote) -> AnalystNote:
        self.note_list.append(note)
        self.dump_note_to_file()
        return note

    def update_note(self, title: str, note: AnalystNote) -> AnalystNote:
        for index, note in enumerate(self.note_list):
            if note.title == title:
                self.note_list[index] = note
                self.dump_note_to_file()
                return note
        raise KeyError(f"No note with title '{title}'")


data_manager = DataManager()
