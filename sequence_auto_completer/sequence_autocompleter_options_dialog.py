from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QComboBox,
)


class SequenceAutocompleterOptionsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sequence Options")

        # Layout and widgets
        layout = QVBoxLayout()

        # Option to specify hand for each beat
        self.hand_options = []
        for i in range(8):  # Assuming 8 beats for demonstration
            layout.addWidget(QLabel(f"Beat {i+1} Hand:"))
            hand_option = QComboBox()
            hand_option.addItems(["Both", "Blue", "Red"])
            self.hand_options.append(hand_option)
            layout.addWidget(hand_option)

        # Dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_hand_options(self):
        return [option.currentText() for option in self.hand_options]
