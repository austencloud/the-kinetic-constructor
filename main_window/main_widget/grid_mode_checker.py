from typing import TYPE_CHECKING, Literal

from data.constants import BOX, DIAMOND


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GridModeChecker:
    """Checks what grid a given pictograph is in by looking at its start and end positions"""


    def get_grid_mode(
        self, pictograph_dict
    ) -> None | Literal["box"] | Literal["diamond"]:
        box_mode_positions = self.get_box_mode_positions()
        diamond_mode_positions = self.get_diamond_mode_positions()

        if (
            pictograph_dict["start_pos"] in box_mode_positions
            and pictograph_dict["end_pos"] in box_mode_positions
        ):
            return BOX
        elif (
            pictograph_dict["start_pos"] in diamond_mode_positions
            and pictograph_dict["end_pos"] in diamond_mode_positions
        ):
            return DIAMOND

        elif (
            pictograph_dict["start_pos"] in box_mode_positions
            and pictograph_dict["end_pos"] in diamond_mode_positions
        ) or (
            pictograph_dict["start_pos"] in diamond_mode_positions
            and pictograph_dict["end_pos"] in box_mode_positions
        ):
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
