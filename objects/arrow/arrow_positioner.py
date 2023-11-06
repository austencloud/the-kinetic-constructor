from PyQt6.QtCore import QPointF
from settings.numerical_constants import *
from settings.string_constants import *

class ArrowPositioner:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager
        self.letters = self.arrow_manager.main_widget.letters



    def set_optimal_arrow_pos(self, current_arrows):
        current_state = self.arrow_manager.graphboard.get_state()
        current_letter = self.arrow_manager.graphboard.info_handler.determine_current_letter_and_type()[
            0
        ]
        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_locations = (
                self.arrow_manager.state_comparator.find_optimal_locations(
                    current_state, matching_letters
                )
            )
            for arrow in current_arrows:
                if optimal_locations:
                    optimal_location = optimal_locations.get(
                        f"optimal_{arrow.color}_location"
                    )
                    if optimal_location:
                        pos = QPointF(
                            optimal_location["x"] * GRAPHBOARD_SCALE,
                            optimal_location["y"] * GRAPHBOARD_SCALE,
                        )

                        new_x = pos.x() - (arrow.boundingRect().width()) / 2
                        new_y = pos.y() - (arrow.boundingRect().height()) / 2

                        new_pos = QPointF(new_x, new_y)
                        arrow.setPos(new_pos)
                else:
                    self.set_default_arrow_pos(arrow)

    def set_default_arrow_pos(self, arrow):
        quadrant_center = self.arrow_manager.graphboard.grid.get_layer2_point(arrow.quadrant)
        pos = (quadrant_center * GRAPHBOARD_SCALE) - arrow.center
        adjustment = QPointF(0, 0)  # Initialize an adjustment QPointF

        if arrow.quadrant == NORTHEAST:
            adjustment = QPointF(ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == SOUTHEAST:
            adjustment = QPointF(ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == SOUTHWEST:
            adjustment = QPointF(-ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == NORTHWEST:
            adjustment = QPointF(-ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)

        # Create a new QPointF for the sum
        new_pos = QPointF(pos.x() + adjustment.x(), pos.y() + adjustment.y())

        # Manually add the x and y coordinates for the final position
        final_pos = QPointF(
            new_pos.x() + GRAPHBOARD_GRID_PADDING, new_pos.y() + GRAPHBOARD_GRID_PADDING
        )

        arrow.setPos(final_pos.x(), final_pos.y())
