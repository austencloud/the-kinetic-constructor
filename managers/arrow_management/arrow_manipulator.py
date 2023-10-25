import re
import os
from PyQt6.QtCore import QByteArray
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow import Arrow
from PyQt6.QtGui import QTransform
class ArrowManipulator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def finalize_manipulation(self, selected_arrow, updated_arrow):
        selected_arrow.attributes.update_attributes_from_dict(selected_arrow, updated_arrow)
        self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
        selected_arrow.update_appearance()
        self.arrow_manager.info_frame.update()
        selected_arrow.staff.update()

    def move_arrow_quadrant_wasd(self, direction, selected_arrow):
        wasd_quadrant_mapping = {
            'up': {'se': 'ne', 'sw': 'nw'},
            'left': {'ne': 'nw', 'se': 'sw'},
            'down': {'ne': 'se', 'nw': 'sw'},
            'right': {'nw': 'ne', 'sw': 'se'}
        }
        selected_arrow = selected_arrow
        current_quadrant = selected_arrow.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(current_quadrant, current_quadrant)
        selected_arrow.quadrant = new_quadrant
        new_start_location, new_end_location = selected_arrow.attributes.get_start_end_locations(selected_arrow.motion_type, selected_arrow.rotation_direction, new_quadrant)
        
        updated_arrow = {
            'color': selected_arrow.color,
            'motion_type': selected_arrow.motion_type,
            'quadrant': new_quadrant,
            'rotation_direction': selected_arrow.rotation_direction,
            'start_location': new_start_location,
            'end_location': new_end_location,
            'turns': selected_arrow.turns
        }
        
        self.finalize_manipulation(selected_arrow, updated_arrow)


    def rotate_arrow(self, direction, arrows):
        for arrow in arrows:
            quadrants = ['ne', 'se', 'sw', 'nw']
            current_quadrant_index = quadrants.index(arrow.quadrant)
            new_quadrant_index = (current_quadrant_index + 1) % 4 if direction == "right" else (current_quadrant_index - 1) % 4
            new_quadrant = quadrants[new_quadrant_index]
            new_start_location, new_end_location = arrow.attributes.get_start_end_locations(arrow.motion_type, arrow.rotation_direction, new_quadrant)
            
            updated_arrow = {
                'color': arrow.color,
                'motion_type': arrow.motion_type,
                'quadrant': new_quadrant,
                'rotation_direction': arrow.rotation_direction,
                'start_location': new_start_location,
                'end_location': new_end_location,
                'turns': arrow.turns
                }

        self.finalize_manipulation(arrow, updated_arrow)



    def mirror_arrow(self, arrows):
        for arrow in arrows:
            original_pos = arrow.pos()
            if arrow.is_mirrored:
                arrow.is_mirrored = False
                arrow.setTransform(QTransform())
            else:
                arrow.is_mirrored = True
                arrow.setTransform(QTransform.fromScale(-1, 1))

            offset = original_pos - arrow.pos()
            arrow.setPos(arrow.pos() + offset)
            self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
            arrow.update_appearance()

    def swap_motion_type(self, arrows):
        if not isinstance(arrows, list):
            arrows = [arrows]

        for arrow in arrows:
            if arrow.motion_type == "anti":
                new_motion_type = "pro"
            elif arrow.motion_type == "pro":
                new_motion_type = "anti"
            else:
                print(f"Unknown motion type: {self.motion_type}")
                continue

            if arrow.rotation_direction == "l":
                new_rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_rotation_direction = "l"

            new_end_location = arrow.start_location
            new_start_location = arrow.end_location
            
            new_arrow_dict = {
                'color': arrow.color,
                'motion_type': new_motion_type,
                'quadrant': arrow.quadrant,
                'rotation_direction': new_rotation_direction,
                'start_location': new_end_location,
                'end_location': new_start_location,
                'turns': arrow.turns
            }

            new_arrow = self.arrow_manager.arrow_factory.create_arrow(self.arrow_manager.graphboard_view, new_arrow_dict)
            new_arrow.update_appearance()
            
            self.arrow_manager.graphboard_view.graphboard_scene.removeItem(arrow)
            self.arrow_manager.graphboard_view.graphboard_scene.addItem(new_arrow)
            

            new_arrow.view.info_manager.update()
            
        self.arrow_manager.info_frame.update()
        
    def swap_colors(self, _):
        arrows = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow)]
        if len(arrows) >= 1:
            for arrow in arrows:
                if arrow.color == "red":
                    new_color = "blue"
                elif arrow.color == "blue":
                    new_color = "red"
                else:
                    print("swap_colors - Unexpected color:", arrow.color)
                    continue

                if arrow.motion_type in ["pro", "anti"]:
                    new_svg = arrow.svg_file.replace(arrow.color, new_color)
                    new_renderer = QSvgRenderer(new_svg)

                    if new_renderer.isValid():
                        arrow.setSharedRenderer(new_renderer)
                        arrow.svg_file = new_svg
                        arrow.color = new_color
                    else:
                        print("Failed to load SVG file:", new_svg)
                elif arrow.motion_type == "static":
                    arrow.color = new_color
