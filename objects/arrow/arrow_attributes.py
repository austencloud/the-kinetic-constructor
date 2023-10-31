from data.start_end_location_mapping import start_end_location_mapping

class ArrowAttributes:
    ARROW_ATTRIBUTES = [
        'color', 'motion_type', 'rotation_direction', 
        'quadrant', 'end_location', 'start_location', 'turns'
    ]
    
    def __init__(self, arrow, arrow_dict = None):
        if arrow_dict:
            self.update_attributes(arrow, arrow_dict)

    def update_attributes(self, arrow, arrow_dict):
        for attr in self.ARROW_ATTRIBUTES:
            value = arrow_dict.get(attr)
            if attr == 'turns':
                value = int(value)
            setattr(arrow, attr, value)

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        return start_end_location_mapping.get(
            quadrant, {}).get(rotation_direction, {}).get(motion_type, (None, None))

    def get_attr(self, arrow):
        return {attr: getattr(arrow, attr) for attr in self.ARROW_ATTRIBUTES}

    def create_arrow_dict(self, color, motion_type, rotation_direction, quadrant, start_location, end_location, turns):
        if start_location is None and end_location is None:
            start_location, end_location = self.view.arrow_manager.arrow_attributes.get_start_end_locations(motion_type, rotation_direction, quadrant)
        arrow_dict = {
            'color': color,
            'motion_type': motion_type,
            'rotation_direction': rotation_direction,
            'quadrant': quadrant,
            'start_location': start_location,
            'end_location': end_location,
            'turns': turns
        }
        return arrow_dict