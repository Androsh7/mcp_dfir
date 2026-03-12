"""Defines the data manager class"""

# Standard libraries
import json

# Third-party libraries
from pydantic import BaseModel, Field

# Project libraries
from llm_forensics.config import config
from llm_forensics.tools.models import AnalystNote, CommandRecord, CommandRecordSummary, AnalystNoteSummary


class CommandHistoryManager(BaseModel):
    command_summary_list: list[CommandRecordSummary] = Field(default_factory=list, init=False)

    def model_post_init(self, __context):
        # Load commands
        if config.command_history_json.exists():
            self.load()
        config.command_record_directory.mkdir(mode=500, exist_ok=True)

    def dump(self, command: CommandRecord | None, command_number: int | None = None):
        # Write to command history
        with open(file=config.command_history_json, mode="w", encoding="utf-8") as command_summary_file:
            json.dump(
                [record.model_dump() for record in self.command_summary_list],
                command_summary_file,
                indent=4,
            )

        # Write to command file
        if command is not None and command_number is not None:
            with open(file=config.command_record_directory / f'{command_number}.txt', mode="w", encoding="utf-8") as command_file:
                command_file.write(command.result)

    def load(self):
        with open(file=config.command_history_json, encoding="utf-8") as command_file:
            for command_summary_dict in json.load(command_file):
                self.command_summary_list.append(CommandRecordSummary.model_validate(command_summary_dict))

    def add_command(self, command_record: CommandRecord) -> CommandRecordSummary:
        number = len(self.command_summary_list) + 1
        summary = command_record.summary(number=number)
        self.command_summary_list.append(summary)
        self.dump(command_record, number)
        return summary

    def get_command(self, command_number: int) -> CommandRecord:
        for command in self.command_summary_list:
            if command.number == command_number:
                with open(file=config.command_record_directory / f'{command_number}.txt', mode="r", encoding="utf-8") as file:
                    return CommandRecord(
                        command=command.command,
                        date_run=command.date_run,
                        result=file.read(),
                    )
        raise KeyError(f"Could not find command with number {command_number}")

class AnalystNoteManager(BaseModel):
    note_list: list[AnalystNoteSummary] = Field(default_factory=list, init=False)

    def model_post_init(self, __context):
        if config.analyst_notes_list_json.exists():
            self.load()
        config.analyst_notes_directory.mkdir(mode=500, exist_ok=True)

    def dump(self, note: AnalystNote | None):
        # Update note summary
        with open(file=config.analyst_notes_list_json, mode="w", encoding="utf-8") as note_summary_file:
            json.dump(
                [note.model_dump() for note in self.note_list],
                note_summary_file,
                indent=4,
            )

        # Write to note file
        if note is not None:
            with open(file=config.analyst_notes_directory / f'{note.title}.md', mode="w", encoding="utf-8") as note_file:
                note_file.write(note.description)

    def load(self):
        with open(file=config.analyst_notes_list_json, encoding="utf-8") as note_file:
            for note_dict in json.load(note_file):
                self.note_list.append(AnalystNote.model_validate(note_dict))

    def add_note(self, note: AnalystNote) -> AnalystNote:
        self.note_list.append(note.summary())
        self.dump(note)
        return note

    def update_note(self, title: str, note: AnalystNote) -> AnalystNote:
        for index, note in enumerate(self.note_list):
            if note.title == title:
                self.note_list[index] = note.summary()
                self.dump(note)
                return note
        raise KeyError(f"No note with title '{title}'")

    def get_note(self, title: str) -> AnalystNote:
        for note in self.note_list:
            if note.title == title:
                with open(file=config.analyst_notes_directory / f'{title}.md', mode="r", encoding="utf-8") as note_file:
                    return AnalystNote(
                        title=note.title,
                        status=note.status,
                        tags=note.tags,
                        description=note_file.read()
                    )
        raise KeyError(f"No note with title '{title}'")

command_history_manager = CommandHistoryManager()
analyst_note_manager = AnalystNoteManager()
