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

class Mini_Graphboard(Graphboard_View):
    def __init__(self, graphboard_scene, grid, info_tracker, staff_manager, svg_handler, arrow_hanndler, ui_setup, generator, sequence_manager, *args, **kwargs):
        super().__init__(graphboard_scene, grid, info_tracker, staff_manager, svg_handler, arrow_hanndler, ui_setup, generator, sequence_manager, *args, **kwargs)
        self.info_tracker = Info_Tracker(self, None, self.staff_manager)

    def init_grid(self):
        self.grid.setScale(1)

        grid_position = QPointF((self.width() - self.grid.boundingRect().width()) / 2,
                                (self.height() - self.grid.boundingRect().height()) / 2 - (75 * 1))

        transform = QTransform()
        transform.translate(grid_position.x(), grid_position.y())
        self.grid.setTransform(transform)

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
            self.graphboard_scene.addItem(arrow)

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

        # # Update the staffs
        # self.staff_manager.update_graphboard_staffs(self.graphboard_scene)

        # # Update any trackers or other state
        # self.info_tracker.update()
