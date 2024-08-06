from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject

from widgets.sequence_widget.edit_notes_dialog import EditNotesDialog

if TYPE_CHECKING:
    from settings_manager.user_profile_settings import UserProfileSettings


class NotesManager(QObject):
    def __init__(self, user_profile_settings: "UserProfileSettings"):
        super().__init__()
        self.user_profile_settings = user_profile_settings
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
        return self.user_profile_settings.settings.get("saved_notes", [])

    def add_new_note(self, note):
        notes = self.user_profile_settings.settings.get("saved_notes", [])
        if note in notes:
            return False
        notes.append(note)
        self.user_profile_settings.settings["saved_notes"] = notes
        return True

    def remove_note(self, note):
        notes = self.user_profile_settings.settings.get("saved_notes", [])
        if note in notes:
            notes.remove(note)
            self.user_profile_settings.settings["saved_notes"] = notes
            return True
        return False

    def save_notes(self):
        self.user_profile_settings.settings_manager.save_settings()

    def get_current_note(self):
        return self.user_profile_settings.settings.get("current_note", "")

    def set_current_note(self, note):
        if note != "Edit Notes":
            self.user_profile_settings.settings["current_note"] = note
        index = self.notes_combo_box.findText(note)
        if index != -1:
            self.notes_combo_box.setCurrentIndex(index)

    def get_previous_note(self):
        return self.previous_note
