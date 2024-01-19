from typing import TYPE_CHECKING
from constants import ANTI, DASH, PRO, STATIC
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class ArrowInitialPosCalculator:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def get_initial_pos(self, arrow: Arrow) -> QPointF:
        if arrow.motion.motion_type in [PRO, ANTI]:
            return self._get_diamond_shift_pos(arrow)
        elif arrow.motion.motion_type in [STATIC, DASH]:
            return self._get_diamond_static_dash_pos(arrow)

    def _get_diamond_shift_pos(self, arrow: Arrow) -> QPointF:
        layer = self.pictograph.grid.grid_data.layer2_points_normal
        point_name = f"{arrow.loc}_{self.pictograph.main_widget.grid_mode}_layer2_point"
        return layer.points[point_name].coordinates

    def _get_diamond_static_dash_pos(self, arrow: Arrow) -> QPointF:
        layer = self.pictograph.grid.grid_data.hand_points_normal
        point_name = f"{arrow.loc}_{self.pictograph.main_widget.grid_mode}_hand_point"
        return layer.points[point_name].coordinates
