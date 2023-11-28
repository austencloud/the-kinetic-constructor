from objects.props import Prop
from settings.string_constants import COLOR
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

    def update_ghost_prop(self, attributes) -> None:
        self.set_attributes_from_dict(attributes)
        self.update_appearance()
        self.show()
