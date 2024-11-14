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

    def get_initial_coords(self, arrow: Arrow) -> QPointF:
        if arrow.motion.motion_type in [PRO, ANTI, FLOAT]:
            return self._get_shift_coords(arrow)
        elif arrow.motion.motion_type in [STATIC, DASH]:
            return self._get_static_coords(arrow)

    def _get_shift_coords(self, arrow: Arrow) -> QPointF:
        layer2_points = self.pictograph.grid.grid_data.layer2_points_normal
        grid_mode = (
            self.pictograph.main_widget.settings_manager.global_settings.get_grid_mode()
        )
        point_name = f"{arrow.loc}_{grid_mode}_layer2_point"
        return layer2_points.points[point_name].coordinates

    def _get_static_coords(self, arrow: Arrow) -> QPointF:
        hand_points = self.pictograph.grid.grid_data.hand_points_normal
        grid_mode = (
            self.pictograph.main_widget.settings_manager.global_settings.get_grid_mode()
        )
        point_name = f"{arrow.loc}_{grid_mode}_hand_point"
        return hand_points.points[point_name].coordinates
