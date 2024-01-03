from typing import TYPE_CHECKING, Dict, List, Union
from constants import (
    BLUE,
    BLUE_END_LOC,
    BLUE_END_ORI,
    BLUE_MOTION_TYPE,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    END_POS,
    LETTER,
    RED,
    RED_END_ORI,
    RED_START_ORI,
    RED_TURNS,
    START_POS,
)
from widgets.ig_tab.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area import PictographScrollArea
from Enums import Letter, Orientation, PictographAttributesDict, Turns
from constants import IG_PICTOGRAPH
from utilities.TypeChecking.Letters import letters

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScrollArea(PictographScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(main_widget, ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab
        self.filters: Dict[str, Union[Turns, Orientation]] = {}
        self.pictographs: Dict[Letter, IGPictograph] = {}

    def update_scroll_area_content(self) -> None:
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    def update_pictographs(self) -> None:
        # Clear existing widgets but keep a reference to the existing pictographs
        existing_pictographs = {
            self.generate_image_name(p, p.letter): p for p in self.pictographs.values()
        }
        self.clear_layout()
        index = 0
        for letter in self.ig_tab.selected_letters:
            pictograph_dict_list = self.letters.get(letter, [])
            filtered_pictograph_dicts = self.filter_pictographs(pictograph_dict_list)
            for pictograph_dict in filtered_pictograph_dicts:
                pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
                ig_pictograph = existing_pictographs.get(pictograph_key)
                if ig_pictograph is None:
                    ig_pictograph = self._create_pictograph(
                        pictograph_dict, IG_PICTOGRAPH
                    )
                    ig_pictograph.update_pictograph(pictograph_dict)
                self.apply_filters_to_pictograph(ig_pictograph)
                image_key = self.generate_image_name(ig_pictograph, letter)
                self.add_pictograph_to_layout(ig_pictograph, index)
                self.pictographs[image_key] = ig_pictograph
                index += 1
        if self.pictographs:
            self.update_attr_panel()

    def generate_pictograph_key_from_dict(self, pictograph_dict):
        # Create a unique key for the pictograph using its dictionary representation
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[BLUE_TURNS]}_"
        )

    def apply_filters_to_pictograph(self, ig_pictograph: IGPictograph) -> None:
        for color, motion in ig_pictograph.motions.items():
            for attr, value in self.filters.items():
                if attr.startswith(color):
                    # Set the motion attribute if it's in the filters
                    setattr(motion, attr.replace(f"{color}_", ""), value)
            # Update the motion to apply changes
            motion.update_motion()

    def clear_layout(self):
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.pictographs.clear()

    def get_or_create_pictograph(self, existing_pictographs, pictograph_dict):
        image_key = self.generate_pictograph_key(pictograph_dict)
        ig_pictograph = existing_pictographs.get(image_key)
        if ig_pictograph is None:
            ig_pictograph = self._create_pictograph(pictograph_dict, IG_PICTOGRAPH)
            ig_pictograph.update_pictograph(pictograph_dict)
        return ig_pictograph

    def generate_image_name(self, ig_pictograph: IGPictograph, letter: Letter) -> str:
        # This function should exactly match the structure of the keys
        # you have provided, using the motion attributes after they have been set
        start_to_end_string = f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}"
        blue_turns = ig_pictograph.motions[BLUE].turns
        red_turns = ig_pictograph.motions[RED].turns
        blue_end_ori = ig_pictograph.motions[BLUE].end_ori
        red_end_ori = ig_pictograph.motions[RED].end_ori

        return (
            f"{letter}_"
            f"({start_to_end_string})_"
            f"({ig_pictograph.motions[BLUE].motion_type}_"
            f"{ig_pictograph.motions[BLUE].start_loc}→{ig_pictograph.motions[BLUE].end_loc}_"
            f"{blue_turns}_"
            f"{ig_pictograph.motions[BLUE].start_ori}→{blue_end_ori})_"
            f"({ig_pictograph.motions[RED].motion_type}_"
            f"{ig_pictograph.motions[RED].start_loc}→{ig_pictograph.motions[RED].end_loc}_"
            f"{red_turns}_"
            f"{ig_pictograph.motions[RED].start_ori}→{red_end_ori})_"
            f"{self.main_widget.prop_type}"
        )

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
        self.setMaximumWidth(
            self.main_widget.width()
            - self.main_widget.sequence_widget.width()
            - self.ig_tab.letter_button_frame.width()
        )
