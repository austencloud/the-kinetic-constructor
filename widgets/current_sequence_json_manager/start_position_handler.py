from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import NO_ROT
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.current_sequence_json_manager.current_sequence_json_manager import CurrentSequenceJsonManager


class StartPositionHandler:
    def __init__(self, manager: "CurrentSequenceJsonManager"):
        self.manager = manager

    def set_start_position_data(self, start_pos_pictograph: Pictograph) -> None:
        red_start_ori = start_pos_pictograph.pictograph_dict["red_attributes"][
            "start_ori"
        ]
        blue_start_ori = start_pos_pictograph.pictograph_dict["blue_attributes"][
            "start_ori"
        ]

        sequence = self.manager.loader_saver.load_current_sequence_json()

        start_position_dict = {
            "beat": 0,
            "sequence_start_position": start_pos_pictograph.end_pos[:-1],
            "letter": start_pos_pictograph.letter.name,
            "end_pos": start_pos_pictograph.end_pos,
            "blue_attributes": {
                "start_loc": start_pos_pictograph.blue_motion.start_loc,
                "end_loc": start_pos_pictograph.blue_motion.end_loc,
                "start_ori": blue_start_ori,
                "end_ori": blue_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.blue_motion.motion_type,
            },
            "red_attributes": {
                "start_loc": start_pos_pictograph.red_motion.start_loc,
                "end_loc": start_pos_pictograph.red_motion.end_loc,
                "start_ori": red_start_ori,
                "end_ori": red_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.red_motion.motion_type,
            },
        }

        if len(sequence) == 1:
            sequence.append(start_position_dict)
        else:
            sequence.insert(1, start_position_dict)

        self.manager.loader_saver.save_current_sequence(sequence)

    def update_start_pos_ori(self, color: Color, ori: int) -> None:
        sequence = self.manager.loader_saver.load_current_sequence_json()
        if sequence:
            sequence[1][f"{color}_attributes"]["end_ori"] = ori
            sequence[1][f"{color}_attributes"]["start_ori"] = ori
            self.manager.loader_saver.save_current_sequence(sequence)
