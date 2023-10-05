from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QTransform, QImage, QPen, QBrush
from staff import Staff
from grid import Grid
from arrow import Arrow
import os
from exporter import Exporter
from settings import Settings
from info_tracker import Info_Tracker
from graphboard import Graphboard_View
from staff_manager import Staff_Manager
from arrow_manager import Arrow_Manager
from handlers import Svg_Handler


PICTOGRAPH_SCALE = 0.5
class Mini_Graphboard_View(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setFixedSize(int(750 * PICTOGRAPH_SCALE), int(900 * PICTOGRAPH_SCALE))
        self.mini_graphboard_scene = QGraphicsScene()
        self.mini_graphboard_scene.setSceneRect(0, 0, 650 * PICTOGRAPH_SCALE, 650 * PICTOGRAPH_SCALE)
        self.setScene(self.mini_graphboard_scene)  # Set the scene
        
        self.mini_grid = Grid("images/grid/mini_grid.svg")
        self.svg_handler = Svg_Handler()
        self.staff_manager = Staff_Manager(self.mini_graphboard_scene)
        self.arrow_manager = Arrow_Manager(self, self.staff_manager)
        self.info_tracker = Info_Tracker(self, None, self.staff_manager)
        
    def scale_down(self):
        scale_factor = PICTOGRAPH_SCALE  # 50%
        
        # Apply scaling
        for item in self.mini_graphboard_scene.items():
            if item is not self.mini_grid:
                item.setScale(scale_factor)
        # Calculate the offset needed to center the entire group
        offset_x = (self.width() - self.mini_grid.boundingRect().width() * scale_factor) / 2
        offset_y = (self.height() - self.mini_grid.boundingRect().height() * scale_factor) / 2
        
        # Apply the translation to all items in the scene
        for item in self.mini_graphboard_scene.items():
            item.setPos(item.pos() + QPointF(offset_x, offset_y))
                


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
        centers = {
            'ne': QPointF(550 * PICTOGRAPH_SCALE, 175 * PICTOGRAPH_SCALE),
            'se': QPointF(550 * PICTOGRAPH_SCALE, 550 * PICTOGRAPH_SCALE),
            'sw': QPointF(175 * PICTOGRAPH_SCALE, 550 * PICTOGRAPH_SCALE),
            'nw': QPointF(175 * PICTOGRAPH_SCALE, 175 * PICTOGRAPH_SCALE),
        }
        return centers.get(quadrant, QPointF(0, 0))



    def populate_with_combination(self, combination):
        # Create a list to store the created arrows
        created_arrows = []

        # Find the optimal positions dictionary in combination
        optimal_positions = next((d for d in combination if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
 
        for arrow_dict in combination:
            # Check if the dictionary has all the keys you need         
            if all(key in arrow_dict for key in ['color', 'motion_type', 'rotation_direction', 'quadrant', 'turns']):
                if arrow_dict['motion_type'] == 'static':
                    svg_file = f"images/arrows/blank.svg"
                else:
                    svg_file = f"images/arrows/shift/{arrow_dict['motion_type']}/{arrow_dict['color']}_{arrow_dict['motion_type']}_{arrow_dict['rotation_direction']}_{arrow_dict['quadrant']}_{arrow_dict['turns']}.svg"

                arrow = Arrow(svg_file, self, self.info_tracker, self.svg_handler, self.arrow_manager, arrow_dict['motion_type'], self.staff_manager)
                arrow.set_attributes(arrow_dict)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)
                # Get the translation values from the grid's transform
                grid_transform = self.mini_grid.transform()
                dx = grid_transform.dx()
                dy = grid_transform.dy()

                for arrow in created_arrows:    
                    # Create a new transform for the arrow
                    arrow_transform = QTransform()
                    arrow_transform.translate(dx, dy)  # Apply the same translation as the grid
                    arrow.setTransform(arrow_transform)


                # Add the arrows to the scene
                for arrow in created_arrows:
                    self.mini_graphboard_scene.addItem(arrow)
                    
            # Position the arrows
            for arrow in created_arrows:
                if optimal_positions:
                    optimal_position = optimal_positions.get(f"optimal_{arrow.get_attributes()['color']}_location")
                    if optimal_position:
                        pos = QPointF(optimal_position['x']*PICTOGRAPH_SCALE, optimal_position['y'])*PICTOGRAPH_SCALE - arrow.boundingRect().center()
                        arrow.setPos(pos)
                    else:
                        if arrow.get_attributes()['quadrant'] != "None":
                            pos = self.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                            arrow.setPos(pos)
                else:
                    #resize the arrows
                    
                    pos = self.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                    arrow.setPos(pos)

        # Update the staffs
        self.staff_manager.connect_grid(self.mini_grid)
        self.staff_manager.init_mini_graphboard_staffs(self, self.mini_grid)
        self.staff_manager.update_graphboard_staffs(self.mini_graphboard_scene)

        # # # Update any trackers or other state
        # # self.info_tracker.update()

        self.setFixedSize(int(750 * PICTOGRAPH_SCALE), int(900 * PICTOGRAPH_SCALE))
        self.scale_down()
        self.init_grid()
