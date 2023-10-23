import os
from data.start_end_location_mapping import start_end_location_mapping
#import Qtransform
from PyQt6.QtGui import QTransform

class ArrowAttributes:
    def __init__(self, arrow, arrow_dict=None, svg_file=None, motion_type=None, color=None, quadrant=None, rotation_direction=None, turns=None):
        self.dict = arrow_dict if arrow_dict else {}
        self.svg_file = svg_file if svg_file else ""
        self.motion_type = motion_type if motion_type else ""
        self.color = color if color else ""
        self.quadrant = quadrant if quadrant else ""
        self.rotation_direction = rotation_direction if rotation_direction else ""
        self.turns = turns if turns else 0
        self.start_location = None
        self.end_location = None
        self.arrow = arrow
        if arrow_dict:
            self.update(arrow_dict)

    def update(self, arrow_dict):
        self.update_attributes_from_dict(arrow_dict)
        self.update_start_end_locations()
        self.update_appearance()

    def update_appearance(self):
        self.update_color()
        self.update_mirror()
        self.update_rotation()

    def update_attributes_from_dict(self, arrow_dict):
        self.color = arrow_dict.get('color', self.color)
        self.motion_type = arrow_dict.get('motion_type', self.motion_type)
        self.rotation_direction = arrow_dict.get('rotation_direction', self.rotation_direction)
        self.quadrant = arrow_dict.get('quadrant', self.quadrant)
        self.end_location = arrow_dict.get('end_location', self.end_location)
        self.start_location = arrow_dict.get('start_location', self.start_location)
        self.turns = int(arrow_dict.get('turns', self.turns))

    def update_from_filename(self):
        if self.svg_file:
            parts = os.path.basename(self.svg_file).split('_')
            self.motion_type, self.turns = parts[:2]
            self.turns = int(self.turns.split('.')[0])

    def update_start_end_locations(self):
        self.start_location, self.end_location = start_end_location_mapping.get(
            self.quadrant, {}).get(self.rotation_direction, {}).get(self.motion_type, (None, None))


    def get_attributes(self):
        attributes = {
            'color': self.color,
            'motion_type': self.motion_type,
            'quadrant': self.quadrant,
            'rotation_direction': self.rotation_direction,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'turns': self.turns
        }
        return attributes

    def update_arrow_for_new_quadrant(self, new_quadrant):
        if new_quadrant in start_end_location_mapping:
            if self.rotation_direction in start_end_location_mapping[new_quadrant]:
                if self.motion_type in start_end_location_mapping[new_quadrant][self.rotation_direction]:
                    self.quadrant = new_quadrant
                    self.start_location, self.end_location = start_end_location_mapping[self.quadrant][self.rotation_direction][self.motion_type]
                    
    # UPDATE APPEARANCE          
        
    def update_color(self):
        if self.motion_type in ["pro", "anti"]:
            new_svg_data = self.arrow.svg_manager.set_svg_color(self.arrow.svg_file, self.arrow.color)
            self.arrow.renderer.load(new_svg_data)
            self.arrow.setSharedRenderer(self.arrow.renderer)
           
    def update_mirror(self):
        if self.is_mirrored:
            self.arrow.setTransform(QTransform().scale(-1, 1))
        else:
            self.arrow.setTransform(QTransform().scale(1, 1))
            
    def update_rotation(self):
        quadrant_to_angle = {
            "ne": 0,
            "se": 90,
            "sw": 180,
            "nw": 270
        }
        angle = quadrant_to_angle.get(self.arrow.quadrant, 0)

        self.arrow.setRotation(angle)
    