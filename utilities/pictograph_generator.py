import os
from constants.string_constants import (
    PICTOGRAPH_DIR,
    START_POS,
    END_POS,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    ANTI,
    PRO,
    COLOR,
    RED,
    ARROW_LOCATION,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class PictographGenerator:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.pictograph = main_widget.graph_editor_widget.graph_editor.pictograph
        self.main_window = main_widget.main_window
        self.export_handler = main_widget.export_handler
        self.grid = self.pictograph.grid
        self.output_dir = f"{PICTOGRAPH_DIR}"
        self.letters = main_widget.letters

    def generate_all_pictographs(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

        for letter, combinations in self.letters.items():
            for combination in combinations:
                positions_dict = next(
                    (d for d in combination if START_POS in d and END_POS in d),
                    None,
                )
                if positions_dict is None:
                    continue

                start_position = (
                    positions_dict[START_POS]
                    .replace("alpha", "a")
                    .replace("beta", "b")
                    .replace("gamma", "g")
                )
                end_position = (
                    positions_dict[END_POS]
                    .replace("alpha", "a")
                    .replace("beta", "b")
                    .replace("gamma", "g")
                )

                motion_types = [
                    arrow_dict[MOTION_TYPE]
                    for arrow_dict in combination
                    if MOTION_TYPE in arrow_dict
                ]
                is_hybrid = (
                    motion_types.count(ANTI) == 1 and motion_types.count(PRO) == 1
                )

                for arrow_dict in combination:
                    if all(
                        key in arrow_dict
                        for key in [
                            COLOR,
                            MOTION_TYPE,
                            ROTATION_DIRECTION,
                            ARROW_LOCATION,
                        ]
                    ):
                        color = arrow_dict[COLOR]
                        motion_type = arrow_dict[MOTION_TYPE]

                        file_name = f"{letter}_{start_position}_{end_position}"
                        if motion_type == PRO and is_hybrid and color == RED:
                            file_name += f"_r-pro_l-anti"
                        elif motion_type == ANTI and is_hybrid and color == RED:
                            file_name += f"_r-anti_l-pro"
                        file_name += ".svg"

                        output_file_path = os.path.join(self.output_dir, file_name)
                        self.export_handler = self.pictograph.main_widget.export_handler
                        self.export_handler.export_to_svg(output_file_path)

                # Clear the pictograph for the next combination
                self.pictograph.clear()
