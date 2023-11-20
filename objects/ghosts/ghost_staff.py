from objects.staff import Staff
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, StaffAttributesDicts
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graphboard.graphboard import GraphBoard

class GhostStaff(Staff):
    """
    Represents a ghost staff object.

    Args:
        graphboard (GraphBoard): The main GraphBoard object. 
        attributes (StaffAttributesDicts): The attributes of the ghost staff.

    Attributes:
    
        target_staff: The staff that the ghost arrow is mimicking.

    """

    def __init__(
        self, main_widget: "MainWidget", graphboard: "GraphBoard", attributes: StaffAttributesDicts
    ) -> None:
        super().__init__(main_widget, graphboard, attributes)
        self.setOpacity(0.2)
        self.target_staff = None
