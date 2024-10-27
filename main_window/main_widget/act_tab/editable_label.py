from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QWidget,
    QStackedLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QEvent

from main_window.main_widget.act_tab.editable_label_manager import EditableLabelManager


class EditableLabel(QWidget):
    def __init__(
        self,
        parent,
        label_text: str,
        align=Qt.AlignmentFlag.AlignLeft,
        padding=5,
        bg_color="#FFFFFF",
        multi_line=False,
    ):
        super().__init__(parent)

        self._align = align
        self._padding = padding
        self._bg_color = bg_color
        self.multi_line = multi_line

        self.label = self._create_label(label_text)
        self.edit = self._create_edit_widget()

        self.layout: QStackedLayout = self._configure_layout()
        self.apply_styles()

        self.label.mousePressEvent = self._show_edit
        self.edit.installEventFilter(self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def _create_label(self, text):
        """Initialize the label to display text."""
        label = QLabel(text, self)
        label.setAlignment(self._align)
        if self.multi_line:
            label.setWordWrap(True)
            label.setTextFormat(Qt.TextFormat.PlainText)
        return label

    def _create_edit_widget(self):
        """Initialize the editing widget (QLineEdit or QTextEdit)."""
        if self.multi_line:
            edit = QTextEdit(self)
            edit.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            edit = QLineEdit(self)
            edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return edit

    def _configure_layout(self):
        """Configure a stacked layout to switch between label and edit view."""
        layout = QStackedLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        return layout

    def apply_styles(self):
        """Apply styling to label and edit fields."""
        self.label.setStyleSheet("padding: 0px; margin: 0px;")
        self.edit.setStyleSheet(
            f"background-color: {self._bg_color}; padding: {self._padding}px; margin: 0px;"
        )
        self.edit.setAlignment(self._align)

    def _show_edit(self, event=None):
        """Switch from label to edit mode."""

        EditableLabelManager.set_active(self)  # Set this as the active edit

        if self.multi_line:
            self.edit.setPlainText(self.label.text())
        else:
            self.edit.setText(self.label.text())
        self.edit.setFont(self.label.font())
        self.layout.setCurrentWidget(self.edit)
        self.edit.setFocus()
        self.edit.selectAll()

    def _hide_edit(self):
        """Switch from edit mode back to label mode and save the text."""
        text = self.edit.toPlainText() if self.multi_line else self.edit.text()
        if self.multi_line:
            self.label.setTextFormat(Qt.TextFormat.PlainText)
            self.label.setWordWrap(True)
        self.label.setText(text or self.label.text())
        self.layout.setCurrentWidget(self.label)
        EditableLabelManager.clear_active()  # Clear the active edit when hiding

    def eventFilter(self, source, event):
        """Detect Enter key press in edit mode to exit edit mode."""
        if (
            source == self.edit
            and event.type() == QEvent.Type.KeyPress
            and event.key() == Qt.Key.Key_Return
            and (
                not self.multi_line
                or event.modifiers() == Qt.KeyboardModifier.NoModifier
            )
        ):
            self._hide_edit()
            return True
        return super().eventFilter(source, event)
