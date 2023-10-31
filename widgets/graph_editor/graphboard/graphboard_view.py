from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QSizePolicy, QFrame
from objects.staff.staff import Staff
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from resources.constants import GRAPHBOARD_SCALE, GRAPHBOARD_WIDTH, GRAPHBOARD_HEIGHT, VERTICAL_OFFSET, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST
from widgets.graph_editor.graphboard.graphboard_staff_handler import GraphboardStaffHandler
from widgets.graph_editor.graphboard.graphboard_info_handler import GraphboardInfoHandler
from widgets.graph_editor.graphboard.graphboard_context_menu_handler import GraphboardContextMenuHandler
from events.mouse_events.graphboard_mouse_events import GraphboardMouseEvents
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
        self.is_graphboard = True
        self.temp_arrow = None
        self.temp_staff = None
        self.drag_preview = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setFixedSize(int(GRAPHBOARD_WIDTH), int(GRAPHBOARD_HEIGHT))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)

    def init_scene(self, main_widget):
        self.graphboard_scene = QGraphicsScene()
        self.setScene(self.graphboard_scene)
        self.main_widget = main_widget
        self.grid = Grid('resources/images/grid/grid.svg')
        self.grid.setScale(GRAPHBOARD_SCALE)
        self.scene().setSceneRect(0, 0, int(GRAPHBOARD_WIDTH), int(GRAPHBOARD_HEIGHT))
        self.VERTICAL_OFFSET = (self.height() - self.width()) / 2
        self.view_scale = GRAPHBOARD_SCALE
        # Add the grid and letter item to the scene
        self.graphboard_scene.addItem(self.grid)

    def init_managers(self, main_widget):
        self.info_handler = GraphboardInfoHandler(main_widget, self)
        self.staff_handler = GraphboardStaffHandler(main_widget, self.graphboard_scene)
        self.export_manager = ExportHandler(self.staff_handler, self.grid, self)
        self.context_menu_manager = GraphboardContextMenuHandler(self)
        self.mouse_events = GraphboardMouseEvents(self)
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manager.graphboard_view = self
        self.arrow_factory = self.arrow_manager.arrow_factory
        self.staff_factory = self.staff_handler.staff_factory
        
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
            self.letter_renderers[letter] = QSvgRenderer(f'resources/images/letters/{letter_type}/{letter}.svg')
        self.letter_item = QGraphicsSvgItem()

        self.main_widget.graphboard_scene = self.graphboard_scene
        self.graphboard_scene.addItem(self.letter_item)


    ### EVENTS ###

    def mousePressEvent(self, event):
        self.mouse_events.handle_mouse_press(event)
        super().mousePressEvent(event)

    def dragMoveEvent(self, event, drag_preview):
        if drag_preview.in_graphboard == True:
            self.mouse_events.update_temp_staff(drag_preview)




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
        letter = self.info_handler.determine_current_letter_and_type()[0]
        if letter is None or letter == 'None':
            svg_file = f'resources/images/letters/blank.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        if letter is not None and letter != 'None':
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    break
            svg_file = f'resources/images/letters/{letter_type}/{letter}.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        self.letter_item.setScale(GRAPHBOARD_SCALE)
        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width()*GRAPHBOARD_SCALE / 2, GRAPHBOARD_WIDTH)

