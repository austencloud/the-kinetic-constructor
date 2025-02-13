from typing import TYPE_CHECKING
from .labeled_toggle_base import LabeledToggleBase

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab

class PermutationTypeToggle(LabeledToggleBase):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(
            generate_tab=generate_tab,
            left_text="Mirrored",
            right_text="Rotated",
        )

    def _handle_toggle_changed(self, state: bool):
        permutation_type = "rotated" if state else "mirrored"
        self.generate_tab.settings.set_setting("permutation_type", permutation_type)
        self.update_label_styles()
