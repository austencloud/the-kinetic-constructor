from constants.string_constants import HORIZONTAL, VERTICAL
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropManipulator:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def swap_axis(self) -> None:
        if self.prop.axis == VERTICAL:
            self.prop.axis = HORIZONTAL
        else:
            self.prop.axis = VERTICAL
        self.prop.update_rotation()

    def swap_layer(self) -> None:
        if self.prop.layer == 1:
            self.prop.layer = 2
        else:
            self.prop.layer = 1
        self.prop.update_rotation()

    def delete(self) -> None:
        self.prop.scene.removeItem(self.prop)
        self.prop.scene.removeItem(self.prop.scene.ghost_props[self.prop.color])
        self.prop.motion.arrow.clear_attributes()
        self.prop.motion.arrow.ghost.clear_attributes()
        self.prop.motion.clear_attributes()
        self.prop.clear_attributes()
        self.prop.scene.update_pictograph()
