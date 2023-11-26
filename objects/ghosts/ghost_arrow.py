from settings.string_constants import COLOR
from objects.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from utilities.TypeChecking.TypeChecking import ArrowAttributesDicts
    from objects.arrow import Arrow


class GhostArrow(Arrow):
    """
    Represents a ghost arrow object, displaying the position that an arrow will be while dragging if the user were to drop it.

    Inherits from the Arrow class.

    Attributes:
        graphboard (GraphBoard): The graphboard object.
        color (str): The color of the arrow.
        target_arrow (Arrow): The arrow that the ghost arrow is copying.

    Methods:
        __init__: Initialize a GhostArrow object.

    """

    def __init__(
        self, graphboard: "GraphBoard", attributes: "ArrowAttributesDicts"
    ) -> None:
        """
        Initialize a GhostArrow object.

        Args:
            graphboard (GraphBoard): The graphboard object.
            attributes (MotionAttributesDicts): The attributes of the arrow.

        Returns:
            None
        """
        super().__init__(graphboard, attributes, None)
        self.setOpacity(0.2)
        self.graphboard, self.color, self.target_arrow = (
            graphboard,
            attributes[COLOR],
            None,
        )
        self.setup_svg_renderer(self.svg_file)

    def update(self, attributes) -> None:
        """
        Update the GhostArrow object with new attributes.

        Args:
            attributes (MotionAttributesDicts): The updated attributes of the arrow.

        Returns:
            None
        """
        self.set_attributes_from_dict(attributes)
        self.update_appearance()
        self.show()
