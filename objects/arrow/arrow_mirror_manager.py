from PyQt6.QtGui import QTransform
from constants import *
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING
if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowMirrorManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_mirror(self) -> None:
        if self.arrow.motion_type == PRO:
            rot_dir = self.arrow.motion.prop_rot_dir
            if rot_dir == CLOCKWISE:
                self.arrow.is_svg_mirrored = False
            elif rot_dir == COUNTER_CLOCKWISE:
                self.arrow.is_svg_mirrored = True
        elif self.arrow.motion_type == ANTI:
            rot_dir = self.arrow.motion.prop_rot_dir
            if rot_dir == CLOCKWISE:
                self.arrow.is_svg_mirrored = True
            elif rot_dir == COUNTER_CLOCKWISE:
                self.arrow.is_svg_mirrored = False
        elif self.arrow.motion_type == DASH:
            if self.arrow.turns > 0:
                if self.arrow.motion.prop_rot_dir == CLOCKWISE:
                    self.arrow.is_svg_mirrored = False
                elif self.arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    self.arrow.is_svg_mirrored = True
            else:
                self.arrow.is_svg_mirrored = False
        elif self.arrow.motion_type == STATIC:
            if self.arrow.turns > 0:
                if self.arrow.motion.prop_rot_dir == CLOCKWISE:
                    self.arrow.is_svg_mirrored = False
                elif self.arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    self.arrow.is_svg_mirrored = True
            else:
                self.arrow.is_svg_mirrored = False

        if self.arrow.is_svg_mirrored:
            self.mirror_svg(self.arrow)
            if not self.arrow.is_ghost:
                self.mirror_svg(self.arrow.ghost)
        else:
            self.unmirror_svg(self.arrow)
            if not self.arrow.is_ghost:
                self.unmirror_svg(self.arrow.ghost)

    def mirror_svg(self, arrow: "Arrow") -> None:
        center_x = self.arrow.boundingRect().center().x()
        center_y = self.arrow.boundingRect().center().y()
        arrow.set_arrow_transform_origin_to_center()
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(-1, 1)
        transform.translate(-center_x, -center_y)
        arrow.setTransform(transform)
        if not arrow.is_ghost and arrow.ghost:
            arrow.ghost.setTransform(transform)
            arrow.ghost.is_svg_mirrored = True
        arrow.is_svg_mirrored = True

    def unmirror_svg(self, arrow: "Arrow") -> None:
        center_x = arrow.boundingRect().center().x()
        center_y = arrow.boundingRect().center().y()
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(1, 1)
        transform.translate(-center_x, -center_y)
        arrow.setTransform(transform)
        if hasattr(self, GHOST) and arrow.ghost:
            arrow.ghost.setTransform(transform)
            arrow.ghost.is_svg_mirrored = False
        arrow.is_svg_mirrored = False
