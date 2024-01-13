from typing import TYPE_CHECKING, Dict, List, Literal, Set, Union
from constants import (
    BLUE,
    BLUE_END_LOC,
    BLUE_END_ORI,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    END_POS,
    LETTER,
    NO_ROT,
    OPP,
    RED,
    RED_END_LOC,
    RED_END_ORI,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    SAME,
    START_POS,
    STATIC,
)
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area import PictographScrollArea
from constants import IG_PICTOGRAPH
from utilities.TypeChecking.TypeChecking import (
    Letters,
    Turns,
    Orientations,
    VtgDirections,
)
from PyQt6.QtCore import QTimer

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScrollArea(PictographScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(main_widget, ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab
        self.filters: Dict[str, Union[Turns, Orientations]] = {}
        self.pictographs: Dict[Letters, IGPictograph] = {}

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_pictographs_positions)
        self.update_timer.start(300)

    def update_pictographs_positions(self) -> None:
        """Method to update positions of all pictographs"""
        for pictograph in self.pictographs.values():
            self.update_individual_pictograph_position(pictograph)

    def update_individual_pictograph_position(self, pictograph: IGPictograph) -> None:
        if hasattr(pictograph, "arrow_placement_manager"):
            pictograph.arrow_placement_manager.update_arrow_placement()

    def reset_turns(self) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                motion.turns = 0
                motion.update_motion()
            pictograph.update_pictograph()

    def update_pictographs(self) -> None:
        self.remove_deselected_pictographs()
        self.process_selected_letters()
        self.order_and_display_pictographs()
        self.cleanup_unused_pictographs()
        self.update_attr_panel_if_needed()

    def remove_deselected_pictographs(self) -> None:
        deselected_letters = self.get_deselected_letters()
        for letter in deselected_letters:
            self.remove_deselected_letter_pictographs(letter)

    def get_deselected_letters(self) -> Set[Letters]:
        selected_letters = set(self.ig_tab.selected_letters)
        existing_letters = {key.split("_")[0] for key in self.pictographs.keys()}
        return existing_letters - selected_letters

    def process_selected_letters(self) -> None:
        sorted_selected_letters = self.get_sorted_selected_letters()
        for letter in sorted_selected_letters:
            self.process_letter(letter)

    def get_sorted_selected_letters(self) -> List[Letters]:
        return sorted(self.ig_tab.selected_letters, key=lambda x: Letters.index(x))

    def process_letter(self, letter) -> None:
        pictograph_dicts = self.letters.get(letter, [])
        for pictograph_dict in self.filter_pictographs(pictograph_dicts):
            self.create_or_update_pictograph(pictograph_dict, letter)

    def create_or_update_pictograph(self, pictograph_dict, letter) -> None:
        pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
        ig_pictograph = self.pictographs.get(
            pictograph_key, self._create_pictograph(IG_PICTOGRAPH)
        )
        self.pictographs[pictograph_key] = ig_pictograph
        self.update_pictograph_motions(ig_pictograph, pictograph_dict)
        ig_pictograph.update_pictograph(pictograph_dict)

    def update_pictograph_motions(self, ig_pictograph, pictograph_dict) -> None:
        for motion_color in (BLUE, RED):
            motion_type = pictograph_dict.get(f"{motion_color}_motion_type")
            if motion_type:
                turns_value = self.get_turns_from_attr_panel(motion_type)
                vtg_dir = self.get_vtg_dir_from_attr_panel()
                pictograph_dict[f"{motion_color}_turns"] = turns_value
                # pictograph_dict[f"{motion_color}_prop_rot_dir"] = vtg_dir

    def order_and_display_pictographs(self) -> None:
        ordered_pictographs = self.get_ordered_pictographs()
        for index, (key, ig_pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(ig_pictograph, index)
        self.pictographs.update(ordered_pictographs)

    def cleanup_unused_pictographs(self) -> None:
        keys_to_remove = self.get_keys_to_remove()
        for key in keys_to_remove:
            self.remove_pictograph(key)

    def get_keys_to_remove(self) -> List[str]:
        selected_letters = {
            letter.split("_")[0] for letter in self.ig_tab.selected_letters
        }
        return [
            key for key in self.pictographs if key.split("_")[0] not in selected_letters
        ]

    def get_ordered_pictographs(self) -> Dict[Letters, IGPictograph]:
        # Assuming you want to order by the letter's index and then by start position
        return {
            k: v
            for k, v in sorted(
                self.pictographs.items(),
                key=lambda item: (Letters.index(item[1].letter), item[1].start_pos),
            )
        }

    def get_vtg_dir_from_attr_panel(self) -> VtgDirections:
        header_widget = (
            self.ig_tab.filter_tab.motion_attr_panel.dash_attr_box.header_widget
        )
        if header_widget.same_button.isChecked():
            return SAME
        elif header_widget.opp_button.isChecked():
            return OPP

    def remove_pictograph(self, key) -> None:
        ig_pictograph = self.pictographs.pop(key)
        self.layout.removeWidget(ig_pictograph.view)
        ig_pictograph.view.setParent(None)
        ig_pictograph.view.deleteLater()

    def update_attr_panel_if_needed(self) -> None:
        if self.pictographs:
            self.update_attr_panel()

    def get_dash_prop_rot_dir_from_attr_panel(
        self, motion_type
    ) -> Literal["cw", "ccw", "no_rot"]:
        header_widget = (
            self.ig_tab.filter_tab.motion_attr_panel.dash_attr_box.header_widget
        )
        if motion_type == DASH:
            if header_widget.same_button.isChecked():
                return CLOCKWISE
            elif header_widget.opp_button.isChecked():
                return COUNTER_CLOCKWISE
            else:
                return NO_ROT
        else:
            return NO_ROT

    def get_static_prop_rot_dir_from_attr_panel(
        self, motion_type
    ) -> Literal["cw", "ccw", "no_rot"]:
        header_widget = (
            self.ig_tab.filter_tab.motion_attr_panel.static_attr_box.header_widget
        )
        if motion_type == STATIC:
            if header_widget.same_button.isChecked():
                return CLOCKWISE
            elif header_widget.opp_button.isChecked():
                return COUNTER_CLOCKWISE
            else:
                return NO_ROT
        else:
            return NO_ROT

    def get_turns_from_attr_panel(self, motion_type) -> Turns:
        return self.ig_tab.filter_tab.motion_attr_panel.get_turns_for_motion_type(
            motion_type
        )

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key for key in self.pictographs if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            ig_pictograph = self.pictographs.pop(key)
            self.layout.removeWidget(ig_pictograph.view)
            ig_pictograph.view.setParent(None)
            ig_pictograph.view.deleteLater()

    def generate_pictograph_key_from_dict(self, pictograph_dict) -> str:
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
        )

    def generate_image_name(self, ig_pictograph: IGPictograph, letter: Letters) -> str:
        return (
            f"{letter}_"
            f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}_"
            f"{ig_pictograph.motions[BLUE].motion_type}_"
            f"{ig_pictograph.motions[BLUE].prop_rot_dir}_"
            f"{ig_pictograph.motions[BLUE].start_loc}→{ig_pictograph.motions[BLUE].end_loc}_"
            f"{ig_pictograph.motions[RED].motion_type}_"
            f"{ig_pictograph.motions[RED].prop_rot_dir}_"
            f"{ig_pictograph.motions[RED].start_loc}→{ig_pictograph.motions[RED].end_loc}"
        )

    def apply_filters_to_pictograph(self, ig_pictograph: IGPictograph) -> None:
        for color, motion in ig_pictograph.motions.items():
            for attr, value in self.filters.items():
                if attr.startswith(color):
                    setattr(motion, attr.replace(f"{color}_", ""), value)
            motion.update_motion()

    def clear_layout(self) -> None:
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.pictographs.clear()

    def generate_pictograph_key_from_motion(
        self, ig_pictograph: IGPictograph, letter
    ) -> str:
        return (
            f"{letter}_"
            f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}_"
            f"{ig_pictograph.motions[BLUE].motion_type}→{ig_pictograph.motions[BLUE].end_loc}_"
            f"{ig_pictograph.motions[RED].motion_type}→{ig_pictograph.motions[RED].end_loc}"
        )

    def add_pictograph_to_layout(self, ig_pictograph: IGPictograph, index) -> None:
        row = index // self.COLUMN_COUNT
        col = index % self.COLUMN_COUNT
        self.layout.addWidget(ig_pictograph.view, row, col)
        ig_pictograph.view.resize_for_scroll_area()

    def update_attr_panel(self) -> None:
        first_pictograph = next(iter(self.pictographs.values()), None)
        for motion in first_pictograph.motions.values():
            if self.ig_tab.filter_tab.motion_attr_panel.isVisible():
                for attr_box in self.ig_tab.filter_tab.motion_attr_panel.boxes:
                    if motion.motion_type == attr_box.motion_type:
                        attr_box.update_attr_box(motion)
            elif self.ig_tab.filter_tab.color_attr_panel.isVisible():
                for attr_box in self.ig_tab.filter_tab.color_attr_panel.boxes:
                    if motion.motion_type == attr_box.color:
                        attr_box.update_attr_box(motion)

    def filter_pictographs(self, pictograph_dicts: List[Dict]) -> List[Dict]:
        return [
            pictograph_dict
            for pictograph_dict in pictograph_dicts
            if self.pictograph_matches_filters(pictograph_dict)
        ]

    def pictograph_matches_filters(self, pictograph_dict: Dict) -> bool:
        for filter_key, filter_value in self.filters.items():
            if filter_value in ["0", "1", "2", "3"]:
                filter_value = int(filter_value)
            elif filter_value in ["0.5", "1.5", "2.5"]:
                filter_value = float(filter_value)
            if filter_value != "":
                if pictograph_dict.get(filter_key) != filter_value:
                    return False
        return True

    def update_existing_pictographs(self) -> None:
        for letter, ig_pictograph in self.pictographs.items():
            if BLUE_TURNS in self.filters:
                update = {BLUE_TURNS: self.filters[BLUE_TURNS]}
                blue_motion = ig_pictograph.motions[BLUE]
                blue_motion.turns = (
                    float(self.filters[BLUE_TURNS])
                    if "." in self.filters[BLUE_TURNS]
                    else int(self.filters[BLUE_TURNS])
                )
                blue_motion.update_motion(update)
            elif BLUE_START_ORI in self.filters:
                update = {BLUE_START_ORI: self.filters[BLUE_START_ORI]}
                ig_pictograph.motions[BLUE].update_motion(update)
            elif BLUE_END_ORI in self.filters:
                ig_pictograph.motions[BLUE].end_ori = self.filters[BLUE_END_ORI]
                start_ori = ig_pictograph.motions[BLUE].get_start_ori_from_end_ori()
                update = {BLUE_START_ORI: start_ori}
                ig_pictograph.motions[BLUE].update_motion(update)
            if RED_TURNS in self.filters:
                update = {RED_TURNS: self.filters[RED_TURNS]}
                red_motion = ig_pictograph.motions[RED]
                red_motion.turns = (
                    float(self.filters[RED_TURNS])
                    if "." in self.filters[RED_TURNS]
                    else int(self.filters[RED_TURNS])
                )
                red_motion.update_motion(update)
            elif RED_START_ORI in self.filters:
                update = {RED_START_ORI: self.filters[RED_START_ORI]}
                ig_pictograph.motions[RED].update_motion(update)
            elif RED_END_ORI in self.filters:
                ig_pictograph.motions[RED].end_ori = self.filters[RED_END_ORI]
                start_ori = ig_pictograph.motions[RED].get_start_ori_from_end_ori()
                update = {RED_START_ORI: start_ori}
                ig_pictograph.motions[RED].update_motion(update)

            ig_pictograph.update_pictograph()
