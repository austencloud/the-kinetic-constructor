import logging
from objects.arrow import Arrow
from objects.props.prop import Prop
from settings.string_constants import PROP_TYPE, STAFF
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from objects.arrow import Arrow
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import (
    Color,
    Location,
    Layer,
    Axis,
)

logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Staff(Prop):
    """
    Represents a Staff. Inherits from the Prop class.

    Attributes:
        arrow (Arrow): The arrow associated with the staff.
        svg_file (str): The SVG file path for the staff.
        color (Color): The color of the staff.
        location (Location): The location of the staff.
        layer (Layer): The layer of the staff.
        axis (Axis): The axis of the staff.
    """

    arrow: "Arrow"
    svg_file: str
    color: Color
    location: Location
    layer: Layer
    axis: Axis

    def __init__(self, pictograph: "Pictograph", attributes) -> None:
        attributes[PROP_TYPE] = STAFF
        super().__init__(pictograph, attributes)

    def update_appearance(self) -> None:
        """
        Updates the appearance of the staff.
        """
        self.axis = self.get_axis(self.location)
        super().update_appearance()
