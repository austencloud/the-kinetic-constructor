from typing import TYPE_CHECKING
from data.constants import ANTI, DASH, FLOAT, PRO, STATIC
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class ArrowInitialPosCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.pictograph: "BasePictograph" = placement_manager.pictograph

    def get_initial_coords(self, arrow: Arrow, grid_mode: str) -> QPointF:
        if arrow.motion.motion_type in [PRO, ANTI, FLOAT]:
            return self._get_shift_coords(arrow, grid_mode)
        elif arrow.motion.motion_type in [STATIC, DASH]:
            return self._get_static_coords(arrow, grid_mode)

    def _get_shift_coords(self, arrow: Arrow, grid_mode:str) -> QPointF:
        """
        Retrieves the coordinates for a given layer2 point name.
        """
        point_name = f"{arrow.loc}_{grid_mode}_layer2_point"
        coord = self.pictograph.grid.grid_data.get_shift_coord(point_name)
        if coord:
            return coord
        else:
            print(f"Warning: Shift coordinate for '{point_name}' not found.")
            return QPointF(0, 0)

    def _get_grid_mode_from_arrow_loc(self, arrow: "Arrow") -> str:
        if arrow.motion.prop.loc in ["ne", "nw", "se", "sw"]:
            grid_mode = "box"
        elif arrow.motion.prop.loc in ["n", "s", "e", "w"]:
            grid_mode = "diamond"
        return grid_mode

    def _get_static_coords(self, arrow: Arrow, grid_mode:str) -> QPointF:
        """
        Retrieves the coordinates for a given static point name.
        """
        point_name = f"{arrow.loc}_{grid_mode}_hand_point"
        coord = self.pictograph.grid.grid_data.get_static_coord(point_name)
        if coord:
            return coord
        else:
            print(f"Warning: Static coordinate for '{point_name}' not found.")
            return QPointF(0, 0)  # Example default
