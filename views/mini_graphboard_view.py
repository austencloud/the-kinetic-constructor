from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QAction, QMenu
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QTransform
from objects.grid import Grid
from objects.arrow import Arrow
from info_tracker import Info_Tracker
from managers.staff_manager import Staff_Manager
from managers.arrow_manager import Arrow_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager

PICTOGRAPH_SCALE = 0.5
class Mini_Graphboard_View(QGraphicsView):
    def __init__(self, main_graphboard_view):
        super().__init__()
        self.setFixedSize(int(750 * PICTOGRAPH_SCALE), int(900 * PICTOGRAPH_SCALE))
        self.mini_graphboard_scene = QGraphicsScene()
        self.mini_graphboard_scene.setSceneRect(0, 0, 650 * PICTOGRAPH_SCALE, 650 * PICTOGRAPH_SCALE)
        self.setScene(self.mini_graphboard_scene)  # Set the scene
        self.mini_grid = Grid("images/grid/mini_grid.svg")
        self.svg_manager = Svg_Manager()
        self.staff_manager = Staff_Manager(self.mini_graphboard_scene)
        self.arrow_manager = Arrow_Manager(None, self, self.staff_manager)
        self.json_manager = Json_Manager(self.mini_graphboard_scene)
        self.info_tracker = Info_Tracker(self, None, self.staff_manager, self.json_manager)
        self.arrow_manager.connect_info_tracker(self.info_tracker)
        self.staff_manager.connect_grid(self.mini_grid)
        self.init_grid()
        self.staff_manager.init_mini_graphboard_staffs(self, self.mini_grid)
        self.VERTICAL_OFFSET = (self.height() - self.width()) / 2
        self.main_graphboard_view = main_graphboard_view
        
    def init_grid(self):
        self.PADDING = self.width() - self.mini_grid.boundingRect().width()
        mini_grid_position = QPointF((self.mini_grid.get_width() - self.mini_grid.boundingRect().width()) / 2,
                                (self.height() - self.mini_grid.boundingRect().height()) / 2 - (self.height() - self.mini_grid.boundingRect().height()) + self.PADDING / 2)

        transform = QTransform()
        transform.translate(mini_grid_position.x(), mini_grid_position.y())
        self.mini_grid.setTransform(transform)
        #show the grid
        self.mini_graphboard_scene.addItem(self.mini_grid)

        pass
    
    def get_graphboard_state(self):
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
            cx, cy = self.mini_grid.get_circle_coordinates(point_name)
            graphboard_layer2_points[point_name] = QPointF(cx, cy - self.VERTICAL_OFFSET)  # Subtract VERTICAL_OFFSET from y-coordinate

        # Map the quadrants to the corresponding layer 2 points
        centers = {
            'ne': graphboard_layer2_points['NE_layer2_point'],
            'se': graphboard_layer2_points['SE_layer2_point'],
            'sw': graphboard_layer2_points['SW_layer2_point'],
            'nw': graphboard_layer2_points['NW_layer2_point']
        }

        return centers.get(quadrant, QPointF(0, 0))  # Subtract VERTICAL_OFFSET from default y-coordinate

    def get_arrows(self):
        # return the current arrows on the graphboard as an array
        current_arrows = []
        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                current_arrows.append(arrow)
        return current_arrows

    def add_arrows_to_mini_graphboard(self, combination):
        DISTANCE = 15
        created_arrows = []
        optimal_locations = next((d for d in combination if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
        for arrow_dict in combination:     
            if all(key in arrow_dict for key in ['color', 'motion_type', 'rotation_direction', 'quadrant', 'turns']):
                
                if arrow_dict['motion_type'] == 'pro' or arrow_dict['motion_type'] == 'anti':
                    self.place_shift_arrows(DISTANCE, created_arrows, optimal_locations, arrow_dict)
                            
                elif arrow_dict['motion_type'] == 'static':
                    self.place_ghost_arrows(created_arrows, arrow_dict)

        for arrow in created_arrows:
            if arrow not in self.mini_graphboard_scene.items():
                self.mini_graphboard_scene.addItem(arrow)                    
        self.staff_manager.update_mini_graphboard_staffs(self.mini_graphboard_scene)

    def place_ghost_arrows(self, created_arrows, arrow_dict):
        ghost_arrow = Arrow(None, self, self.info_tracker, self.svg_manager, self.arrow_manager, 'static', self.staff_manager, arrow_dict)
        ghost_arrow.update_attributes()
        created_arrows.append(ghost_arrow)

    def place_shift_arrows(self, DISTANCE, created_arrows, optimal_locations, arrow_dict):
        svg_file = f"images/arrows/shift/{arrow_dict['motion_type']}/{arrow_dict['color']}_{arrow_dict['motion_type']}_{arrow_dict['rotation_direction']}_{arrow_dict['quadrant']}_{arrow_dict['turns']}.svg"
        arrow = Arrow(svg_file, self, self.info_tracker, self.svg_manager, self.arrow_manager, arrow_dict['motion_type'], self.staff_manager, arrow_dict)
        arrow.update_attributes()
        arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
        arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)
        created_arrows.append(arrow)

        for arrow in created_arrows:
            arrow_transform = QTransform()
            arrow_transform.scale(PICTOGRAPH_SCALE, PICTOGRAPH_SCALE)
            arrow.setTransform(arrow_transform)
            BUFFER = (self.width() - self.mini_grid.boundingRect().width()) / 2

                        # Calculate the center of the bounding rectangle
            center = arrow.boundingRect().center()

            if optimal_locations:
                optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
                if optimal_location:
                                # Adjust the position based on the center
                    pos = QPointF(optimal_location['x'] * PICTOGRAPH_SCALE - BUFFER, optimal_location['y'] * PICTOGRAPH_SCALE - BUFFER) - center * PICTOGRAPH_SCALE
                    new_pos = pos + QPointF(0, -self.VERTICAL_OFFSET)
                    arrow.setPos(new_pos)
            else:
                pos = self.get_quadrant_center(arrow.quadrant) - center * PICTOGRAPH_SCALE
                if arrow.quadrant == 'ne':
                    pos += QPointF(DISTANCE, -DISTANCE)
                elif arrow.quadrant == 'se':
                    pos += QPointF(DISTANCE, DISTANCE)
                elif arrow.quadrant == 'sw':
                    pos += QPointF(-DISTANCE, DISTANCE)
                elif arrow.quadrant == 'nw':
                    pos += QPointF(-DISTANCE, -DISTANCE)
                arrow.setPos(pos)

    
    def save_optimal_positions(self):
        MAIN_GRAPHBOARD_BUFFER = (self.main_graphboard_view.width() - self.main_graphboard_view.grid.boundingRect().width()) / 2
        MAIN_GRAPHBOARD_V_OFFSET = (self.main_graphboard_view.height() - self.main_graphboard_view.width()) / 2
        
        for item in self.mini_graphboard_scene.items():
            if isinstance(item, Arrow):
                pos = item.pos() + item.boundingRect().center() * PICTOGRAPH_SCALE
                # Reverse the scaling
                pos = pos / PICTOGRAPH_SCALE
                # Reverse the vertical buffer
                pos.setY(pos.y() + MAIN_GRAPHBOARD_V_OFFSET)
                # Reverse the buffer
                pos = pos + QPointF(MAIN_GRAPHBOARD_BUFFER, MAIN_GRAPHBOARD_BUFFER)
                if item.get_attributes()['color'] == 'red':
                    red_position = pos
                elif item.get_attributes()['color'] == 'blue':
                    blue_position = pos
        self.json_manager.update_optimal_locations_in_json(red_position, blue_position)
        
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        saveOptimalAction = QAction("Save Optimal Positions", self)
        saveOptimalAction.triggered.connect(self.save_optimal_positions)
        contextMenu.addAction(saveOptimalAction)
        contextMenu.exec_(event.globalPos())

