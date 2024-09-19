from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QCheckBox,
    QWidget,
    QHBoxLayout,
    QComboBox,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt

if TYPE_CHECKING:
    from .image_export_dialog import ImageExportDialog


class ExportDialogControlPanel(QWidget):
    notesChanged = pyqtSignal(str)

    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__()
        self.export_dialog = export_dialog
        self.settings_manager = export_dialog.export_manager.settings_manager
        self.user_combo_box = QComboBox(self)
        self.settings_manager.users.user_manager.populate_user_profiles_combo_box(
            self.user_combo_box
        )
        self.notes_manager = self.settings_manager.users.notes_manager
        self.user_manager = self.settings_manager.users.user_manager

        self.notes_combo_box = QComboBox(self)
        self.notes_manager.populate_notes(self.notes_combo_box)
        self.notes_combo_box.currentIndexChanged.connect(self._handle_note_selection)

        self.previous_note = self.notes_manager.get_current_note()
        self.previous_user = self.user_manager.get_current_user()

        self._setup_checkboxes()
        # self._setup_add_date_field()
        self._setup_layout()
        self._connect_signals()

        # # Timer for the date field
        # self.date_update_timer = QTimer(self)
        # self.date_update_timer.setInterval(1000)  # 1 second interval
        # self.date_update_timer.setSingleShot(True)
        # self.date_update_timer.timeout.connect(
        #     lambda: self.export_dialog.preview_panel.update_preview(
        #         self.include_start_pos_check.isChecked(),
        #         self.add_info_check.isChecked(),
        #         self.export_dialog.sequence,
        #         self.add_word_check.isChecked(),
        #         self.include_difficulty_level_check.isChecked(),
        #         self.add_beat_numbers_check.isChecked(),
        #     )
        # )

    def _setup_open_directory_checkbox(self):
        """Setup checkbox for opening file location after export."""
        self.open_directory_check = QCheckBox("Open file location after export", self)
        self.open_directory_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting(
                "open_directory_on_export"
            )
        )
        self.open_directory_check.toggled.connect(self.update_open_directory_setting)
        self.open_dir_layout = QHBoxLayout()
        self.open_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.open_dir_layout.addWidget(self.open_directory_check)

    def update_open_directory_setting(self):
        """Update setting for opening the directory after export."""
        self.settings_manager.image_export.set_image_export_setting(
            "open_directory_on_export", self.open_directory_check.isChecked()
        )

    def _connect_signals(self):
        """Connect signals to their respective slots."""

        self.include_start_pos_check.toggled.connect(
            self.export_dialog.update_export_setting_and_layout
        )
        self.user_combo_box.currentIndexChanged.connect(self._handle_user_selection)
        # self.add_date_field.textChanged.connect(self._on_date_field_text_changed)

    def _setup_checkboxes(self):
        """Setup the checkboxes for the control panel."""
        self.include_start_pos_check = QCheckBox("Add Start Position", self)
        self.include_start_pos_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting(
                "include_start_position"
            )
        )
        self.include_start_pos_check.toggled.connect(self.toggle_add_start_position)
        # set the cursor to pointing hand when hovering over the checkbox
        self.include_start_pos_check.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_info_check = QCheckBox("Add Info", self)
        self.add_info_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting("add_info")
        )
        self.add_info_check.toggled.connect(self.toggle_add_info)
        self.add_info_check.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_word_check = QCheckBox("Add Word to Image", self)
        self.add_word_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting("add_word")
        )
        self.add_word_check.toggled.connect(self.toggle_add_word)
        self.add_word_check.setCursor(Qt.CursorShape.PointingHandCursor)

        self.include_difficulty_level_check = QCheckBox(
            "Include Difficulty Level", self
        )
        self.include_difficulty_level_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting(
                "add_difficulty_level"
            )
        )
        self.include_difficulty_level_check.toggled.connect(
            self.toggle_include_difficulty_level
        )
        self.include_difficulty_level_check.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_beat_numbers_check = QCheckBox("Add Beat Numbers", self)
        self.add_beat_numbers_check.setChecked(
            self.settings_manager.image_export.get_image_export_setting(
                "add_beat_numbers"
            )
        )
        self.add_beat_numbers_check.toggled.connect(self.toggle_add_beat_numbers)
        self.add_beat_numbers_check.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_open_directory_checkbox()

    def _setup_layout(self):
        """Setup the layout of the control panel."""
        self.user_input_layout = QVBoxLayout()
        # Add a User Label
        user_label = QLabel("User:", self)
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_input_layout.addWidget(user_label)
        self.user_input_layout.addWidget(self.user_combo_box)
        # Add a Note Label
        notes_label = QLabel("Note:", self)
        notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_input_layout.addWidget(notes_label)
        self.user_input_layout.addWidget(self.notes_combo_box)
        # self.user_input_layout.addWidget(self.add_date_field, 1)

        self.options_checkbox_layout = QVBoxLayout()
        self.options_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.options_checkbox_layout.addWidget(self.include_start_pos_check)
        self.options_checkbox_layout.addWidget(self.add_info_check)
        self.options_checkbox_layout.addWidget(self.add_word_check)
        self.options_checkbox_layout.addWidget(self.include_difficulty_level_check)
        self.options_checkbox_layout.addWidget(self.add_beat_numbers_check)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addLayout(self.user_input_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.options_checkbox_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.open_dir_layout)
        self.layout.addStretch(1)

    # def _setup_add_date_field(self):
    #     """Setup the input field for the date."""
    #     self.add_date_field = QLineEdit(self)
    #     current_date = datetime.now().strftime("%m-%d-%Y")
    #     current_date = "-".join([str(int(part)) for part in current_date.split("-")])
    #     self.add_date_field.setText(current_date)
    #     self.add_date_field.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.add_date_field.setEnabled(False)  # Disable editing
    #     self.add_date_field.setStyleSheet("color: gray;")

    def _handle_user_selection(self):
        """Handle the selection of a user from the combo box."""
        selected_user = self.user_combo_box.currentText()
        if selected_user == "Edit Users":
            self.user_manager.previous_user = self.previous_user
            self.user_manager.open_edit_users_dialog()
            index = self.user_combo_box.findText(self.previous_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        else:
            self.previous_user = selected_user
            self.export_dialog.preview_panel.update_preview(
                self.include_start_pos_check.isChecked(),
                self.add_info_check.isChecked(),
                self.export_dialog.sequence,
                self.add_word_check.isChecked(),
                self.include_difficulty_level_check.isChecked(),
                self.add_beat_numbers_check.isChecked(),
            )

    def _handle_note_selection(self):
        """Handle the selection of a note from the combo box."""
        selected_note = self.notes_combo_box.currentText()
        if selected_note == "Edit Notes":
            self.notes_manager.previous_note = self.previous_note
            self.notes_manager.open_edit_notes_dialog()
            index = self.notes_combo_box.findText(self.previous_note)
            if index != -1:
                self.notes_combo_box.setCurrentIndex(index)
        else:
            self.previous_note = selected_note
            self.export_dialog.preview_panel.update_preview(
                self.include_start_pos_check.isChecked(),
                self.add_info_check.isChecked(),
                self.export_dialog.sequence,
                self.add_word_check.isChecked(),
                self.include_difficulty_level_check.isChecked(),
                self.add_beat_numbers_check.isChecked(),
            )

    def toggle_add_info(self):
        """Toggle the state of the additional info fields based on the checkbox."""
        state = self.add_info_check.isChecked()
        self.user_combo_box.setEnabled(state)
        self.notes_combo_box.setEnabled(state)
        color = "gray" if not state else ""
        self.user_combo_box.setStyleSheet(f"color: {color};")
        self.notes_combo_box.setStyleSheet(f"color: {color};")
        self.export_dialog.preview_panel.update_preview(
            self.include_start_pos_check.isChecked(),
            self.add_info_check.isChecked(),
            self.export_dialog.sequence,
            self.add_word_check.isChecked(),
            self.include_difficulty_level_check.isChecked(),
            self.add_beat_numbers_check.isChecked(),
        )
        self.settings_manager.image_export.set_image_export_setting("add_info", state)

    def toggle_add_word(self):
        """Toggle the state of the add word field based on the checkbox."""
        state = self.add_word_check.isChecked()
        self.settings_manager.image_export.set_image_export_setting("add_word", state)
        self.export_dialog.preview_panel.update_preview(
            self.include_start_pos_check.isChecked(),
            self.add_info_check.isChecked(),
            self.export_dialog.sequence,
            self.add_word_check.isChecked(),
            self.include_difficulty_level_check.isChecked(),
            self.add_beat_numbers_check.isChecked(),
        )

    def toggle_include_difficulty_level(self):
        """Toggle the state of the include difficulty level field based on the checkbox."""
        state = self.include_difficulty_level_check.isChecked()
        self.settings_manager.image_export.set_image_export_setting(
            "add_difficulty_level", state
        )
        self.export_dialog.preview_panel.update_preview(
            self.include_start_pos_check.isChecked(),
            self.add_info_check.isChecked(),
            self.export_dialog.sequence,
            self.add_word_check.isChecked(),
            self.include_difficulty_level_check.isChecked(),
            self.add_beat_numbers_check.isChecked(),
        )

    def toggle_add_beat_numbers(self):
        """Toggle the state of the add beat numbers field based on the checkbox."""
        state = self.add_beat_numbers_check.isChecked()
        self.settings_manager.image_export.set_image_export_setting(
            "add_beat_numbers", state
        )
        self.export_dialog.preview_panel.update_preview(
            self.include_start_pos_check.isChecked(),
            self.add_info_check.isChecked(),
            self.export_dialog.sequence,
            self.add_word_check.isChecked(),
            self.include_difficulty_level_check.isChecked(),
            self.add_beat_numbers_check.isChecked(),
        )

    def toggle_add_start_position(self):
        """Toggle the state of the add start position field based on the checkbox."""
        state = self.include_start_pos_check.isChecked()
        self.settings_manager.image_export.set_image_export_setting(
            "include_start_position", state
        )
        self.export_dialog.preview_panel.update_preview(
            self.include_start_pos_check.isChecked(),
            self.add_info_check.isChecked(),
            self.export_dialog.sequence,
            self.add_word_check.isChecked(),
            self.include_difficulty_level_check.isChecked(),
            self.add_beat_numbers_check.isChecked(),
        )
