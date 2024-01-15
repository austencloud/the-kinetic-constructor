from typing import TYPE_CHECKING, Dict, List, Literal, Union, Set
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from constants import (
    IG_PICTOGRAPH,
    OPTION,
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
    MOTION_TYPE,
    NO_ROT,
    OPP,
    PROP_ROT_DIR,
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
    TURNS,
)
from utilities.TypeChecking.Letters import Letters_list
from utilities.TypeChecking.TypeChecking import (
    Orientations,
    Turns,
    Letters,
    VtgDirections,
)
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from widgets.pictograph_scroll_area.scroll_area_display_manager import (
    ScrollAreaDisplayManager,
)
from widgets.pictograph_scroll_area.scroll_area_filter_manager import (
    ScrollAreaFilterFrameManager,
)
from widgets.pictograph_scroll_area.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget
    from widgets.filter_frame.attr_box.color_attr_box import ColorAttrBox
    from widgets.filter_frame.attr_box.lead_state_attr_box import LeadStateAttrBox
    from widgets.filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox


class PictographScrollArea(QScrollArea):
    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters: Dict[Letters, List[Dict[str, str]]] = self.main_widget.letters
        self.pictographs: Dict[Letters, Union["IGPictograph", "Option"]] = {}
        
        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterFrameManager(self)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QGridLayout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.order_and_display_pictographs()
        self.display_manager.cleanup_unused_pictographs()
        self.filter_frame_manager.update_filter_frame_if_needed()


# class PictographScrollArea(QScrollArea):
#     COLUMN_COUNT = 6
#     SPACING = 10

#     def __init__(
#         self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
#     ) -> None:
#         super().__init__(parent_tab)
#         self.main_widget = main_widget
#         self.parent_tab = parent_tab
#         self.letters: Dict[Letters, List[Dict[str, str]]] = self.main_widget.letters
#         self.pictographs: Dict[Letters, Union["IGPictograph", "Option"]] = {}

#         self.main_widget = main_widget
#         self.parent_tab = parent_tab
#         self.filters: Dict[str, Union[Turns, Orientations]] = {}

#         self.update_timer = QTimer(self)
#         self.update_timer.timeout.connect(self.update_pictographs_positions)
#         self.update_timer.start(300)
#         self._setup_ui()

#     def update_pictographs_positions(self) -> None:
#         """Method to update positions of all pictographs"""
#         for pictograph in self.pictographs.values():
#             self.update_individual_pictograph_position(pictograph)

#     def update_individual_pictograph_position(self, pictograph: IGPictograph) -> None:
#         if hasattr(pictograph, "arrow_placement_manager"):
#             pictograph.arrow_placement_manager.update_arrow_placement()

#     def update_pictographs(self) -> None:
#         self.remove_deselected_pictographs()
#         self.process_selected_letters()
#         self.order_and_display_pictographs()
#         self.cleanup_unused_pictographs()
#         self.update_attr_panel_if_needed()

#     def remove_deselected_pictographs(self) -> None:
#         deselected_letters = self.get_deselected_letters()
#         for letter in deselected_letters:
#             self.remove_deselected_letter_pictographs(letter)

#     def get_deselected_letters(self) -> Set[Letters]:
#         selected_letters = set(self.parent_tab.selected_letters)
#         existing_letters = {key.split("_")[0] for key in self.pictographs.keys()}
#         return existing_letters - selected_letters

#     def process_selected_letters(self) -> None:
#         sorted_selected_letters = self.get_sorted_selected_letters()
#         for letter in sorted_selected_letters:
#             self.process_letter(letter)

#     def get_sorted_selected_letters(self) -> List[Letters]:
#         return sorted(
#             self.parent_tab.selected_letters, key=lambda x: Letters_list.index(x)
#         )

#     def process_letter(self, letter) -> None:
#         pictograph_dicts = self.letters.get(letter, [])
#         for pictograph_dict in self.filter_pictographs(pictograph_dicts):
#             self.create_or_update_pictograph(pictograph_dict.copy(), letter)

#     def create_or_update_pictograph(self, pictograph_dict, letter) -> None:
#         pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
#         ig_pictograph = self.get_or_create_pictograph(pictograph_key)
#         self.update_pictograph_from_attr_panel(ig_pictograph, pictograph_dict)
#         ig_pictograph.update_pictograph(pictograph_dict)

#     def get_or_create_pictograph(self, pictograph_key) -> IGPictograph:
#         if pictograph_key not in self.pictographs:
#             self.pictographs[pictograph_key] = self._create_pictograph(IG_PICTOGRAPH)
#         return self.pictographs[pictograph_key]

#     def update_pictograph_from_attr_panel(
#         self, ig_pictograph: Pictograph, pictograph_dict
#     ) -> None:
#         for motion in ig_pictograph.motions.values():
#             self.update_motion_attributes_from_boxes(motion, pictograph_dict)

#     def update_motion_attributes_from_boxes(
#         self, motion: Motion, pictograph_dict: Dict
#     ) -> None:
#         for box in self.parent_tab.filter_tab.motion_type_attr_panel.boxes:
#             if (
#                 box.attribute_type == MOTION_TYPE
#                 and box.motion_type
#                 == pictograph_dict.get(f"{motion.color}_{MOTION_TYPE}")
#             ):
#                 self.set_motion_attributes_from_box(box, motion, pictograph_dict)

#     def set_motion_attributes_from_box(
#         self,
#         box: Union["ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"],
#         motion,
#         pictograph_dict,
#     ) -> None:
#         box_text = box.turns_widget.turn_display_manager.turns_display.text()
#         turns = float(box_text) if "." in box_text else int(box_text)

#         if box.motion_type in [DASH, STATIC]:
#             self.set_motion_turns_and_direction(box, motion, pictograph_dict, turns)

#     def set_motion_turns_and_direction(
#         self,
#         box: Union["ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"],
#         motion: Motion,
#         pictograph_dict,
#         turns,
#     ) -> None:
#         if box.vtg_dir_btn_state[SAME]:
#             self.set_same_direction_turns(box, motion, pictograph_dict, turns)
#         elif box.vtg_dir_btn_state[OPP]:
#             self.set_opposite_direction_turns(box, motion, pictograph_dict, turns)

#         if turns == 0 and pictograph_dict[motion.color + "_" + MOTION_TYPE] in [
#             DASH,
#             STATIC,
#         ]:
#             pictograph_dict[motion.color + "_" + PROP_ROT_DIR] = NO_ROT

#     def set_same_direction_turns(
#         self,
#         box: Union["ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"],
#         motion: Motion,
#         pictograph_dict,
#         turns,
#     ) -> None:
#         other_color = RED if motion.color == BLUE else BLUE
#         if pictograph_dict[motion.color + "_" + MOTION_TYPE] == box.motion_type:
#             pictograph_dict[motion.color + "_" + PROP_ROT_DIR] = pictograph_dict[
#                 other_color + "_" + PROP_ROT_DIR
#             ]
#             pictograph_dict[motion.color + "_" + TURNS] = turns

#     def set_opposite_direction_turns(
#         self,
#         box: Union["ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"],
#         motion: Motion,
#         pictograph_dict,
#         turns,
#     ) -> None:
#         other_color = RED if motion.color == BLUE else BLUE
#         opposite_dir = (
#             COUNTER_CLOCKWISE
#             if pictograph_dict[other_color + "_" + PROP_ROT_DIR] == CLOCKWISE
#             else CLOCKWISE
#         )
#         if pictograph_dict[motion.color + "_" + MOTION_TYPE] == box.motion_type:
#             pictograph_dict[motion.color + "_" + PROP_ROT_DIR] = opposite_dir
#             pictograph_dict[motion.color + "_" + TURNS] = turns

#     def order_and_display_pictographs(self) -> None:
#         ordered_pictographs = self.get_ordered_pictographs()
#         for index, (key, ig_pictograph) in enumerate(ordered_pictographs.items()):
#             self.add_pictograph_to_layout(ig_pictograph, index)
#         self.pictographs.update(ordered_pictographs)

#     def cleanup_unused_pictographs(self) -> None:
#         keys_to_remove = self.get_keys_to_remove()
#         for key in keys_to_remove:
#             self.remove_pictograph(key)

#     def get_keys_to_remove(self) -> List[str]:
#         selected_letters = {
#             letter.split("_")[0] for letter in self.parent_tab.selected_letters
#         }
#         return [
#             key for key in self.pictographs if key.split("_")[0] not in selected_letters
#         ]

#     def get_ordered_pictographs(self) -> Dict[Letters, IGPictograph]:
#         return {
#             k: v
#             for k, v in sorted(
#                 self.pictographs.items(),
#                 key=lambda item: (
#                     Letters_list.index(item[1].letter),
#                     item[1].start_pos,
#                 ),
#             )
#         }

#     def get_vtg_dir_from_attr_panel(self) -> VtgDirections:
#         header_widget = (
#             self.parent_tab.filter_tab.motion_type_attr_panel.dash_attr_box.header_widget
#         )
#         if header_widget.same_button.isChecked():
#             return SAME
#         elif header_widget.opp_button.isChecked():
#             return OPP

#     def remove_pictograph(self, key) -> None:
#         ig_pictograph = self.pictographs.pop(key)
#         self.layout.removeWidget(ig_pictograph.view)
#         ig_pictograph.view.setParent(None)
#         ig_pictograph.view.deleteLater()

#     def update_attr_panel_if_needed(self) -> None:
#         if self.pictographs:
#             self.update_attr_panel()

#     def get_static_prop_rot_dir_from_attr_panel(
#         self, motion_type
#     ) -> Literal["cw", "ccw", "no_rot"]:
#         header_widget = (
#             self.parent_tab.filter_tab.motion_type_attr_panel.static_attr_box.header_widget
#         )
#         if motion_type == STATIC:
#             if header_widget.same_button.isChecked():
#                 return CLOCKWISE
#             elif header_widget.opp_button.isChecked():
#                 return COUNTER_CLOCKWISE
#             else:
#                 return NO_ROT
#         else:
#             return NO_ROT

#     def get_turns_from_attr_panel(self, motion_type) -> Turns:
#         return (
#             self.parent_tab.filter_tab.motion_type_attr_panel.get_turns_for_motion_type(
#                 motion_type
#             )
#         )

#     def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
#         keys_to_remove = [
#             key for key in self.pictographs if key.startswith(deselected_letter + "_")
#         ]
#         for key in keys_to_remove:
#             ig_pictograph = self.pictographs.pop(key)
#             self.layout.removeWidget(ig_pictograph.view)
#             ig_pictograph.view.setParent(None)
#             ig_pictograph.view.deleteLater()

#     def generate_pictograph_key_from_dict(self, pictograph_dict) -> str:
#         return (
#             f"{pictograph_dict[LETTER]}_"
#             f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
#             f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
#             f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
#             f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
#             f"{pictograph_dict[RED_MOTION_TYPE]}_"
#             f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
#             f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
#         )

#     def generate_image_name(self, ig_pictograph: IGPictograph, letter: Letters) -> str:
#         return (
#             f"{letter}_"
#             f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}_"
#             f"{ig_pictograph.motions[BLUE].motion_type}_"
#             f"{ig_pictograph.motions[BLUE].prop_rot_dir}_"
#             f"{ig_pictograph.motions[BLUE].start_loc}→{ig_pictograph.motions[BLUE].end_loc}_"
#             f"{ig_pictograph.motions[RED].motion_type}_"
#             f"{ig_pictograph.motions[RED].prop_rot_dir}_"
#             f"{ig_pictograph.motions[RED].start_loc}→{ig_pictograph.motions[RED].end_loc}"
#         )

#     def apply_filters_to_pictograph(self, ig_pictograph: IGPictograph) -> None:
#         for color, motion in ig_pictograph.motions.items():
#             for attr, value in self.filters.items():
#                 if attr.startswith(color):
#                     setattr(motion, attr.replace(f"{color}_", ""), value)
#             motion.update_motion()

#     def clear_layout(self) -> None:
#         while self.layout.count():
#             widget = self.layout.takeAt(0).widget()
#             if widget is not None:
#                 widget.setParent(None)
#                 widget.deleteLater()
#         self.pictographs.clear()

#     def generate_pictograph_key_from_motion(
#         self, ig_pictograph: IGPictograph, letter
#     ) -> str:
#         return (
#             f"{letter}_"
#             f"{ig_pictograph.start_pos}→{ig_pictograph.end_pos}_"
#             f"{ig_pictograph.motions[BLUE].motion_type}→{ig_pictograph.motions[BLUE].end_loc}_"
#             f"{ig_pictograph.motions[RED].motion_type}→{ig_pictograph.motions[RED].end_loc}"
#         )

#     def add_pictograph_to_layout(self, ig_pictograph: IGPictograph, index) -> None:
#         row = index // self.COLUMN_COUNT
#         col = index % self.COLUMN_COUNT
#         self.layout.addWidget(ig_pictograph.view, row, col)
#         ig_pictograph.view.resize_for_scroll_area()

#     def update_attr_panel(self) -> None:
#         first_pictograph = next(iter(self.pictographs.values()), None)
#         for motion in first_pictograph.motions.values():
#             if self.parent_tab.filter_tab.motion_type_attr_panel.isVisible():
#                 for attr_box in self.parent_tab.filter_tab.motion_type_attr_panel.boxes:
#                     if motion.motion_type == attr_box.motion_type:
#                         attr_box.update_attr_box(motion)
#             elif self.parent_tab.filter_tab.color_attr_panel.isVisible():
#                 for attr_box in self.parent_tab.filter_tab.color_attr_panel.boxes:
#                     if motion.motion_type == attr_box.color:
#                         attr_box.update_attr_box(motion)

#     def filter_pictographs(self, pictograph_dicts: List[Dict]) -> List[Dict]:
#         return [
#             pictograph_dict
#             for pictograph_dict in pictograph_dicts
#             if self.pictograph_matches_filters(pictograph_dict)
#         ]

#     def pictograph_matches_filters(self, pictograph_dict: Dict) -> bool:
#         for filter_key, filter_value in self.filters.items():
#             if filter_value in ["0", "1", "2", "3"]:
#                 filter_value = int(filter_value)
#             elif filter_value in ["0.5", "1.5", "2.5"]:
#                 filter_value = float(filter_value)
#             if filter_value != "":
#                 if pictograph_dict.get(filter_key) != filter_value:
#                     return False
#         return True

#     def update_existing_pictographs(self) -> None:
#         for letter, ig_pictograph in self.pictographs.items():
#             if BLUE_TURNS in self.filters:
#                 update = {BLUE_TURNS: self.filters[BLUE_TURNS]}
#                 blue_motion = ig_pictograph.motions[BLUE]
#                 blue_motion.turns = (
#                     float(self.filters[BLUE_TURNS])
#                     if "." in self.filters[BLUE_TURNS]
#                     else int(self.filters[BLUE_TURNS])
#                 )
#                 blue_motion.update_motion(update)
#             elif BLUE_START_ORI in self.filters:
#                 update = {BLUE_START_ORI: self.filters[BLUE_START_ORI]}
#                 ig_pictograph.motions[BLUE].update_motion(update)
#             elif BLUE_END_ORI in self.filters:
#                 ig_pictograph.motions[BLUE].end_ori = self.filters[BLUE_END_ORI]
#                 start_ori = ig_pictograph.motions[BLUE].get_start_ori_from_end_ori()
#                 update = {BLUE_START_ORI: start_ori}
#                 ig_pictograph.motions[BLUE].update_motion(update)
#             if RED_TURNS in self.filters:
#                 update = {RED_TURNS: self.filters[RED_TURNS]}
#                 red_motion = ig_pictograph.motions[RED]
#                 red_motion.turns = (
#                     float(self.filters[RED_TURNS])
#                     if "." in self.filters[RED_TURNS]
#                     else int(self.filters[RED_TURNS])
#                 )
#                 red_motion.update_motion(update)
#             elif RED_START_ORI in self.filters:
#                 update = {RED_START_ORI: self.filters[RED_START_ORI]}
#                 ig_pictograph.motions[RED].update_motion(update)
#             elif RED_END_ORI in self.filters:
#                 ig_pictograph.motions[RED].end_ori = self.filters[RED_END_ORI]
#                 start_ori = ig_pictograph.motions[RED].get_start_ori_from_end_ori()
#                 update = {RED_START_ORI: start_ori}
#                 ig_pictograph.motions[RED].update_motion(update)

#             ig_pictograph.update_pictograph()

#     def _setup_ui(self) -> None:
#         self.setWidgetResizable(True)
#         self.container = QWidget()
#         self.layout: QGridLayout = QGridLayout(self.container)
#         self.container.setContentsMargins(10, 10, 10, 10)
#         self.setWidget(self.container)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

#     def apply_filters(
#         self,
#         filters: Dict[str, Union[Turns, Orientations]],
#     ) -> None:
#         for ig_pictograph in self.pictographs.values():
#             if ig_pictograph._meets_filter_criteria(filters):
#                 self.update_pictographs()

#     ### PICTOGRAPH CREATION ###

#     def _create_pictograph(
#         self,
#         graph_type: Literal["option", "ig_pictograph"],
#     ) -> Option | IGPictograph:
#         if graph_type == OPTION:
#             pictograph = Option(self.main_widget, self)
#         elif graph_type == IG_PICTOGRAPH:
#             pictograph = IGPictograph(self.main_widget, self)
#         return pictograph

#     def reset_turns(self) -> None:
#         for pictograph in self.pictographs.values():
#             for motion in pictograph.motions.values():
#                 motion.turns = 0
#                 motion.update_motion()
#             pictograph.update_pictograph()
