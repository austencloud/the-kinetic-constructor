from objects.arrow.arrow import Arrow
from PyQt6.QtCore import QByteArray
from lxml import etree
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform


class ArrowManipulator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager
        

    def update_arrow_and_staff(self, arrow, arrow_dict, staff_dict):
        staff = arrow.staff
        arrow.attributes.update_attributes(arrow, arrow_dict)
        staff.attributes.update_attributes(staff, staff_dict)
        staff.setPos(arrow.view.staff_handler.staff_xy_locations[staff.location])

    def finalize_manipulation(self, arrow):
        self.graphboard_staff_handler.update_staff_key(arrow.staff)
        self.arrow_manager.arrow_positioner.update_arrow_position(
            self.arrow_manager.graphboard_view
        )
        arrow.update_appearance()
        self.arrow_manager.info_frame.update()
        arrow.view.info_handler.update()
        arrow.staff.update_appearance()


    def move_arrow_quadrant_wasd(self, direction, selected_arrow):
        wasd_quadrant_mapping = {
            "up": {"se": "ne", "sw": "nw"},
            "left": {"ne": "nw", "se": "sw"},
            "down": {"ne": "se", "nw": "sw"},
            "right": {"nw": "ne", "sw": "se"},
        }
        selected_arrow = selected_arrow
        current_quadrant = selected_arrow.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(
            current_quadrant, current_quadrant
        )
        selected_arrow.quadrant = new_quadrant
        (
            new_start_location,
            new_end_location,
        ) = selected_arrow.attributes.get_start_end_locations(
            selected_arrow.motion_type, selected_arrow.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            "color": selected_arrow.color,
            "motion_type": selected_arrow.motion_type,
            "quadrant": new_quadrant,
            "rotation_direction": selected_arrow.rotation_direction,
            "start_location": new_start_location,
            "end_location": new_end_location,
            "turns": selected_arrow.turns,
        }

        updated_staff_dict = {
            "color": selected_arrow.color,
            "location": new_end_location,
            "layer": 1,
        }

        self.update_arrow_and_staff(
            selected_arrow, updated_arrow_dict, updated_staff_dict
        )
        self.finalize_manipulation(selected_arrow)

    def rotate_arrow(self, rotation_direction, arrows):
        if arrows:
            for arrow in arrows:
                quadrants = ["ne", "se", "sw", "nw"]
                current_quadrant_index = quadrants.index(arrow.quadrant)
                new_quadrant_index = (
                    (current_quadrant_index + 1) % 4
                    if rotation_direction == "right"
                    else (current_quadrant_index - 1) % 4
                )
                new_quadrant = quadrants[new_quadrant_index]
                (
                    new_start_location,
                    new_end_location,
                ) = arrow.attributes.get_start_end_locations(
                    arrow.motion_type, arrow.rotation_direction, new_quadrant
                )

                updated_arrow_dict = {
                    "color": arrow.color,
                    "motion_type": arrow.motion_type,
                    "quadrant": new_quadrant,
                    "rotation_direction": arrow.rotation_direction,
                    "start_location": new_start_location,
                    "end_location": new_end_location,
                    "turns": arrow.turns,
                }

                updated_staff_dict = {
                    "color": arrow.color,
                    "location": new_end_location,
                    "layer": 1,
                }

            self.update_arrow_and_staff(arrow, updated_arrow_dict, updated_staff_dict)
            self.finalize_manipulation(arrow)

    def mirror_arrow(self, arrows):
        for arrow in arrows:
            if arrow.is_mirrored:
                arrow.is_mirrored = False
                original_svg_data = arrow.get_svg_data(arrow.svg_file)
                arrow.renderer.load(QByteArray(original_svg_data))  # No need to encode

                # Reset the transformation matrix to the identity matrix to unmirror the arrow
                arrow.resetTransform()

            else:
                arrow.is_mirrored = True

                # Get the center of the arrow
                center_x = arrow.boundingRect().width() / 2
                center_y = arrow.boundingRect().height() / 2

                # Create a QTransform object and configure it for mirroring around the center
                transform = QTransform()
                transform.translate(center_x, center_y)
                transform.scale(-1, 1)
                transform.translate(-center_x, -center_y)

                # Apply the transform to the arrow
                arrow.setTransform(transform)

            if arrow.rotation_direction == "l":
                new_rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_rotation_direction = "l"

            old_start_location = arrow.start_location
            old_end_location = arrow.end_location
            arrow.start_location = old_end_location
            arrow.end_location = old_start_location

            arrow.update_appearance()

            new_arrow = {
                "color": arrow.color,
                "motion_type": arrow.motion_type,
                "quadrant": arrow.quadrant,
                "rotation_direction": new_rotation_direction,
                "start_location": arrow.start_location,
                "end_location": arrow.end_location,
                "turns": arrow.turns,
            }

            arrow.attributes.update_attributes(arrow, new_arrow)
            self.finalize_manipulation(arrow)
            self.arrow_manager.arrow_positioner.update_arrow_position(arrow.view)
            arrow.update()

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

            new_arrow_dict = {
                "color": arrow.color,
                "motion_type": new_motion_type,
                "quadrant": arrow.quadrant,
                "rotation_direction": new_rotation_direction,
                "start_location": arrow.start_location,
                "end_location": arrow.end_location,
                "turns": arrow.turns,
            }

            staff_dict = {
                "color": arrow.color,
                "location": arrow.end_location,
                "layer": 1,
            }

            arrow.svg_file = (
                f"resources/images/arrows/shift/{new_motion_type}_{arrow.turns}.svg"
            )
            arrow.initialize_svg_renderer(arrow.svg_file)

            self.update_arrow_and_staff(arrow, new_arrow_dict, staff_dict)
            self.finalize_manipulation(arrow)

            arrow.attributes.update_attributes(arrow, new_arrow_dict)
            arrow.update_appearance()

            arrow.view.info_handler.update()

            self.arrow_manager.info_frame.update()

    def swap_colors(self):
        arrows = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow)]
        
        if len(arrows) >= 1:
            for arrow in arrows:
                print(f"Before swap: Arrow color: {arrow.color}, Staff color: {arrow.staff.color}")
                
                if arrow.color == "red":
                    new_color = "blue"
                elif arrow.color == "blue":
                    new_color = "red"
                else:
                    print("swap_colors - Unexpected color:", arrow.color)
                    continue

                arrow.color = new_color
                arrow.staff.color = new_color
                
                arrow.update_appearance()
                arrow.staff.update_appearance()
                print(f"After swap: Arrow color: {arrow.color}, Staff color: {arrow.staff.color}")
                self.finalize_manipulation(arrow)
