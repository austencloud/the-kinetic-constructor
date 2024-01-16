from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from typing import TYPE_CHECKING, Union

from constants import CLOCKWISE, COUNTER_CLOCKWISE, DASH, STATIC
from utilities.TypeChecking.letter_lists import Type4_letters


from ...base_attr_box_widget import BaseAttrBoxWidget
from ...base_attr_box_widget import BaseAttrBoxWidget
from .turn_adjustment_manager import TurnAdjustmentManager
from .turn_direct_set_manager import TurnDirectSetManager
from .turn_display_manager import TurnDisplayManager

if TYPE_CHECKING:
    from ....color_attr_box import ColorAttrBox
    from ....motion_type_attr_box import MotionTypeAttrBox
    from ....lead_state_attr_box import LeadStateAttrBox


class BaseTurnsWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"
        ] = attr_box
        self.vbox_layout: QVBoxLayout = QVBoxLayout(self)
        self.turn_direct_set_manager = TurnDirectSetManager(self)
        self.turn_adjustment_manager = TurnAdjustmentManager(self.attr_box, self)
        self.turn_display_manager = TurnDisplayManager(self, self.attr_box)
        if hasattr(self.attr_box, "same_button"):
            self.same_button = self.attr_box.same_button
            self.opp_button = self.attr_box.opp_button
            self.same_opp_buttons = [self.same_button, self.opp_button]
            self.pictographs = self.attr_box.pictographs
        self.initialize_components()
        self.setup_ui()

    def initialize_components(self) -> None:
        """Initialize components here."""
        self.turns_label = None

    def setup_ui(self) -> None:
        self.turn_adjustment_manager.setup_adjustment_buttons()
        self.turn_display_manager.setup_display_components()
        self.turn_direct_set_manager.setup_direct_set_buttons()
        self._setup_prop_rot_dir_buttons()

    def _setup_prop_rot_dir_buttons(self):
        # Create CW and CCW buttons here and hide them initially
        self.cw_button = self.create_attr_box_button('cw_icon.png', self._set_cw)
        self.ccw_button = self.create_attr_box_button('ccw_icon.png', self._set_ccw)
        self.cw_button.hide()
        self.ccw_button.hide()

        # Add logic to determine when to show VTG buttons or CW/CCW buttons
        self._update_button_visibility()

    def _update_button_visibility(self):
        if self._should_show_cw_ccw_buttons():
            self.same_button.hide()
            self.opp_button.hide()
            self.cw_button.show()
            self.ccw_button.show()
        else:
            self.cw_button.hide()
            self.ccw_button.hide()
            self.same_button.show()
            self.opp_button.show()

    def _should_show_cw_ccw_buttons(self):
        # Logic to determine if the CW/CCW buttons should be shown
        # based on the current state of the motion's turns and the letter type.
        motion, other_motion = self._get_motion_pair()
        return (
            self.attr_box.motion_type in [DASH, STATIC] and
            motion.turns > 0 and other_motion.turns == 0 and
            self.attr_box.pictograph.letter in Type4_letters
        )

    def _set_cw(self):
        # Logic to set the current motion's prop rotation direction to clockwise
        motion, _ = self._get_motion_pair()
        motion.prop_rot_dir = CLOCKWISE
        self._update_button_visibility()

    def _set_ccw(self):
        # Logic to set the current motion's prop rotation direction to counter-clockwise
        motion, _ = self._get_motion_pair()
        motion.prop_rot_dir = COUNTER_CLOCKWISE
        self._update_button_visibility()

    def _get_motion_pair(self):
        # Retrieve the current motion and its corresponding other motion
        motion = self.attr_box.get_current_motion()
        other_motion = self.attr_box.get_other_motion(motion)
        return motion, other_motion

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        """Convert turn values from string to numeric."""
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    @staticmethod
    def create_frame(layout: QHBoxLayout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return frame

    def resize_turns_widget(self) -> None:
        self.turn_display_manager.update_turnbox_size()
        self.turn_display_manager.update_adjust_turns_button_size()
