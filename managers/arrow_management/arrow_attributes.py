import os
from data.start_end_location_mapping import start_end_location_mapping


class ArrowAttributes:
    def __init__(self, arrow, arrow_dict=None):
        self.dict = arrow_dict
        self.arrow = arrow
        
        if arrow_dict:
            self.update_attributes_from_dict(arrow, arrow_dict)


    def update_attributes_from_dict(self, arrow, arrow_dict):
        arrow.color = arrow_dict.get('color')
        arrow.motion_type = arrow_dict.get('motion_type')
        arrow.rotation_direction = arrow_dict.get('rotation_direction')
        arrow.quadrant = arrow_dict.get('quadrant')
        arrow.end_location = arrow_dict.get('end_location')
        arrow.start_location = arrow_dict.get('start_location')
        arrow.turns = int(arrow_dict.get('turns'))

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        start_location, end_location = start_end_location_mapping.get(
            quadrant, {}).get(rotation_direction, {}).get(motion_type, (None, None))
        return start_location, end_location
    
    def get_attributes(self, arrow):
        attributes = {
            'color': arrow.color,
            'motion_type': arrow.motion_type,
            'quadrant': arrow.quadrant,
            'rotation_direction': arrow.rotation_direction,
            'start_location': arrow.start_location,
            'end_location': arrow.end_location,
            'turns': arrow.turns
        }
        return attributes

