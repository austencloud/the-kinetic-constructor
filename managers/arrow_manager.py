import os
import random
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import  QObject
from objects.arrow import Arrow
from data import ARROW_START_END_LOCATIONS
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QDrag
from views.graphboard_view import Graphboard_View
from managers.json_manager import Json_Manager
from settings import GRID_PADDING, ARROW_ADJUSTMENT_DISTANCE
class Arrow_Manager(QObject):
    def __init__(self, arrow, graphboard_view, staff_manager):
        super().__init__()
        self.graphboard_view = graphboard_view
        self.staff_manager = staff_manager
        self.remaining_staff = {}
        self.dragging_arrow = None
        self.drag_offset = QPointF(0, 0)  
        self.timer = QTimer()
        self.json_manager = Json_Manager(None)
        self.letters = self.json_manager.load_all_letters()

        self.timer.timeout.connect(self.update_pixmap)
        
    ### CONNECTORS ###

    def connect_arrow(self, arrow):
        self.arrow = arrow

    def connect_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker



    def connect_to_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.graphboard_scene = graphboard_view.scene()

    ### ARROW MANIUPLATION ###

    def move_arrow_quadrant_wasd(self, direction, arrow):
        self.selected_arrow = arrow
        current_quadrant = self.selected_arrow.quadrant

        quadrant_mapping = {
            'up': {'se': 'ne', 'sw': 'nw'},
            'left': {'ne': 'nw', 'se': 'sw'},
            'down': {'ne': 'se', 'nw': 'sw'},
            'right': {'nw': 'ne', 'sw': 'se'}
        }

        new_quadrant = quadrant_mapping.get(direction, {}).get(current_quadrant, current_quadrant)
        self.selected_arrow.quadrant = new_quadrant

        self.update_arrow_image(self.selected_arrow)
        self.arrow.update_attributes()
        self.set_optimal_arrow_pos(self.graphboard_view.get_arrows())
        self.info_tracker.update()

    def swap_motion_type(self, arrows):
        if not isinstance(arrows, list):
            arrows = [arrows]  

        for arrow in arrows:
            current_svg = arrow.svg_file
            folder, base_name = os.path.split(current_svg)

            if arrow.motion_type == "anti":
                new_motion_type = "pro"
                new_folder = folder.replace("anti", "pro")
            elif arrow.motion_type == "pro":
                new_motion_type = "anti"
                new_folder = folder.replace("pro", "anti")
            else:
                print(f"Unknown motion type: {self.motion_type}")
                continue

            if arrow.rotation_direction == "l":
                new_rotation_direction = "r"
            elif arrow.rotation_direction == "r":
                new_rotation_direction = "l"
            new_svg = os.path.join(new_folder, base_name.replace(f"{arrow.motion_type}_{arrow.rotation_direction}_", f"{new_motion_type}_{new_rotation_direction}_"))
            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.motion_type = new_motion_type
                arrow.rotation_direction = new_rotation_direction 
                self.set_optimal_arrow_pos(self.graphboard_view.get_arrows())
            else:
                print(f"Failed to load SVG file: {new_svg}")

        # Update the info tracker and the graphboard_view
        self.info_tracker.update()

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
                self.update_arrow_position(arrow, self.graphboard_view)
                self.info_tracker.update()
            else:
                print("Failed to load SVG file:", new_svg)

    def mirror_arrow(self, arrows):
        for arrow in arrows:
            current_svg = arrow.svg_file

            if arrow.rotation_direction == "l":
                new_svg = current_svg.replace("_l_", "_r_").replace("\\l\\", "\\r\\")
            elif arrow.rotation_direction == "r":
                new_svg = current_svg.replace("_r_", "_l_").replace("\\r\\", "\\l\\")
            else:
                print("mirror_arrow -- Unexpected svg_file:", current_svg)
                continue

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                arrow.setSharedRenderer(new_renderer)
                arrow.svg_file = new_svg
                arrow.quadrant = arrow.quadrant.replace('.svg', '')
                arrow.update_attributes()
                self.set_optimal_arrow_pos(self.graphboard_view.get_arrows())
            else:
                print("Failed to load SVG file:", new_svg)
                
        self.info_tracker.update()
        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        
    def bring_forward(self, items):
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

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
                if arrow.motion_type == "pro" or arrow.motion_type == "anti":
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

        else:
            print("Cannot swap colors with no arrows on the graphboard_view.")
            
        self.info_tracker.update()
        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        
        ### UPDATERS ###
        
    def update_arrow_position(self, arrow, graphboard_view):
        current_arrows = graphboard_view.get_arrows()
        letter = self.info_tracker.determine_current_letter_and_type()[0]
        if letter is not None:
            self.set_optimal_arrow_pos(current_arrows)
        elif letter is None:
            self.set_default_arrow_pos(arrow)
        
    def find_optimal_locations(self, current_state, combinations):
        for inner_list in combinations:
            if self.compare_states(current_state, inner_list):
                optimal_locations = next((d for d in inner_list if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
                if optimal_locations:
                    return optimal_locations
        return None
    
    def compare_states(self, current_state, candidate_state):
        # Convert candidate_state to a format similar to current_state for easier comparison
        candidate_state_dict = {
            'arrows': [],
            'staffs': [],
            'grid': None
        }
        
        for entry in candidate_state:
            if 'color' in entry and 'motion_type' in entry:
                candidate_state_dict['arrows'].append({
                    'color': entry['color'],
                    'quadrant': entry['quadrant'],
                    'rotation_direction': entry['rotation_direction'],
                    # Add other attributes as needed
                })
            elif 'motion_type' in entry and entry['motion_type'] == 'static':
                candidate_state_dict['staffs'].append({
                    # Add attributes as needed
                })
            # Add conditions for grid if needed

        # Now compare the two states
        if len(current_state['arrows']) != len(candidate_state_dict['arrows']):
            return False
        
        for arrow in current_state['arrows']:
            matching_arrows = [candidate_arrow for candidate_arrow in candidate_state_dict['arrows']
                            if all(arrow.get(key) == candidate_arrow.get(key) for key in ['color', 'quadrant', 'rotation_direction'])]
            if not matching_arrows:
                return False

        return True

    def set_optimal_arrow_pos(self, current_arrows):
        current_state = self.graphboard_view.get_state()  # Implement this function to get the current state
        current_letter = self.info_tracker.determine_current_letter_and_type()[0]
        if current_letter is not None:
            combinations = self.letters[current_letter]  # Assuming json_data contains your JSON data
            for arrow in current_arrows:
                optimal_locations = self.find_optimal_locations(current_state, combinations)
                if optimal_locations:
                    optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
                    if optimal_location:
                        pos = QPointF(optimal_location['x'], optimal_location['y']) - arrow.boundingRect().center()
                        arrow.setPos(pos)  
                    else:
                        self.set_default_arrow_pos(arrow)
                else:
                    self.set_default_arrow_pos(arrow)
        else:
            for arrow in current_arrows:
                self.set_default_arrow_pos(arrow)

    def set_default_arrow_pos(self, arrow):
        pos = self.graphboard_view.get_quadrant_center(arrow.quadrant) - arrow.boundingRect().center()
        if arrow.quadrant == 'ne':
            pos += QPointF(ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'se':
            pos += QPointF(ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'sw':
            pos += QPointF(-ARROW_ADJUSTMENT_DISTANCE, ARROW_ADJUSTMENT_DISTANCE)
        elif arrow.quadrant == 'nw':
            pos += QPointF(-ARROW_ADJUSTMENT_DISTANCE, -ARROW_ADJUSTMENT_DISTANCE)
            
        arrow.setPos(pos + QPointF(GRID_PADDING, GRID_PADDING))
        
    def update_arrow_image(self, arrow):
        if arrow.motion_type == 'pro' or arrow.motion_type == 'anti':
            new_filename = f"images\\arrows\\shift\\{arrow.motion_type}\\{arrow.color}_{arrow.motion_type}_{arrow.rotation_direction}_{arrow.quadrant}_{arrow.turns}.svg"
            if os.path.isfile(new_filename):
                arrow.svg_file = new_filename
                arrow.setSharedRenderer(arrow.svg_manager.get_renderer(new_filename))
            else:
                print(f"File {new_filename} does not exist")
        
    ### SELECTION ###    
    
    def select_all_arrows(self):
        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                ghost_arrow = staff.get_arrow()
                if ghost_arrow:
                    self.graphboard_view.scene().removeItem(ghost_arrow)
                    print(f"Ghost arrow for {staff.color} staff deleted")
            
                staff.hide()
                self.graphboard_view.scene().removeItem(staff)
                print(f"{staff.color} staff deleted")
                
                self.info_tracker.update()
                self.graphboard_view.update_letter(self.info_tracker.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")

    def delete_arrow(self, deleted_arrows):
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                ghost_arrow = Arrow(None, arrow.graphboard_view, arrow.info_tracker, arrow.svg_manager, self, 'static', arrow.staff_manager, None)
                ghost_arrow.set_static_attributes_from_deleted_arrow(arrow)
                self.graphboard_scene.addItem(ghost_arrow)
                self.graphboard_scene.removeItem(arrow)
                self.info_tracker.update()
        else:
            print("No items selected")

    def prepare_dragging(self, event):
        if isinstance(self.graphboard_view, Graphboard_View):
            self.drag_start_position = event.pos()
            self.graphboard_view.setFocus()
            draggable_items = [item for item in self.graphboard_view.items(event.pos().toPoint()) if item.flags() & QGraphicsItem.ItemIsMovable]

            if draggable_items:
                item = draggable_items[0]
                self.dragging_arrow = item
                self.drag_offset = self.graphboard_view.mapToScene(event.pos().toPoint()) - self.dragging_arrow.pos()
            else:
                self.graphboard_view.clear_selection()
                self.dragging_arrow = None

            return self.dragging_arrow, self.drag_offset

    def exec_(self, *args, **kwargs):
        self.timer.start(100)
        drag = QDrag(self.graphboard_view)
        result = drag.exec_(*args, **kwargs)
        self.timer.stop()
        return result

    def update_pixmap(self):
        if self.dragging_arrow:
            new_pos = self.dragging_arrow.pos()
            new_quadrant = self.graphboard_view.get_graphboard_quadrants(new_pos) 
            
            if self.dragging_arrow.quadrant != new_quadrant:
                self.dragging_arrow.update_arrow_for_new_quadrant(new_quadrant)
                self.info_tracker.update()  # Assuming info_tracker is accessible

        new_svg = f'images\\arrows\\red\\r\\anti\\red_anti_r_{new_quadrant}.svg'
        arrow_renderer = QSvgRenderer(new_svg)
        self.dragging_arrow.setSharedRenderer(arrow_renderer)

        if arrow_renderer.isValid():
            pixmap = QPixmap(self.dragging_arrow.pixmap().size())
            painter = QPainter(pixmap)
            arrow_renderer.render(painter)
            painter.end()
            self.dragging_arrow.setPixmap(pixmap)