
import os
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QCursor, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView, QGraphicsItem, QGraphicsScene, QSizePolicy, QToolTip, QFrame
from objects.staff.staff import Staff
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from constants import GRAPHBOARD_SCALE, GRAPHBOARD_WIDTH, GRAPHBOARD_HEIGHT, VERTICAL_OFFSET, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST, STATIC, PRO, ANTI
from widgets.graph_editor.graphboard.graphboard_staff_handler import GraphboardStaffHandler
from widgets.graph_editor.graphboard.graphboard_info_handler import GraphboardInfoHandler
from widgets.graph_editor.graphboard.graphboard_context_menu_handler import GraphboardContextMenuHandler
from utilities.export_handler import ExportHandler
from data.letter_types import letter_types
class GraphboardView(QGraphicsView):
    def __init__(self, main_widget, graph_editor_widget):
        super().__init__(graph_editor_widget)
        self.init_ui()
        self.init_scene(main_widget)
        self.init_managers(main_widget)
        self.init_grid()
        self.init_letter_renderers()

    # INIT #
    
    def init_ui(self):
        self.setAcceptDrops(True)
        self.setInteractive(True)
        self.dragging = None
        self.temp_arrow = None
        self.temp_staff = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setFixedSize(int(GRAPHBOARD_WIDTH), int(GRAPHBOARD_HEIGHT))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)

    def init_scene(self, main_widget):
        self.graphboard_scene = QGraphicsScene()
        self.setScene(self.graphboard_scene)
        self.main_widget = main_widget
        self.grid = Grid('images/grid/grid.svg')
        self.grid.setScale(GRAPHBOARD_SCALE)
        self.scene().setSceneRect(0, 0, int(GRAPHBOARD_WIDTH), int(GRAPHBOARD_HEIGHT))
        self.VERTICAL_OFFSET = (self.height() - self.width()) / 2
        self.view_scale = GRAPHBOARD_SCALE
        # Add the grid and letter item to the scene
        self.graphboard_scene.addItem(self.grid)

    def init_managers(self, main_widget):
        self.info_manager = GraphboardInfoHandler(main_widget, self)
        self.staff_manager = GraphboardStaffHandler(main_widget, self.graphboard_scene)
        self.export_manager = ExportHandler(self.staff_manager, self.grid, self)
        self.context_menu_manager = GraphboardContextMenuHandler(self)
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manager.graphboard_view = self
        self.arrow_factory = self.arrow_manager.arrow_factory
        self.staff_factory = self.staff_manager.staff_factory
        
    def init_grid(self):
        transform = QTransform()
        graphboard_size = self.frameSize()

        grid_position = QPointF((graphboard_size.width() - self.grid.boundingRect().width() * GRAPHBOARD_SCALE) / 2,
                                (graphboard_size.height() - self.grid.boundingRect().height() * GRAPHBOARD_SCALE) / 2 - (VERTICAL_OFFSET))

        transform.translate(grid_position.x(), grid_position.y())
        self.grid.setTransform(transform)

    def init_letter_renderers(self):
        self.letter_renderers = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUV':
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    break
            self.letter_renderers[letter] = QSvgRenderer(f'images/letters/{letter_type}/{letter}.svg')
        self.letter_item = QGraphicsSvgItem()

        self.main_widget.graphboard_scene = self.graphboard_scene
        self.graphboard_scene.addItem(self.letter_item)


    ### EVENTS ###

    def mousePressEvent(self, event):
        self.setFocus()
        items = self.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.clear_selection()
                items[0].setSelected(True)
        else:
            self.clear_selection()
        super().mousePressEvent(event)
        
        # Check if any item got selected after calling the parent class's method
        if items and not items[0].isSelected():
            items[0].setSelected(True)

    def dragMoveEvent(self, event):
        current_quadrant = self.get_graphboard_quadrants(self.mapToScene(event.position().toPoint()))  # Changed event.pos() to event.position()

        dropped_svg = event.mimeData().text()
        base_name = os.path.basename(dropped_svg)
        motion_type = base_name.split('_')[0]
        turns = base_name.split('_')[1].split('.')[0]
        rotation_direction = 'r' if motion_type == PRO else 'l'
        color = event.mimeData().data("color").data().decode()  # Retrieve the color
        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                if arrow.color == color:
                    event.ignore()
                    QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
                    return
        event.accept()
        QToolTip.hideText() 
        
        temp_arrow_dict = {
            'color': color,
            'motion_type': motion_type,
            'rotation_direction': rotation_direction,
            'quadrant': current_quadrant,
            'start_location': None,
            'end_location': None,
            'turns': turns
        }
        
        if self.temp_arrow is None:
            self.temp_arrow = self.arrow_factory.create_arrow(self, temp_arrow_dict)
            self.temp_arrow.color = event.mimeData().data("color").data().decode() 
            self.temp_arrow.start_location, self.temp_arrow.end_location = self.temp_arrow.attributes.get_start_end_locations(motion_type, rotation_direction, current_quadrant)
           
            temp_staff_dict = {
                'color': color,
                'location': self.temp_arrow.end_location,
                'layer': 1
            } 
        

            self.temp_staff = self.staff_factory.create_staff(self.graphboard_scene, temp_staff_dict)
            self.graphboard_scene.addItem(self.temp_staff)
            
    
        # Update the temporary arrow and staff
        self.update_dragged_arrow_and_staff(current_quadrant, self.temp_arrow, self.temp_staff)

    # Update the temporary arrow and staff
    def update_dragged_arrow_and_staff(self, current_quadrant, temp_arrow, temp_staff):
        temp_arrow.quadrant = current_quadrant  # Update the quadrant of the temporary arrow
        temp_arrow.update_rotation()  # Update the rotation based on the new quadrant
        temp_arrow.update_appearance()  # Update the appearance based on the new quadrant
        # Update the staff's position based on the new end location of the temporary arrow
        temp_arrow.start_location, temp_arrow.end_location = temp_arrow.attributes.get_start_end_locations(
            temp_arrow.motion_type, temp_arrow.rotation_direction, current_quadrant)
        temp_staff_dict = {
            'color': temp_arrow.color,
            'location': temp_arrow.end_location,
            'layer': 1
        }
        temp_staff.attributes.update_attributes(temp_staff, temp_staff_dict)
        temp_staff.update_appearance()
        temp_staff.setPos(self.staff_manager.staff_xy_locations[temp_staff_dict['location']])

    def dropEvent(self, event):
        arrow = None
        self.setFocus()
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()
        dropped_arrow_svg_path = event.mimeData().text()
        dropped_arrow_color = event.mimeData().data("color").data().decode()  # Retrieve the color
        parts = os.path.basename(dropped_arrow_svg_path).split('_')
        dropped_arrow_svg_motion_type = parts[0]
        dropped_arrow_turns = parts[1].split('.')[0]
        
        if dropped_arrow_svg_motion_type == PRO:
            dropped_arrow_rotation_direction = 'r'
        elif dropped_arrow_svg_motion_type == ANTI:
            dropped_arrow_rotation_direction = 'l'
            
        self.mouse_pos = self.mapToScene(event.position().toPoint()) 
        dropped_arrow_quadrant = self.get_graphboard_quadrants(self.mouse_pos)
        dropped_arrow_start_location, dropped_arrow_end_location = self.arrow_manager.arrow_attributes.get_start_end_locations(dropped_arrow_svg_motion_type, dropped_arrow_rotation_direction, dropped_arrow_quadrant)
        
        dropped_arrow = {
            'color': dropped_arrow_color,
            'motion_type': dropped_arrow_svg_motion_type,
            'rotation_direction': dropped_arrow_rotation_direction,
            'quadrant': dropped_arrow_quadrant,
            'start_location': dropped_arrow_start_location,
            'end_location': dropped_arrow_end_location,
            'turns': dropped_arrow_turns
        }
        
        dropped_staff = {
            'color': dropped_arrow_color,
            'location': dropped_arrow_end_location,
            'layer': 1
        } 
        
        # Check for existing arrows and staffs of the same color
        existing_arrows = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow) and item.color == dropped_arrow_color]
        existing_staffs = [item for item in self.graphboard_scene.items() if isinstance(item, Staff) and item.color == dropped_arrow_color]

        # Case 1: No existing staff or arrow of the same color
        if not existing_arrows and not existing_staffs:
            arrow = self.arrow_factory.create_arrow(self, dropped_arrow)
            staff = self.staff_factory.create_staff(self.graphboard_scene, dropped_staff)
            self.graphboard_scene.addItem(arrow)
            self.graphboard_scene.addItem(staff)


        # Case 2: Existing staff of the same color but is static
        elif existing_staffs and existing_staffs[0].type == STATIC:
            existing_staff = existing_staffs[0]
            dropped_staff_attributes = self.staff_manager.staff_attributes.get_attributes(dropped_staff)
            existing_staff.attributes.update_attributes(existing_staff, dropped_staff_attributes)  # Update the staff's attributes
            existing_staff.setPos(self.staff_xy_locations[dropped_arrow_end_location])  # Update staff position
            arrow = self.arrow_factory.create_arrow(self, dropped_arrow)
            self.graphboard_scene.addItem(arrow)

        # Case 3: Both existing staff and arrow of the same color
        elif existing_arrows and existing_staffs:
            event.ignore()
            QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
            return
        
        if arrow: 
            arrow.setScale(GRAPHBOARD_SCALE)
            staff.setScale(GRAPHBOARD_SCALE)     
            self.clear_selection()
            arrow.setSelected(True)

            arrow.staff = staff
            staff.arrow = arrow

            self.graphboard_scene.removeItem(self.temp_staff)
            
            for arrow in self.graphboard_scene.items():
                if isinstance(arrow, Arrow):
                    arrow.arrow_manager.arrow_positioner.update_arrow_position(self)
            
            for staff in self.graphboard_scene.items():
                if isinstance(staff, Staff):
                    staff.setPos(self.staff_manager.staff_xy_locations[staff.location])
            
            self.info_manager.update()

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.get_selected_items()
        if isinstance(clicked_item, Arrow):
            self.context_menu_manager.create_arrow_menu(selected_items, event)
        elif isinstance(clicked_item, Staff):
            self.context_menu_manager.create_staff_menu(selected_items, event)
        else:
            self.context_menu_manager.create_graphboard_menu(event)


    ### GETTERS ###

    def get_graphboard_quadrants(self, mouse_pos):
        scene_H_center = self.sceneRect().width() / 2
        scene_V_center = self.sceneRect().height() / 2
        adjusted_mouse_y = mouse_pos.y() + VERTICAL_OFFSET
        
        if adjusted_mouse_y < scene_V_center: 
            if mouse_pos.x() < scene_H_center:
                quadrant = NORTHWEST
            else:
                quadrant = NORTHEAST
        else:
            if mouse_pos.x() < scene_H_center:
                quadrant = SOUTHWEST
            else:
                quadrant = SOUTHEAST
                
        return quadrant

    def get_state(self):
        state = {
            'arrows': [],
        }
        for item in self.scene().items():
            if isinstance(item, Arrow):
                state['arrows'].append({
                    'color': item.color,
                    'motion_type': item.motion_type,
                    'rotation_direction': item.rotation_direction,
                    'quadrant': item.quadrant,
                    'start_location': item.start_location,
                    'end_location': item.end_location,
                    'turns': item.turns,
                })
        return state
    
    def get_quadrant_center(self, quadrant):
        # Calculate the layer 2 points on the graphboard based on the grid
        graphboard_layer2_points = {}
        for point_name in ['NE_layer2_point', 'SE_layer2_point', 'SW_layer2_point', 'NW_layer2_point']:
            cx, cy = self.grid.get_circle_coordinates(point_name)
            graphboard_layer2_points[point_name] = QPointF(cx, cy)  # Subtract VERTICAL_OFFSET from y-coordinate

        # Map the quadrants to the corresponding layer 2 points
        centers = {
            NORTHEAST: graphboard_layer2_points['NE_layer2_point'],
            SOUTHEAST: graphboard_layer2_points['SE_layer2_point'],
            SOUTHWEST: graphboard_layer2_points['SW_layer2_point'],
            NORTHWEST: graphboard_layer2_points['NW_layer2_point']
        }

        return centers.get(quadrant, QPointF(0, 0))  # Subtract VERTICAL_OFFSET from default y-coordinate

    def get_current_arrow_positions(self):
        red_position = None
        blue_position = None

        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                center = arrow.pos() + arrow.boundingRect().center()
                if arrow.color == 'red':
                    red_position = center
                elif arrow.color == 'blue':
                    blue_position = center
        print(red_position, blue_position)
        return red_position, blue_position

    def get_selected_items(self):
        return self.graphboard_scene.selectedItems()
    
    def get_arrows(self):
        # return the current arrows on the graphboard as an array
        current_arrows = []
        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                current_arrows.append(arrow)
        return current_arrows
    
    ### SELECTION ###

    def select_all_items(self):
        for item in self.scene().items():
            item.setSelected(True)

    def select_all_arrows(self):
        for arrow in self.graphboard_scene.items():
            if isinstance(arrow, Arrow):
                arrow.setSelected(True)

    def clear_selection(self):
        for arrow in self.scene().selectedItems():
            arrow.setSelected(False)

    def clear_graphboard(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item


    ### OTHER ###

    def update_letter(self, letter):
        letter = self.info_manager.determine_current_letter_and_type()[0]
        if letter is None or letter == 'None':
            svg_file = f'images/letters/blank.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        if letter is not None and letter != 'None':
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    break
            svg_file = f'images/letters/{letter_type}/{letter}.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        self.letter_item.setScale(GRAPHBOARD_SCALE)
        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width()*GRAPHBOARD_SCALE / 2, GRAPHBOARD_WIDTH)

