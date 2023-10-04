from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QTransform, QImage
from staff import Staff
from grid import Grid
from arrow import Arrow
import os
from handlers import Arrow_Handler
from exporter import Exporter
from settings import Settings
from info_tracker import Info_Tracker
from graphboard import Graphboard_View
from staff_manager import Staff_Manager
class Mini_Graphboard_View(Graphboard_View):
    def __init__(self,
                graphboard_scene,
                grid,
                info_tracker,
                staff_manager,
                svg_handler,
                arrow_handler,
                ui_setup,
                generator,
                sequence_manager,
                *args,
                **kwargs):
        
        super().__init__(
            graphboard_scene, 
            grid=grid, 
            info_tracker=info_tracker, 
            staff_manager=staff_manager, 
            svg_handler=svg_handler, 
            arrow_handler=arrow_handler, 
            ui_setup=ui_setup, 
            generator=generator, 
            sequence_manager=sequence_manager, 
            parent=None, 
            **kwargs
        )
        
        self.info_tracker = Info_Tracker(self, None, self.staff_manager)
        
        self.mini_graphboard_scene = QGraphicsScene()
        self.mini_graphboard_scene.setSceneRect(0, 0, 650, 650)
        self.setScene(self.mini_graphboard_scene)  # Set the scene
        self.mini_grid = Grid("images/grid/grid.svg")
        self.init_grid()
        self.mini_staff_manager = Staff_Manager(self.mini_graphboard_scene)  # Initialize a new Staff_Manager for the mini graphboard

    def scale_down(self):
        scale_factor = 0.5  # 50%
        self.setTransform(QTransform().scale(scale_factor, scale_factor))
        
    def init_grid(self):
        self.mini_grid.setScale(1)

        mini_grid_position = QPointF((self.width() - self.mini_grid.boundingRect().width()) / 2,
                                (self.height() - self.mini_grid.boundingRect().height()) / 2 - (75 * 1))

        transform = QTransform()
        transform.translate(mini_grid_position.x(), mini_grid_position.y())
        self.mini_grid.setTransform(transform)
        #show the grid
        self.mini_graphboard_scene.addItem(self.mini_grid)

    def mousePressEvent(self, event):
        pass
    
    def mouseMoveEvent(self, event):
        pass
    
    def mouseReleaseEvent(self, event):
        pass
    

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

                arrow = Arrow(svg_file, self, self.info_tracker, self.svg_handler, self.arrow_handler, arrow_dict['motion_type'], self.staff_manager)
                arrow.set_attributes(arrow_dict)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)

        # Add the arrows to the scene
        for arrow in created_arrows:
            self.mini_graphboard_scene.addItem(arrow)

        # Position the arrows
        for arrow in created_arrows:
            if optimal_positions:
                optimal_position = optimal_positions.get(f"optimal_{arrow.get_attributes()['color']}_location")
                if optimal_position:
                    pos = QPointF(optimal_position['x'], optimal_position['y']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
                else:
                    if arrow.get_attributes()['quadrant'] != "None":
                        pos = self.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
            else:
                pos = self.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                arrow.setPos(pos)

        # Update the staffs
        self.mini_staff_manager.connect_grid(self.mini_grid)
        self.mini_staff_manager.init_mini_graphboard_staffs(self.mini_graphboard_scene)
        self.mini_staff_manager.update_graphboard_staffs(self.mini_graphboard_scene)
        print(f"Mini graphboard View Dimensions: {self.width()} x {self.height()}")
        print(f"Mini graphboard Scene Rect: {self.mini_graphboard_scene.sceneRect()}")
        # # # Update any trackers or other state
        # # self.info_tracker.update()
        # self.scale_down()
        
        

