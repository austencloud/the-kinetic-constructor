from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtCore import QPointF
import random
import os
from objects.arrow.arrow import Arrow
from utilities.export_handler import ExportHandler
from settings.string_constants import *


class PictographGenerator:
    def __init__(self, main_widget, scene, infobox):
        self.scene = scene
        self.infobox = infobox
        self.main_window = main_widget.main_window
        self.export_manager = main_widget.export_manager
        self.grid = self.scene.grid
        self.output_dir = "images/pictographs"
        self.current_letter = None
        self.letters = main_widget.letters

    def generate_all_pictographs(self, staff_handler):
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
                            QUADRANT,
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
                        self.export_manager = ExportHandler(
                            self.scene,
                            self.graphboard,
                            self.staff_handler,
                            self.grid,
                        )
                        self.export_manager.export_to_svg(output_file_path)

                # Clear the graphboard for the next combination
                self.scene.clear()

    def open_selection_window(self, letter):
        self.output_dir = "images/pictographs"
        self.scene.clear()

        combinations = self.letters.get(letter, [])
        if not combinations:
            self.scene.update_letter(None)
            self.infobox.update()
            return
        self.current_letter = letter
        self.scene.update_letter(self.current_letter)

        combination_set = random.choice(combinations)
        created_arrows = []

        optimal_positions = next(
            (
                d
                for d in combination_set
                if "optimal_red_location" in d and "optimal_blue_location" in d
            ),
            None,
        )
        for combination in combination_set:
            if all(
                key in combination
                for key in [
                    COLOR,
                    MOTION_TYPE,
                    ROTATION_DIRECTION,
                    QUADRANT,
                    TURNS,
                ]
            ):
                if combination[MOTION_TYPE] == STATIC:
                    svg_file = f"resources/images/arrows/static_0.svg"
                    arrow = Arrow(
                        svg_file,
                        self.scene,
                        self.infobox,
                        self.svg_manager,
                        self.arrow_manager,
                        STATIC,
                        self.staff_handler,
                    )
                created_arrows.append(arrow)

        # Add the arrows to the scene
        for arrow in created_arrows:
            if arrow.scene is not self.graphboard:
                self.graphboard.addItem(arrow)

        for arrow in created_arrows:
            if optimal_positions:
                optimal_position = optimal_positions.get(
                    f"optimal_{arrow.color}_location"
                )
                if optimal_position:
                    # Calculate the position to center the arrow at the optimal position
                    pos = (
                        QPointF(optimal_position["x"], optimal_position["y"])
                        - arrow.boundingRect().center()
                    )
                    arrow.setPos(pos)
                else:
                    if arrow.quadrant != "None":
                        pos = (
                            self.scene.get_quadrant_center(arrow.quadrant)
                            - arrow.boundingRect().center()
                        )
            else:
                # Calculate the position to center the arrow at the quadrant center
                pos = (
                    self.scene.get_quadrant_center(arrow.quadrant)
                    - arrow.boundingRect().center()
                )
                arrow.setPos(pos)

        self.staff_handler.update_graphboard_staffs(self.graphboard)
        # created_arrows should be a list
        self.infobox.update()

    def get_current_letter(self):
        return self.current_letter

    def update_staff(self, arrow, staff_handler):
        arrows = [arrow] if not isinstance(arrow, list) else arrow

        staff_positions = [
            arrow.end_location.upper() + "_staff_" + arrow.color for arrow in arrows
        ]

        for element_id, staff in staff_handler.graphboard_staffs.items():
            if element_id in staff_positions:
                staff.show()
            else:
                staff.hide()

        self.staff_handler.check_replace_beta_staffs()
