from PyQt6.QtGui import QTransform
from settings.string_constants import *


class Manipulators:
    def __init__(self, graphboard):
        self.graphboard = graphboard

    def update_arrow_and_staff(self, arrow, arrow_dict, staff_dict):
        staff = arrow.staff
        arrow.update_attributes(arrow_dict)
        staff.update_attributes(staff_dict)
        
    def move_wasd(self, direction, selected_arrow):
        wasd_quadrant_mapping = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
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
        ) = selected_arrow.get_start_end_locations(
            selected_arrow.motion_type, selected_arrow.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: selected_arrow.color,
            MOTION_TYPE: selected_arrow.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: selected_arrow.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: selected_arrow.turns,
        }

        updated_staff_dict = {
            COLOR: selected_arrow.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update_arrow_and_staff(
            selected_arrow, updated_arrow_dict, updated_staff_dict
        )
        selected_arrow.update_appearance()
        selected_arrow.staff.update_appearance()
        self.graphboard.update()

    def rotate_arrow(self, rotation_direction, arrows):
        if arrows:
            for arrow in arrows:
                quadrants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
                current_quadrant_index = quadrants.index(arrow.quadrant)
                new_quadrant_index = (
                    (current_quadrant_index + 1) % 4
                    if rotation_direction == RIGHT
                    else (current_quadrant_index - 1) % 4
                )
                new_quadrant = quadrants[new_quadrant_index]
                (
                    new_start_location,
                    new_end_location,
                ) = arrow.get_start_end_locations(
                    arrow.motion_type, arrow.rotation_direction, new_quadrant
                )

                updated_arrow_dict = {
                    COLOR: arrow.color,
                    MOTION_TYPE: arrow.motion_type,
                    QUADRANT: new_quadrant,
                    ROTATION_DIRECTION: arrow.rotation_direction,
                    START_LOCATION: new_start_location,
                    END_LOCATION: new_end_location,
                    TURNS: arrow.turns,
                }

                updated_staff_dict = {
                    COLOR: arrow.color,
                    LOCATION: new_end_location,
                    LAYER: 1,
                }

            self.update_arrow_and_staff(arrow, updated_arrow_dict, updated_staff_dict)
            self.graphboard.update()

    def mirror_arrow(self, arrows, color):
        arrows = [arrow for arrow in arrows if arrow.color == color]
        for arrow in arrows:
            if arrow.is_mirrored:
                arrow.is_mirrored = False
            else:
                arrow.is_mirrored = True

            center_x = arrow.boundingRect().width() / 2
            center_y = arrow.boundingRect().height() / 2

            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.scale(-1, 1)
            transform.translate(-center_x, -center_y)

            arrow.setTransform(transform)

            if arrow.rotation_direction == COUNTER_CLOCKWISE:
                new_rotation_direction = CLOCKWISE
            elif arrow.rotation_direction == CLOCKWISE:
                new_rotation_direction = COUNTER_CLOCKWISE

            old_start_location = arrow.start_location
            old_end_location = arrow.end_location
            new_start_location = old_end_location
            new_end_location = old_start_location

            new_arrow_dict = {
                COLOR: arrow.color,
                MOTION_TYPE: arrow.motion_type,
                QUADRANT: arrow.quadrant,
                ROTATION_DIRECTION: new_rotation_direction,
                START_LOCATION: new_start_location,
                END_LOCATION: new_end_location,
                TURNS: arrow.turns,
            }

            arrow.staff.location = new_end_location
            arrow.update_attributes(new_arrow_dict)
            self.graphboard.update()

    def swap_motion_type(self, arrows, color):
        from objects.arrow.arrow import Arrow

        arrows = [arrow for arrow in arrows if arrow.color == color]
        if not isinstance(arrows, list):
            arrows = [arrows]

        arrows = [arrow for arrow in arrows if isinstance(arrow, Arrow)]

        for arrow in arrows:
            if arrow.motion_type == ANTI:
                new_motion_type = PRO
            elif arrow.motion_type == PRO:
                new_motion_type = ANTI
            else:
                continue

            if arrow.rotation_direction == COUNTER_CLOCKWISE:
                new_rotation_direction = CLOCKWISE
            elif arrow.rotation_direction == CLOCKWISE:
                new_rotation_direction = COUNTER_CLOCKWISE

            new_arrow_dict = {
                COLOR: arrow.color,
                MOTION_TYPE: new_motion_type,
                QUADRANT: arrow.quadrant,
                ROTATION_DIRECTION: new_rotation_direction,
                START_LOCATION: arrow.start_location,
                END_LOCATION: arrow.end_location,
                TURNS: arrow.turns,
            }

            new_staff_dict = {
                COLOR: arrow.color,
                LOCATION: arrow.end_location,
                LAYER: 1,
            }

            arrow.svg_file = (
                f"resources/images/arrows/shift/{new_motion_type}_{arrow.turns}.svg"
            )
            arrow.initialize_svg_renderer(arrow.svg_file)
            arrow.update_attributes(new_arrow_dict)
            arrow.update_appearance()
            self.graphboard.update()
            self.update_arrow_and_staff(arrow, new_arrow_dict, new_staff_dict)
            self.graphboard.update()

    def swap_colors(self):
        from objects.arrow.arrow import Arrow

        current_letter = self.graphboard.get_current_letter()
        if current_letter != "G" and current_letter != "H":
            arrows = [
                item for item in self.graphboard.items() if isinstance(item, Arrow)
            ]
            if len(arrows) >= 1:
                for arrow in arrows:
                    if arrow.color == RED:
                        new_color = BLUE
                    elif arrow.color == BLUE:
                        new_color = RED
                    else:
                        continue

                    arrow.color = new_color
                    arrow.staff.color = new_color

                    arrow.update_appearance()
                    arrow.staff.update_appearance()
                    self.update()


