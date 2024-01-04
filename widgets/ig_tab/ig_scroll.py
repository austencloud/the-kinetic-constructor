from typing import TYPE_CHECKING, Dict, List, Union
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
    RED,
    RED_END_LOC,
    RED_END_ORI,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    START_POS,
    STATIC,
)
from widgets.ig_tab.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area import PictographScrollArea
from Enums import Letter, Orientation, Turns
from constants import IG_PICTOGRAPH
from utilities.TypeChecking.Letters import letters
from utilities.TypeChecking.TypeChecking import letters

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScrollArea(PictographScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(main_widget, ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab
        self.filters: Dict[str, Union[Turns, Orientation]] = {}
        self.pictographs: Dict[letters, IGPictograph] = {}

    def update_scroll_area_content(self) -> None:
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    def update_pictographs(self) -> None:
        ordered_pictographs = {}
        sorted_selected_letters = sorted(
            self.ig_tab.selected_letters, key=lambda x: letters.index(x)
        )
        deselected_letters = set(
            key.split("_")[0] for key in self.pictographs.keys()
        ) - set(sorted_selected_letters)
        for letter in deselected_letters:
            self.remove_deselected_letter_pictographs(letter)
        for letter in sorted_selected_letters:
            pictograph_dict_list = self.letters.get(letter, [])
            filtered_pictograph_dicts = self.filter_pictographs(pictograph_dict_list)
            for pictograph_dict in filtered_pictograph_dicts:
                pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
                ig_pictograph = self.pictographs.get(pictograph_key)
                if ig_pictograph is None:
                    ig_pictograph = self._create_pictograph(
                        pictograph_dict, IG_PICTOGRAPH
                    )
                    for motion_color in ("blue", "red"):
                        motion_type = pictograph_dict.get(f"{motion_color}_motion_type")
                        if motion_type:
                            turns_value = self.get_turns_from_attr_panel(motion_type)
                            if motion_type == DASH:
                                prop_rot_dir = self.get_dash_prop_rot_dir_from_attr_panel(
                                    motion_type
                                )
                                pictograph_dict[f"{motion_color}_prop_rot_dir"] = prop_rot_dir
                            elif motion_type == STATIC:
                                prop_rot_dir = self.get_static_prop_rot_dir_from_attr_panel(
                                    motion_type
                                )
                                pictograph_dict[f"{motion_color}_prop_rot_dir"] = prop_rot_dir
                            pictograph_dict[f"{motion_color}_turns"] = turns_value

                    ig_pictograph.update_pictograph(pictograph_dict)
                image_key = self.generate_image_name(ig_pictograph, letter)
                ordered_pictographs[image_key] = ig_pictograph
        for index, (key, ig_pictograph) in enumerate(ordered_pictographs.items()):
                self.add_pictograph_to_layout(ig_pictograph, index)
        for key, ig_pictograph in ordered_pictographs.items():
            self.pictographs[key] = ig_pictograph

        keys_to_remove = []
        for key in self.pictographs.keys():
            letter = key.split("_")[0]
            if letter not in sorted_selected_letters:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            ig_pictograph = self.pictographs.pop(key)
            self.layout.removeWidget(ig_pictograph.view)
            ig_pictograph.view.setParent(None)
            ig_pictograph.view.deleteLater()

        if self.pictographs:
            self.update_attr_panel()

    def get_dash_prop_rot_dir_from_attr_panel(self, motion_type):
        header_widget = self.ig_tab.attr_panel.dash_attr_box.header_widget
        if motion_type == DASH:
            if header_widget.cw_button.isChecked():
                return CLOCKWISE
            elif header_widget.ccw_button.isChecked():
                return COUNTER_CLOCKWISE
            else:
                return NO_ROT
        else:
            return NO_ROT
        
    def get_static_prop_rot_dir_from_attr_panel(self, motion_type):
        header_widget = self.ig_tab.attr_panel.static_attr_box.header_widget
        if motion_type == STATIC:
            if header_widget.cw_button.isChecked():
                return CLOCKWISE
            elif header_widget.ccw_button.isChecked():
                return COUNTER_CLOCKWISE
            else:
                return NO_ROT
        else:
            return NO_ROT
    
    def get_turns_from_attr_panel(self, motion_type):
        return self.ig_tab.attr_panel.get_turns_for_motion_type(motion_type)

    def remove_deselected_letter_pictographs(self, deselected_letter):
        keys_to_remove = [
            key for key in self.pictographs if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            ig_pictograph = self.pictographs.pop(key)
            self.layout.removeWidget(ig_pictograph.view)
            ig_pictograph.view.setParent(None)
            ig_pictograph.view.deleteLater()

    def generate_pictograph_key_from_dict(self, pictograph_dict):
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

    def generate_image_name(self, ig_pictograph: IGPictograph, letter: Letter) -> str:
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

    def clear_layout(self):
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.pictographs.clear()

    def generate_pictograph_key_from_motion(self, ig_pictograph: IGPictograph, letter):
        return (
            f"{letter}_"
            f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}_"
            f"{ig_pictograph.motions[BLUE].motion_type}→{ig_pictograph.motions[BLUE].end_loc}_"
            f"{ig_pictograph.motions[RED].motion_type}→{ig_pictograph.motions[RED].end_loc}"
        )

    def add_pictograph_to_layout(self, ig_pictograph: IGPictograph, index):
        row = index // self.COLUMN_COUNT
        col = index % self.COLUMN_COUNT
        self.layout.addWidget(ig_pictograph.view, row, col)
        ig_pictograph.view.resize_for_scroll_area()

    def update_attr_panel(self) -> None:
        first_pictograph = next(iter(self.pictographs.values()), None)
        for motion in first_pictograph.motions.values():
            for attr_box in self.ig_tab.attr_panel.boxes:
                if motion.motion_type == attr_box.motion_type:
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

    def update_existing_pictographs(self):
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

    def resize_ig_scroll_area(self) -> None:
        self.setMinimumWidth(self.ig_tab.attr_panel.width())
