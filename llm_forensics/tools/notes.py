"""Defines the notes mcp routes"""

# Project libraries
from llm_forensics.data_manager import data_manager
from llm_forensics.tools.models import AnalystNote, AnalystNoteSummary


def show_analyst_notes_summary() -> list[AnalystNoteSummary]:
    out_list = []
    for note in data_manager.note_list:
        out_list.append(note.summary())
    return out_list


def show_analyst_note(title: str) -> AnalystNote:
    for note in data_manager.note_list:
        if note.title == title:
            return note
    raise RuntimeError(f'Could not find analyst note with title: "{title}"')


def add_analyst_note(note: AnalystNote) -> None:
    data_manager.add_note(note=note)


def update_analyst_note(title: str, note: AnalystNote) -> None:
    data_manager.update_note(title=title, note=note)
