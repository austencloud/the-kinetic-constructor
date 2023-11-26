import logging
from objects.props.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    StaffAttributesDicts,
    TYPE_CHECKING,
)
if TYPE_CHECKING:
    from objects.arrow import Arrow
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
from settings.string_constants import STAFF_SVG_FILE_PATH


logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

class Staff(Prop):
    arrow: "Arrow"
    svg_file: str

    def __init__(
        self,
        main_widget: "MainWidget",
        graphboard: "GraphBoard",
        attributes,
    ) -> None:
        svg_file = STAFF_SVG_FILE_PATH
        super().__init__(main_widget, graphboard, svg_file, attributes)


class RedStaff(Staff):
    def __init__(
        self,
        main_widget: "MainWidget",
        graphboard: "GraphBoard",
        dict: StaffAttributesDicts,
    ) -> None:
        super().__init__(main_widget, graphboard, dict)
        self.setSharedRenderer(self.renderer)


class BlueStaff(Staff):
    def __init__(
        self,
        main_widget: "MainWidget",
        graphboard: "GraphBoard",
        dict: StaffAttributesDicts,
    ) -> None:
        super().__init__(main_widget, graphboard, dict)
        self.setSharedRenderer(self.renderer)
