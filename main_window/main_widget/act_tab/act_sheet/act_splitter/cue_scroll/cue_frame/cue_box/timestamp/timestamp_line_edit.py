from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QKeyEvent
from PyQt6.QtWidgets import QLineEdit


class TimestampLineEdit(QLineEdit):
    def __init__(self, initial_text="0:00"):
        super().__init__(initial_text)

        # Define regular expression for validation (X:XX or XX:XX)
        timestamp_regex = QRegularExpression(r"^\d:\d{2}$|^\d{2}:\d{2}$")
        timestamp_validator = QRegularExpressionValidator(timestamp_regex)

        # Apply the validator to restrict input to valid timestamp format
        self.setValidator(timestamp_validator)
        self.setMaxLength(4)  # Restrict to "X:XX" or "XX:XX" format

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events to auto-format input as a timestamp."""
        key = event.key()

        # Allow Backspace and Delete keys without formatting
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            super().keyPressEvent(event)
            return

        # Only allow numeric input for formatting
        if event.text().isdigit():
            current_text = self.text().replace(":", "")  # Remove any existing colon
            new_text = current_text + event.text()  # Append the new digit

            # Format the text based on the number of digits
            if len(new_text) == 1:
                self.setText(new_text + ":")
            elif len(new_text) == 2:
                self.setText(new_text[0] + ":" + new_text[1])
            elif len(new_text) == 3:
                self.setText(new_text[0] + ":" + new_text[1:])

            # Move cursor to the end
            self.setCursorPosition(len(self.text()))

        # Prevent pressing Enter unless the format is complete (X:XX or XX:XX)
        if key == Qt.Key.Key_Return and not self._is_complete_format():
            return  # Prevent Enter action if format is incomplete

        # Accept the event to prevent further handling
        event.accept()

    def _is_complete_format(self):
        """Check if the current text matches the required X:XX or XX:XX format."""
        current_text = self.text()
        return len(current_text) == 4 and current_text[1] == ":"  # Match X:XX or XX:XX
