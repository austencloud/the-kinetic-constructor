from typing import TYPE_CHECKING, Literal

from data.constants import BOX, DIAMOND


if TYPE_CHECKING:
    pass


class GridModeChecker:
    """Checks what grid a given pictograph is in by looking at its start and end positions"""

    def get_grid_mode(
        self, pictograph_dict: dict
    ) -> None | Literal["box"] | Literal["diamond"]:
        box_mode_positions = self.get_box_mode_positions()
        diamond_mode_positions = self.get_diamond_mode_positions()

        start_pos = (
            pictograph_dict.get("end_pos")
            if pictograph_dict.get("sequence_start_position")
            else pictograph_dict.get("start_pos")
        )
        end_pos = pictograph_dict.get("end_pos")

        if start_pos in box_mode_positions and end_pos in box_mode_positions:
            return BOX
        elif start_pos in diamond_mode_positions and end_pos in diamond_mode_positions:
            return DIAMOND

        elif (
            start_pos in box_mode_positions and end_pos in diamond_mode_positions
        ) or (start_pos in diamond_mode_positions and end_pos in box_mode_positions):
            return "skewed"

    def get_diamond_mode_positions(self):
        positions = [
            "alpha1",
            "alpha3",
            "alpha5",
            "alpha7",
            "beta1",
            "beta3",
            "beta5",
            "beta7",
            "gamma1",
            "gamma3",
            "gamma5",
            "gamma7",
            "gamma9",
            "gamma11",
            "gamma13",
            "gamma15",
        ]
        return positions

    def get_box_mode_positions(self):
        positions = [
            "alpha2",
            "alpha4",
            "alpha6",
            "alpha8",
            "beta2",
            "beta4",
            "beta6",
            "beta8",
            "gamma2",
            "gamma4",
            "gamma6",
            "gamma8",
            "gamma10",
            "gamma12",
            "gamma14",
            "gamma16",
        ]
        return positions
