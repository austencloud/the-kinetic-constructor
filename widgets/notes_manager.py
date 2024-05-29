from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject

from widgets.sequence_widget.edit_notes_dialog import EditNotesDialog

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class NotesManager(QObject):
    def __init__(self, settings_manager: "SettingsManager"):
        super().__init__()
        self.settings_manager = settings_manager
        self.previous_note = ""

    def populate_notes(self, notes_combo_box: QComboBox):
        self.notes_combo_box = notes_combo_box
        notes_combo_box.clear()
        notes = self.get_all_notes()

        for note in notes:
            notes_combo_box.addItem(note)
        notes_combo_box.addItem("Edit Notes")
        current_note = self.get_current_note()
        if current_note in notes:
            index = notes_combo_box.findText(current_note)
            if index != -1:
                notes_combo_box.setCurrentIndex(index)
        else:
            notes_combo_box.setCurrentIndex(0)

    def open_edit_notes_dialog(self):
        dialog = EditNotesDialog(self)
        if dialog.exec():
            self.populate_notes(self.notes_combo_box)

    def get_all_notes(self):
        return self.settings_manager.settings.get("notes", [])

    def add_new_note(self, note):
        notes = self.settings_manager.settings.get("notes", [])
        if note in notes:
            return False
        notes.append(note)
        self.settings_manager.settings["notes"] = notes
        return True

    def remove_note(self, note):
        notes = self.settings_manager.settings.get("notes", [])
        if note in notes:
            notes.remove(note)
            self.settings_manager.settings["notes"] = notes
            return True
        return False

    def save_notes(self):
        self.settings_manager.save_settings()

    def get_current_note(self):
        return self.settings_manager.settings.get("current_note", "")

    def set_current_note(self, note):
        if note != "Edit Notes":
            self.settings_manager.settings["current_note"] = note
        index = self.notes_combo_box.findText(note)
        if index != -1:
            self.notes_combo_box.setCurrentIndex(index)

    def get_previous_note(self):
        return self.previous_note
