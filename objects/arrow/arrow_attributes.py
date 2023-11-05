from data.start_end_location_mapping import start_end_location_mapping


class ArrowAttributes:
    ARROW_ATTRIBUTES = [
        "color",
        "motion_type",
        "rotation_direction",
        "quadrant",
        "end_location",
        "start_location",
        "turns",
    ]

    def __init__(self, arrow, arrow_dict=None):
        if arrow_dict:
            self.update_attributes(arrow, arrow_dict)

    def update_attributes(self, arrow, arrow_dict):
        for attr in self.ARROW_ATTRIBUTES:
            value = arrow_dict.get(attr)
            if attr == "turns":
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
        if arrow.motion_type in ["pro", "anti"]:
            start_location, end_location = self.get_start_end_locations(
                arrow.motion_type, arrow.rotation_direction, arrow.quadrant
            )
        elif arrow.motion_type == "static":
            start_location, end_location = arrow.start_location, arrow.end_location

        arrow_dict = {
            "color": arrow.color,
            "motion_type": arrow.motion_type,
            "rotation_direction": arrow.rotation_direction,
            "quadrant": arrow.quadrant,
            "start_location": start_location,
            "end_location": end_location,
            "turns": arrow.turns,
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
            "motion_type": arrow.motion_type,
            "start_location": arrow.start_location,
            "end_location": arrow.end_location,
            "turns": arrow.turns,
            COLOR: arrow.color,
        }
        return attributes
