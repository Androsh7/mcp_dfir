"""Defines the notes mcp routes"""

# Project libraries
from mcp_dfir.data_manager import analyst_note_manager
from mcp_dfir.tools.models import AnalystNote, AnalystNoteSummary


def show_analyst_notes_summary() -> list[AnalystNoteSummary]:
    return analyst_note_manager.note_list


def show_analyst_note(title: str) -> AnalystNote:
    return analyst_note_manager.get_note(title=title)


def add_analyst_note(note: AnalystNote) -> None:
    analyst_note_manager.add_note(note=note)


def update_analyst_note(title: str, note: AnalystNote) -> None:
    analyst_note_manager.update_note(title=title, note=note)
