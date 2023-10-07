import os
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import pyqtSignal, QObject
from objects.arrow import Arrow
class Arrow_Manager(QObject):

    def __init__(self, graphboard_view, staff_manager):
        super().__init__()
        self.graphboard_view = graphboard_view
        self.staff_manager = staff_manager
        self.remaining_staff = {}


    def connect_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker

    def connect_graphboard_scene(self, graphboard_scene):
        self.graphboard_scene = graphboard_scene

    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def move_arrow_quadrant_wasd(self, direction):
        self.selected_arrow = self.graphboard_view.get_selected_items()[0]
        current_quadrant = self.selected_arrow.quadrant

        quadrant_mapping = {
            'up': {'se': 'ne', 'sw': 'nw'},
            'left': {'ne': 'nw', 'se': 'sw'},
            'down': {'ne': 'se', 'nw': 'sw'},
            'right': {'nw': 'ne', 'sw': 'se'}
        }

        new_quadrant = quadrant_mapping.get(direction, {}).get(current_quadrant, current_quadrant)
        self.selected_arrow.quadrant = new_quadrant

        self.selected_arrow.update_arrow_image()
        self.selected_arrow.update_arrow_position()

        self.arrow_start_end_locations = self.selected_arrow.get_arrow_start_end_locations(self.selected_arrow.svg_file)
        self.selected_arrow.start_location, self.selected_arrow.end_location = self.arrow_start_end_locations.get(os.path.basename(self.selected_arrow.svg_file), (None, None))

        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        self.info_tracker.update()
        print(self.selected_arrow.quadrant)

    def swap_motion_type(self, arrows):
        if not isinstance(arrows, list):
            arrows = [arrows]  # Make sure arrows is a list

        for arrow in arrows:
            current_svg = arrow.svg_file
            folder, base_name = os.path.split(current_svg)
            color, motion_type, rotation, quadrant, turns = base_name.split('_')[:5]

            # Determine the new motion type and folder
            if motion_type == "anti":
                new_motion_type = "pro"
                new_folder = folder.replace("anti", "pro")
            elif motion_type == "pro":
                new_motion_type = "anti"
                new_folder = folder.replace("pro", "anti")
            elif motion_type == "ghost":
                new_motion_type = "dash"
                new_folder = folder.replace("ghost", "dash")
            elif motion_type == "dash":
                new_motion_type = "ghost"
                new_folder = folder.replace("dash", "ghost")
            else:
                print(f"Unknown motion type: {motion_type}")
                continue

            # Swap the rotation direction
            if rotation == "l":
                new_rotation = "r"
            elif rotation == "r":
                new_rotation = "l"


            # Create the new SVG file name
            new_svg = os.path.join(new_folder, base_name.replace(f"{motion_type}_{rotation}_", f"{new_motion_type}_{new_rotation}_"))

            # Create a new renderer
            new_renderer = QSvgRenderer(new_svg)

            if new_renderer.isValid():
                # Update the arrow's renderer and attributes
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.motion_type = new_motion_type
                arrow.rotation_direction = new_rotation  # Update the rotation direction

                # Update the arrow's position and orientation on the graphboard_view
                arrow.update_arrow_position()
            else:
                print(f"Failed to load SVG file: {new_svg}")

        # Update the info tracker and the graphboard_view
        self.info_tracker.update()
        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        self.graphboard_view.update_letter(self.info_tracker.determine_current_letter_and_type()[0])

    def rotate_arrow(self, direction, arrows):
        for arrow in arrows:
            old_svg = f"images/arrows/{arrow.color}_{arrow.motion_type}_{arrow.rotation_direction}_{arrow.quadrant}_{arrow.turns}.svg"
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
                arrow.update_locations()
                arrow.update_quadrant()
                pos = self.graphboard_view.get_quadrant_center(new_quadrant) - arrow.boundingRect().center()
                arrow.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

    def mirror_arrow(self, arrows):
        for arrow in arrows:
            current_svg = arrow.svg_file

            if arrow.rotation_direction == "l":
                new_svg = current_svg.replace("_l_", "_r_").replace("\\l\\", "\\r\\")
                arrow.rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_svg = current_svg.replace("_r_", "_l_").replace("\\r\\", "\\l\\")
                arrow.rotation_direction = "l"
            else:
                print("mirror_arrow -- Unexpected svg_file:", current_svg)
                continue

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.update_locations()
                arrow.quadrant = arrow.quadrant.replace('.svg', '')
                arrow.update_quadrant()
                pos = self.graphboard_view.get_quadrant_center(arrow.quadrant) - arrow.boundingRect().center()
                arrow.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)
        self.info_tracker.update()
        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        self.graphboard_view.update_letter(self.info_tracker.determine_current_letter_and_type()[0])
        
    def bring_forward(self, items):
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def swap_colors(self, _):
        arrows = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow)]
        if len(arrows) >= 1:
            for arrow in arrows:
                current_svg = arrow.svg_file
                base_name = os.path.basename(current_svg)
                color, motion_type, rotation, quadrant = base_name.split('_')[:4]
                if color == "red":
                    new_color = "blue"
                elif color == "blue":
                    new_color = "red"
                else:
                    print("swap_colors - Unexpected color:", color)
                    continue
                new_svg = current_svg.replace(color, new_color)
                new_renderer = QSvgRenderer(new_svg)
                if new_renderer.isValid():
                    arrow.setSharedRenderer(new_renderer)
                    arrow.svg_file = new_svg
                    arrow.color = new_color
                else:
                    print("Failed to load SVG file:", new_svg)
        else:
            print("Cannot swap colors with no arrows on the graphboard_view.")
            
    def selectAll(self):
        for item in self.graphboard_view.items():
            #if item is an arrow
            if isinstance(item, Arrow):
                item.setSelected(True)
    
    def deselectAll(self):
        for item in self.graphboard_view.selectedItems():
            item.setSelected(False)

    def connect_to_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.selected_items_len = len(graphboard_view.get_selected_items())

    def delete_staff(self, staffs):
        if staffs:
            for staff in staffs:
                # Step 1: Identify and remove associated ghost arrows
                ghost_arrow = staff.get_arrow()  # Assuming you have a method that returns the associated ghost arrow
                if ghost_arrow:
                    self.graphboard_view.scene().removeItem(ghost_arrow)
                    print(f"Ghost arrow for {staff.color} staff deleted")
                
                # Remove the staff
                staff.hide()
                self.graphboard_view.scene().removeItem(staff)
                print(f"{staff.color} staff deleted")
                
                # Step 3: Update the info tracker
                
                self.info_tracker.update()
                self.graphboard_view.update_letter(self.info_tracker.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")

    def delete_arrow(self, selected_items):
        for arrow in selected_items:
            if isinstance(arrow, Arrow):
                # Create a ghost arrow with the same attributes
                ghost_arrow = Arrow(None, arrow.graphboard_view, arrow.info_tracker, arrow.svg_manager, self, 'static', arrow.staff_manager)

                attributes = {
                    'color': arrow.color,
                    'quadrant': 'None',
                    'rotation_direction': 'None',
                    'motion_type': "static",
                    'start_location': arrow.end_location,
                    'end_location': arrow.end_location,
                    'turns': arrow.turns
                }

                ghost_arrow.set_attributes(attributes)

                # ghost_arrow.setVisible(False)  # Make it invisible

                # Associate the ghost arrow with the staff
                staff = arrow.get_staff()
                staff.set_arrow(ghost_arrow)
                
                # Add the ghost arrow to the scene (it won't be visible)
                self.graphboard_scene.addItem(ghost_arrow)
                
                # Remove the original arrow
                self.graphboard_scene.removeItem(arrow)
                self.info_tracker.update()
        else:
            print("No items selected")
            


         