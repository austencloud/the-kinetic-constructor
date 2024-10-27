# editable_label.py
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


class EditableLabel(QWidget):
    def __init__(
        self,
        parent,
        label_text: str,
        align=Qt.AlignmentFlag.AlignLeft,
        padding=5,
        bg_color="#FFFFFF",
        multi_line=False,  # Control single or multi-line
    ):
        super().__init__(parent)
        self._align = align
        self._padding = padding
        self._bg_color = bg_color
        self.multi_line = multi_line

        self.label = QLabel(label_text, self)
        if self.multi_line:
            self.edit = QTextEdit(self)
            self.edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.edit.setMinimumHeight(0)
            self.edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.edit.setFrameShape(QFrame.Shape.NoFrame)

            # Enable word wrap and set text format
            self.label.setWordWrap(True)
            self.label.setTextFormat(Qt.TextFormat.PlainText)
        else:
            self.edit = QLineEdit(self)
            self.edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.edit.setMinimumHeight(0)
            self.edit.setFrame(False)

        # Configure layout for stacked editing
        self.layout: QStackedLayout = QStackedLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

        # Apply initial styles and alignment
        self.apply_styles()
        self.setLayout(self.layout)
        self.label.mousePressEvent = self._show_edit  # Edit on click

        # Install event filter on edit to detect Enter key
        self.edit.installEventFilter(self)

        # Set size policies
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def eventFilter(self, source, event):
        """Detect Enter key press in edit to exit edit mode."""
        if (
            source == self.edit
            and event.type() == QEvent.Type.KeyPress
            and event.key() == Qt.Key.Key_Return
            and (
                not self.multi_line
                or (self.multi_line and event.modifiers() == Qt.KeyboardModifier.NoModifier)
            )
        ):
            self._hide_edit()
            return True
        return super().eventFilter(source, event)

    def apply_styles(self):
        """Applies alignment, padding, and color styling to label and edit fields."""
        self.label.setAlignment(self._align)
        self.edit.setAlignment(self._align)
        self.label.setStyleSheet(f"padding: 0px; margin: 0px;")
        self.edit.setStyleSheet(
            f"background-color: {self._bg_color}; padding: {self._padding}px; margin: 0px;"
        )

    def _show_edit(self, event=None):
        """Switch to the edit mode."""
        if self.multi_line:
            self.edit.setPlainText(self.label.text())
        else:
            self.edit.setText(self.label.text())
        self.edit.setFont(self.label.font())
        self.layout.setCurrentWidget(self.edit)
        self.edit.setFocus()
        self.edit.selectAll()

    def _hide_edit(self):
        """Switch back to the label mode."""
        if self.multi_line:
            text = self.edit.toPlainText()
            # Ensure the label uses plain text format and preserves line breaks
            self.label.setTextFormat(Qt.TextFormat.PlainText)
            self.label.setWordWrap(True)
        else:
            text = self.edit.text()
        self.label.setText(text or self.label.text())
        self.layout.setCurrentWidget(self.label)

