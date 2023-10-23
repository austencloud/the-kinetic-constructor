import os
import random
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtCore import QObject, QByteArray, QTimer, QPointF, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QDrag, QTransform
from objects.arrow import Arrow
from settings import *


class ArrowManager(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.remaining_staff = {}
        self.dragging_arrow = None
        self.drag_offset = QPointF(0, 0)
        self.timer = QTimer()
        self.letters = main_widget.letters
        self.main_widget = main_widget

        # Initialize the helper classes
        self.arrow_manipulator = ArrowManipulator(self)
        self.arrow_positioner = ArrowPositioner(self)
        self.arrow_selector = ArrowSelector(self)
        self.arrow_factory = ArrowFactory(self)
        self.arrow_state_comparator = ArrowStateComparator(self)


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


class ArrowPositioner:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def update_arrow_position(self, graphboard_view):
        current_arrows = graphboard_view.get_arrows()
        letter = self.arrow_manager.graphboard_view.info_manager.determine_current_letter_and_type()[0]
        if letter is not None:
            self.set_optimal_arrow_pos(current_arrows)
        else:
            for arrow in current_arrows:
                self.set_default_arrow_pos(arrow)

    def set_optimal_arrow_pos(self, current_arrows):
        current_state = self.arrow_manager.graphboard_view.get_state()
        current_letter = self.arrow_manager.graphboard_view.info_manager.determine_current_letter_and_type()[0]
        if current_letter is not None:
            matching_letters = self.arrow_manager.letters[current_letter]
            optimal_locations = self.arrow_manager.arrow_state_comparator.find_optimal_locations(current_state, matching_letters)
            for arrow in current_arrows:
                if optimal_locations:
                    optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
                    if optimal_location:
                        GRID_PADDING = (self.arrow_manager.graphboard_view.width() - self.arrow_manager.graphboard_view.grid.boundingRect().width() * GRAPHBOARD_SCALE) / 2
                        pos = QPointF(optimal_location['x'] * GRAPHBOARD_SCALE, optimal_location['y'] * GRAPHBOARD_SCALE)
                        arrow.setPos(pos - QPointF(arrow.boundingRect().width()/2, arrow.boundingRect().height()/2))
                else:
                    self.set_default_arrow_pos(arrow)

    def set_default_arrow_pos(self, arrow):
        quadrant_center = self.arrow_manager.graphboard_view.get_quadrant_center(arrow.quadrant)
        pos = (quadrant_center * GRAPHBOARD_SCALE) - arrow.center
        if arrow.quadrant == 'ne':
            pos += QPointF(ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'se':
            pos += QPointF(ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'sw':
            pos += QPointF(-ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'nw':
            pos += QPointF(-ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)
        arrow.setPos(pos + QPointF(GRAPHBOARD_GRID_PADDING, GRAPHBOARD_GRID_PADDING))


class ArrowSelector:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def select_all_arrows(self):
        for item in self.arrow_manager.graphboard_view.items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                ghost_arrow = staff.arrow
                if ghost_arrow:
                    self.arrow_manager.graphboard_view.scene().removeItem(ghost_arrow)
                    print(f"Ghost arrow for {staff.color} staff deleted")

                staff.hide()
                self.arrow_manager.graphboard_view.scene().removeItem(staff)
                print(f"{staff.color} staff deleted")

                self.arrow_manager.info_frame.update()
                self.arrow_manager.graphboard_view.update_letter(self.arrow_manager.graphboard_view.info_manager.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")

    def delete_arrow(self, deleted_arrows):
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                ghost_arrow = Arrow(None, arrow.view, arrow.info_frame, arrow.svg_manager, self.arrow_manager, 'static', arrow.staff_manager, arrow.color, None, None, 0, None)
                ghost_arrow.is_ghost = True
                ghost_arrow.set_static_attributes_from_deleted_arrow(arrow)
                ghost_arrow.setScale(GRAPHBOARD_SCALE)
                self.arrow_manager.graphboard_scene.addItem(ghost_arrow)
                self.arrow_manager.graphboard_scene.removeItem(arrow)
                self.arrow_manager.info_frame.update()
        else:
            print("No items selected")


class ArrowFactory:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def create_arrow(self, base_type, color, rotation_direction, is_mirrored, turns):
        # Create an Arrow object with the given attributes
        svg_file = f"shift/{base_type}/{base_type}_{turns}.svg"
        arrow = Arrow(svg_file, ...)
        arrow.color = color
        arrow.rotation_direction = rotation_direction
        arrow.is_mirrored = is_mirrored
        arrow.update_appearance()
        return arrow


class ArrowStateComparator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def compare_states(self, current_state, candidate_state):
        # Convert candidate_state to a format similar to current_state for easier comparison
        candidate_state_dict = {
            'arrows': []
        }

        for entry in candidate_state:
            if 'color' in entry and 'motion_type' in entry:
                candidate_state_dict['arrows'].append({
                    'color': entry['color'],
                    'motion_type': entry['motion_type'],
                    'rotation_direction': entry['rotation_direction'],
                    'quadrant': entry['quadrant'],
                    'turns': entry.get('turns', 0)
                })

        # Now compare the two states
        if len(current_state['arrows']) != len(candidate_state_dict['arrows']):
            return False

        for arrow in current_state['arrows']:
            matching_arrows = [candidate_arrow for candidate_arrow in candidate_state_dict['arrows']
                               if all(arrow.get(key) == candidate_arrow.get(key) for key in ['color', 'motion_type', 'quadrant', 'rotation_direction'])]
            if not matching_arrows:
                return False

        return True

    def find_optimal_locations(self, current_state, matching_letters):
        for variations in matching_letters:
            if self.compare_states(current_state, variations):
                return next((d for d in variations if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
        return None

