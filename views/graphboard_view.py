# Import Optimization
import os
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QCursor, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView, QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QSizePolicy, QToolTip, QFrame

# Local Imports
from objects.staff import Staff
from objects.arrow import Arrow
from objects.grid import Grid
from constants import GRAPHBOARD_SCALE, GRAPHBOARD_WIDTH, GRAPHBOARD_HEIGHT, VERTICAL_OFFSET
from managers.staff_management.graphboard_staff_manager import GraphboardStaffManager
from managers.info_manager import InfoManager
from managers.context_menu_manager import GraphboardContextMenuManager
from managers.export_manager import ExportManager

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

        # Add the grid and letter item to the scene
        self.graphboard_scene.addItem(self.grid)

    def init_managers(self, main_widget):
        self.info_manager = InfoManager(main_widget, self)
        self.staff_manager = GraphboardStaffManager(main_widget, self.graphboard_scene)
        self.export_manager = ExportManager(self.staff_manager, self.grid, self)
        self.context_menu_manager = GraphboardContextMenuManager(self)
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manager.graphboard_view = self
        self.arrow_factory = self.arrow_manager.arrow_factory

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
            self.letter_renderers[letter] = QSvgRenderer(f'images/letters/{letter}.svg')
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
        dropped_svg = event.mimeData().text()
        base_name = os.path.basename(dropped_svg)
        color = base_name.split('_')[0]

        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                if arrow.color == color:
                    event.ignore()
                    QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
                    return
        event.accept()
        QToolTip.hideText() 

    def dropEvent(self, event):
        self.setFocus()
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()
        dropped_arrow_svg_path = event.mimeData().text()
        dropped_arrow_color = event.mimeData().data("color").data().decode()  # Retrieve the color
        parts = os.path.basename(dropped_arrow_svg_path).split('_')
        dropped_arrow_svg_motion_type = parts[0]
        dropped_arrow_turns = parts[1].split('.')[0]
        dropped_arrow_rotation_direction = 'r'
        self.mouse_pos = self.mapToScene(event.position().toPoint()) 
        quadrant = self.get_graphboard_quadrants(self.mouse_pos)
        
        dropped_arrow = {
            'color': dropped_arrow_color,
            'motion_type': dropped_arrow_svg_motion_type,
            'rotation_direction': dropped_arrow_rotation_direction,
            'quadrant': quadrant,
            'start_location': None,
            'end_location': None,
            'turns': dropped_arrow_turns
        }
        
        self.arrow = self.arrow_factory.create_arrow(self, dropped_arrow)
                
        self.arrow.setScale(GRAPHBOARD_SCALE)
        self.graphboard_scene.addItem(self.arrow)
        self.clear_selection()
        self.arrow.setSelected(True)

        for arrow in self.graphboard_scene.items():
            if isinstance(arrow, Arrow):
                arrow.arrow_manager.arrow_positioner.update_arrow_position(self)
                
        self.info_frame.update()

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
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if mouse_pos.x() < scene_H_center:
                quadrant = 'sw'
            else:
                quadrant = 'se'
                
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
            'ne': graphboard_layer2_points['NE_layer2_point'],
            'se': graphboard_layer2_points['SE_layer2_point'],
            'sw': graphboard_layer2_points['SW_layer2_point'],
            'nw': graphboard_layer2_points['NW_layer2_point']
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
    
    def get_bounding_box(self):
        bounding_boxes = []
        for arrow in self.scene().items():
            if isinstance(arrow, QGraphicsRectItem):
                bounding_boxes.append(arrow)
        return bounding_boxes

    def get_attributes(self):
        attributes = {}
        base_name = os.path.basename(self.svg_file)
        parts = base_name.split('_')

        attributes['color'] = parts[0]
        attributes['type'] = parts[1]
        attributes['rotation_direction'] = parts[2]
        attributes['quadrant'] = parts[3].split('.')[0]

        return attributes
    
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

    ### SETTERS ###

    def connect_info_frame(self, info_frame):
        self.info_frame = info_frame

    def connect_generator(self, generator):
        self.generator = generator

    def connect_staff_manager(self, staff_manager):
        self.staff_manager = staff_manager

    ### OTHER ###

    def update_letter(self, letter):
        if letter is None or letter == 'None':
            svg_file = f'images/letters/blank.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        if letter is not None and letter != 'None':
            svg_file = f'images/letters/{letter}.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        self.letter_item.setScale(GRAPHBOARD_SCALE)
        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width()*GRAPHBOARD_SCALE / 2, GRAPHBOARD_WIDTH)

