from settings.string_constants import COLOR
from objects.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard
    from utilities.TypeChecking.TypeChecking import ArrowAttributesDicts
    from objects.arrow import Arrow
    from widgets.arrowbox.arrowbox_drag import ArrowBoxDrag


class GhostArrow(Arrow):
    def __init__(
        self, graphboard: "GraphBoard", attributes: "ArrowAttributesDicts"
    ) -> None:
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.graphboard, self.color, self.target_arrow = (
            graphboard,
            attributes[COLOR],
            None,
        )
        self.setup_svg_renderer(self.svg_file)

    def update(self, target_arrow: "Arrow", drag: 'ArrowBoxDrag' = None) -> None:
        self.set_attributes_from_dict(
            target_arrow.get_attributes() if not drag else drag.get_attributes()
        )
        self.update_svg(target_arrow.svg_file)
        self.setup_graphics_flags()
        self.update_appearance()
        self.show()
