import re
import os
from PyQt6.QtCore import QByteArray
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow import Arrow
from PyQt6.QtGui import QTransform
class ArrowManipulator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def move_arrow_quadrant_wasd(self, direction, selected_arrow):
        wasd_quadrant_mapping = {
            'up': {'se': 'ne', 'sw': 'nw'},
            'left': {'ne': 'nw', 'se': 'sw'},
            'down': {'ne': 'se', 'nw': 'sw'},
            'right': {'nw': 'ne', 'sw': 'se'}
        }
        self.selected_arrow = selected_arrow
        current_quadrant = self.selected_arrow.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(current_quadrant, current_quadrant)
        self.selected_arrow.quadrant = new_quadrant
        
        updated_arrow = {
            'color': self.selected_arrow.color,
            'motion_type': self.selected_arrow.motion_type,
            'quadrant': new_quadrant,
            'rotation_direction': self.selected_arrow.rotation_direction,
            'start_location': self.selected_arrow.start_location,
            'end_location': self.selected_arrow.end_location,
            'turns': self.selected_arrow.turns
        }
        
        self.selected_arrow.attributes.update(updated_arrow)
        self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
        self.arrow_manager.info_frame.update()

    def rotate_arrow(self, direction, arrows):
        for arrow in arrows:
            quadrants = ['ne', 'se', 'sw', 'nw']
            current_quadrant_index = quadrants.index(arrow.quadrant)
            if direction == "right":
                new_quadrant_index = (current_quadrant_index + 1) % 4
            else:  # direction == "left"
                new_quadrant_index = (current_quadrant_index - 1) % 4
            new_quadrant = quadrants[new_quadrant_index]
            new_svg = arrow.svg_file.replace(arrow.quadrant, new_quadrant)

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.update_attributes()
                self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
                self.arrow_manager.info_frame.update()
                arrow.update_appearance()
            else:
                print("Failed to load SVG file:", new_svg)


    def mirror_arrow(self, arrows):
        for arrow in arrows:
            # Step 1: Store the position of the arrow in the scene
            original_pos = arrow.pos()

            # Step 2: Apply transformations
            if arrow.is_mirrored:
                arrow.is_mirrored = False
                arrow.setTransform(QTransform())
            else:
                arrow.is_mirrored = True
                arrow.setTransform(QTransform.fromScale(-1, 1))

            # Step 3: Calculate the offset
            offset = original_pos - arrow.pos()

            # Step 4: Reposition the arrow
            arrow.setPos(arrow.pos() + offset)

            # Update the arrow's appearance and position according to your logic
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

            new_svg = arrow.svg_file.replace(arrow.motion_type, new_motion_type)
            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg

            if arrow.rotation_direction == "l":
                new_rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_rotation_direction = "l"

            arrow.motion_type = new_motion_type
            arrow.rotation_direction = new_rotation_direction
            arrow.update_appearance()
            self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
            
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
