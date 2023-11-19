from objects.staff import Staff
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, StaffAttributesDicts
if TYPE_CHECKING:
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
        self, graphboard: "GraphBoard", attributes: StaffAttributesDicts
    ) -> None:
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.graphboard = graphboard
        self.target_staff = None
