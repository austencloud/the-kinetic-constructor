import logging
from objects.arrow import Arrow
from objects.props.prop import Prop
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
    arrow: "Arrow"
    svg_file: str
    color: Color
    location: Location
    layer: Layer
    axis: Axis

    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        attributes,
    ) -> None:
        svg_file = "resources/images/props/staff_with_thumb.svg"
        super().__init__(main_widget, pictograph, svg_file, attributes)

    def update_appearance(self) -> None:
        self.axis = self.get_axis(self.location)
        super().update_appearance()
