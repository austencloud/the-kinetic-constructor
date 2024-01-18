from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from objects.graphical_object.graphical_object import GraphicalObject


class GraphicalObjectAttrManager:
    def __init__(self, graphical_object: "GraphicalObject") -> None:
        self.graphical_object = graphical_object

    def update_attributes(self, attributes: Dict) -> None:
        for attribute_name, attribute_value in attributes.items():
            setattr(self, attribute_name, attribute_value)
