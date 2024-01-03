from typing import TYPE_CHECKING, Dict, List, Union
from constants import (
    BLUE,
    BLUE_END_ORI,
    BLUE_START_ORI,
    BLUE_TURNS,
    END_POS,
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
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        index = 0
        for letter in letters:
            if letter in self.ig_tab.selected_letters:
                pictograph_dict_list = self.letters.get(letter, [])
                filtered_pictograph_dicts = self.filter_pictographs(
                    pictograph_dict_list
                )
                for pictograph_dict in filtered_pictograph_dicts:
                    ig_pictograph: IGPictograph = self._create_pictograph(
                        pictograph_dict, IG_PICTOGRAPH
                    )
                    row = index // self.COLUMN_COUNT
                    col = index % self.COLUMN_COUNT
                    self.layout.addWidget(ig_pictograph.view, row, col)
                    start_to_end_string = (
                        f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}"
                    )
                    blue_turns = ig_pictograph.motions[BLUE].turns
                    red_turns = ig_pictograph.motions[RED].turns
                    blue_end_ori = ig_pictograph.motions[BLUE].end_ori
                    red_end_ori = ig_pictograph.motions[RED].end_ori

                    image_name = (
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
                    self.pictographs[image_name] = ig_pictograph
                    ig_pictograph.view.resize_for_scroll_area()
                    index += 1
        self.update_attr_panel()

    def update_attr_panel(self) -> None:
        first_pictograph = next(iter(self.pictographs.values()), None)
        for motion in first_pictograph.motions.values():
            self.ig_tab.attr_panel.update_attr_panel(motion)

    def filter_pictographs(self, pictograph_dicts: List[Dict]) -> List[Dict]:
        return [
            pictograph_dict
            for pictograph_dict in pictograph_dicts
            if self.pictograph_matches_filters(pictograph_dict)
        ]

    def pictograph_matches_filters(
        self, pictograph_dict: PictographAttributesDict
    ) -> bool:
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
