from objects.prop import Prop
from settings.string_constants import (
    COLOR,
    PROP_TYPE,
    STAFF,
    TRIAD,
    HOOP,
    FAN,
    CLUB,
    BUUGENG,
)
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, PropAttributesDicts

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class GhostProp(Prop):
    """
    Represents a ghost prop object, displaying the position that a prop will be while dragging if the user were to drop it.

    Inherits from the Prop class.

    Attributes:
        pictograph (Pictograph): The pictograph object.
        color (str): The color of the prop.
        target_prop (Prop): The prop that the ghost prop is copying.

    Methods:
        __init__: Initialize a GhostProp object.

    """

    def __init__(
        self, pictograph: "Pictograph", attributes: PropAttributesDicts
    ) -> None:
        super().__init__(pictograph, attributes)
        self.setOpacity(0.2)
        self.pictograph = pictograph
        self.color = attributes[COLOR]
        self.target_prop: "Prop" = None
        self.setup_svg_renderer(self.svg_file)


class GhostStaff(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = STAFF
        super().__init__(pictograph, attributes)


class GhostTriad(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = TRIAD
        super().__init__(pictograph, attributes)


class GhostHoop(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = HOOP
        super().__init__(pictograph, attributes)


class GhostFan(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = FAN
        super().__init__(pictograph, attributes)


class GhostClub(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = CLUB
        super().__init__(pictograph, attributes)


class GhostBuugeng(GhostProp):
    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = BUUGENG
        super().__init__(pictograph, attributes)
