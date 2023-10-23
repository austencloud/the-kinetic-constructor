from PyQt5.QtSvg import QSvgRenderer

class ArrowManipulator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def move_arrow_quadrant_wasd(self, direction, selected_arrow):
        self.selected_arrow = selected_arrow
        current_quadrant = self.selected_arrow.quadrant

        quadrant_mapping = {
            'up': {'se': 'ne', 'sw': 'nw'},
            'left': {'ne': 'nw', 'se': 'sw'},
            'down': {'ne': 'se', 'nw': 'sw'},
            'right': {'nw': 'ne', 'sw': 'se'}
        }

        new_quadrant = quadrant_mapping.get(direction, {}).get(current_quadrant, current_quadrant)
        self.selected_arrow.quadrant = new_quadrant
        self.selected_arrow.update_attributes()
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
                self.arrow_manager.update_arrow_position(self.arrow_manager.graphboard_view)
                self.arrow_manager.info_frame.update()
            else:
                print("Failed to load SVG file:", new_svg)

    def mirror_arrow(self, arrows):
        for arrow in arrows:
            if arrow.is_mirrored:
                arrow.is_mirrored = False
            else:
                arrow.is_mirrored = True
            arrow.mirror()

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

            # swap out instances of pro and anti with each other in the arrow svg file
            new_svg = arrow.svg_file.replace(arrow.motion_type, new_motion_type)
            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.update_color()

            if arrow.rotation_direction == "l":
                new_rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_rotation_direction = "l"

            arrow.motion_type = new_motion_type
            arrow.rotation_direction = new_rotation_direction
            arrow.update_appearance()
            self.arrow_manager.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)

        # Update the info frame and the graphboard_view
        self.arrow_manager.info_frame.update()
