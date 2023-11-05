from data.start_end_location_mapping import start_end_location_mapping
from settings.string_constants import *


class ArrowAttributes:
    ARROW_ATTRIBUTES = [
        COLOR,
        MOTION_TYPE,
        ROT_DIR,
        QUADRANT,
        START,
        END,
        TURNS,
    ]

    def __init__(self, arrow, arrow_dict=None):
        if arrow_dict:
            self.update_attributes(arrow, arrow_dict)

    def update_attributes(self, arrow, arrow_dict):
        for attr in self.ARROW_ATTRIBUTES:
            value = arrow_dict.get(attr)
            if attr == TURNS:
                value = int(value)
            setattr(arrow, attr, value)

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        return (
            start_end_location_mapping.get(quadrant, {})
            .get(rotation_direction, {})
            .get(motion_type, (None, None))
        )

    def get_attributes(self, arrow):
        return {attr: getattr(arrow, attr) for attr in self.ARROW_ATTRIBUTES}

    def create_dict_from_arrow(self, arrow):
        if arrow.motion_type in [PRO, ANTI]:
            start_location, end_location = self.get_start_end_locations(
                arrow.motion_type, arrow.rotation_direction, arrow.quadrant
            )
        elif arrow.motion_type == STATIC:
            start_location, end_location = arrow.start_location, arrow.end_location

        arrow_dict = {
            COLOR: arrow.color,
            MOTION_TYPE: arrow.motion_type,
            ROT_DIR: arrow.rotation_direction,
            QUADRANT: arrow.quadrant,
            START: start_location,
            END: end_location,
            TURNS: arrow.turns,
        }
        return arrow_dict

    def get_graphboard_arrow_attributes_by_color(self, color, graphboard_view):
        # Assuming you have a method to get arrows by color in graphboard_view
        arrows = graphboard_view.get_arrows_by_color(color)
        if not arrows:
            return {}

        # For simplicity, we'll use the first arrow of the given color
        arrow = arrows[0]

        attributes = {
            MOTION_TYPE: arrow.motion_type,
            START: arrow.start_location,
            END: arrow.end_location,
            TURNS: arrow.turns,
            COLOR: arrow.color,
        }
        return attributes
