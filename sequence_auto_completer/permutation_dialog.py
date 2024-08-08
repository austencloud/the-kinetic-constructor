from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton


class PermutationDialog(QDialog):
    def __init__(self, valid_permutations: dict):
        super().__init__()
        self.setWindowTitle("Select Permutation Type")

        self.rotation_button = QPushButton("Rotational Permutation")
        self.mirror_button = QPushButton("Mirrored Permutation")
        self.color_swap_button = QPushButton("Color Swap (for Mirrored)")

        self.rotation_button.setFixedSize(200, 50)
        self.mirror_button.setFixedSize(200, 50)
        self.color_swap_button.setFixedSize(200, 50)

        self.rotation_button.clicked.connect(self.return_rotation_option)
        self.mirror_button.clicked.connect(self.return_mirror_option)
        self.color_swap_button.clicked.connect(self.return_color_swap_option)

        layout = QVBoxLayout()
        layout.addWidget(self.rotation_button)
        layout.addWidget(self.mirror_button)
        layout.addWidget(self.color_swap_button)

        self.setLayout(layout)

        self.selected_option = None
        self.set_button_states(valid_permutations)

    def set_button_states(self, valid_permutations: dict):
        self.rotation_button.setEnabled(valid_permutations.get("rotation", False))
        self.mirror_button.setEnabled(valid_permutations.get("mirror", False))
        self.color_swap_button.setEnabled(valid_permutations.get("color_swap", False))

    def return_rotation_option(self):
        self.selected_option = "rotation"
        self.accept()

    def return_mirror_option(self):
        self.selected_option = "mirror"
        self.accept()

    def return_color_swap_option(self):
        self.selected_option = "color_swap"
        self.accept()

    def get_options(self):
        return self.selected_option
