from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QTransform, QImage, QPen, QBrush
from objects.staff import Staff
from objects.grid import Grid
from objects.arrow import Arrow
import os
from exporter import Exporter
from settings import Settings
from info_tracker import Info_Tracker
from graphboard import Graphboard_View
from managers.staff_manager import Staff_Manager
from managers.arrow_manager import Arrow_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager


PICTOGRAPH_SCALE = 0.5
class Mini_Graphboard_View(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setFixedSize(int(750 * PICTOGRAPH_SCALE), int(900 * PICTOGRAPH_SCALE))
        self.mini_graphboard_scene = QGraphicsScene()
        self.mini_graphboard_scene.setSceneRect(0, 0, 650 * PICTOGRAPH_SCALE, 650 * PICTOGRAPH_SCALE)
        self.setScene(self.mini_graphboard_scene)  # Set the scene
        
        self.mini_grid = Grid("images/grid/mini_grid.svg")
        self.svg_manager = Svg_Manager()
        self.staff_manager = Staff_Manager(self.mini_graphboard_scene)
        self.arrow_manager = Arrow_Manager(self, self.staff_manager)
        self.info_tracker = Info_Tracker(self, None, self.staff_manager)
        self.json_manager = Json_Manager(self.mini_graphboard_scene)
        self.staff_manager.connect_grid(self.mini_grid)
        self.init_grid()
        self.staff_manager.init_mini_graphboard_staffs(self, self.mini_grid)
        self.VERTICAL_OFFSET = (self.height() - self.width()) / 2
        
        
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

        return centers.get(quadrant, QPointF(0, 0 - self.VERTICAL_OFFSET))  # Subtract VERTICAL_OFFSET from default y-coordinate





    def add_arrows_to_mini_graphboard(self, combination):
        DISTANCE = 20 # This is the distance between the arrows and the center of the quadrant
        
        # Create a list to store the created arrows
        created_arrows = []

        # Find the optimal positions dictionary in combination
        optimal_positions = next((d for d in combination if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
 
        for arrow_dict in combination:
            # Check if the dictionary has all the keys you need         
            if all(key in arrow_dict for key in ['color', 'motion_type', 'rotation_direction', 'quadrant', 'turns']):
                if arrow_dict['motion_type'] == 'static':
                    svg_file = None
                else:
                    svg_file = f"images/arrows/shift/{arrow_dict['motion_type']}/{arrow_dict['color']}_{arrow_dict['motion_type']}_{arrow_dict['rotation_direction']}_{arrow_dict['quadrant']}_{arrow_dict['turns']}.svg"

                arrow = Arrow(svg_file, self, self.info_tracker, self.svg_manager, self.arrow_manager, arrow_dict['motion_type'], self.staff_manager)
                arrow.set_attributes(arrow_dict)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)

                # Add the arrows to the scene
                for arrow in created_arrows:
                    if arrow not in self.mini_graphboard_scene.items():
                        self.mini_graphboard_scene.addItem(arrow)
        # Position the arrows
        for arrow in created_arrows:
            arrow_transform = QTransform()
            arrow_transform.scale(PICTOGRAPH_SCALE, PICTOGRAPH_SCALE)
            arrow.setTransform(arrow_transform)
            BUFFER = (self.width() - self.mini_grid.boundingRect().width()) / 2

            # Calculate the center of the bounding rectangle
            center = arrow.boundingRect().center()

            if optimal_positions:
                optimal_position = optimal_positions.get(f"optimal_{arrow.get_attributes()['color']}_location")
                if optimal_position:
                    # Adjust the position based on the center
                    pos = QPointF(optimal_position['x'] * PICTOGRAPH_SCALE - BUFFER, optimal_position['y'] * PICTOGRAPH_SCALE - BUFFER) - center * PICTOGRAPH_SCALE
                    new_pos = pos + QPointF(0, -self.VERTICAL_OFFSET)
                    arrow.setPos(new_pos)
            else:
                pos = self.get_quadrant_center(arrow.get_attributes()['quadrant']) - center * PICTOGRAPH_SCALE
                # Move the arrow away from the center by 20 points
                if arrow.get_attributes()['quadrant'] == 'ne':
                    pos += QPointF(DISTANCE, -DISTANCE)
                elif arrow.get_attributes()['quadrant'] == 'se':
                    pos += QPointF(DISTANCE, DISTANCE)
                elif arrow.get_attributes()['quadrant'] == 'sw':
                    pos += QPointF(-DISTANCE, DISTANCE)
                elif arrow.get_attributes()['quadrant'] == 'nw':
                    pos += QPointF(-DISTANCE, -DISTANCE)
                arrow.setPos(pos)
        # Update the staffs
        self.staff_manager.update_mini_graphboard_staffs(self.mini_graphboard_scene)
        # # # Update any trackers or other state
        # # self.info_tracker.update()
        
    def save_optimal_positions(self):
        BUFFER = (self.width() - self.mini_grid.boundingRect().width()) / 2
        MAIN_GRAPHBOARD_BUFFER = 50
        MAIN_GRAPHOARD_V_OFFSET = 75
        
        for item in self.mini_graphboard_scene.items():
            if isinstance(item, Arrow):
                pos = item.pos() + item.boundingRect().center() * PICTOGRAPH_SCALE
                # Reverse the scaling
                pos = pos / PICTOGRAPH_SCALE
                # Reverse the vertical buffer
                pos.setY(pos.y() + MAIN_GRAPHOARD_V_OFFSET)
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

