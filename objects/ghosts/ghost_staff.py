from objects.props.staff import Staff
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, PropAttributesDicts

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class GhostStaff(Staff):
    """
    Represents a ghost staff object.

    Args:
        pictograph (Pictograph): The main Pictograph object.
        attributes (StaffAttributesDicts): The attributes of the ghost staff.

    Attributes:

        target_staff: The staff that the ghost arrow is mimicking.

    """

    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        attributes: PropAttributesDicts,
    ) -> None:
        super().__init__(main_widget, pictograph, attributes)
        self.setOpacity(0.2)
        self.target_staff = None
