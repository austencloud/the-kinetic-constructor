from PyQt5.QtWidgets import QGraphicsItem, QMenu
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import pyqtSignal, QPointF, Qt 
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
import os
import json

class Arrow(QGraphicsSvgItem):
    orientationChanged = pyqtSignal()

    def __init__(self, svg_file, graphboard_view, info_tracker, svg_manager, arrow_manager, motion_type, staff_manager):
        super().__init__(svg_file)
        
        self.graphboard_view = graphboard_view
        self.svg_file = svg_file
        self.info_tracker = info_tracker
        self.motion_type = motion_type
        self.staff_manager = staff_manager
        self.svg_manager = svg_manager
        self.arrow_manager = arrow_manager
        self.in_graphboard = False

        self.dot = None
        self.dragged_item = None
        self.staff = None
        self.quadrant = None
        self.color = None
        self.start_location = None
        self.end_location = None
        self.turns = 0
        
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        # Assuming `arrow` is an instance of the Arrow class

        with open('pictographs.json') as f:
            self.pictographs = json.load(f)
            
        self.setFlag(QGraphicsSvgItem.ItemIsMovable, True)
        self.setFlag(QGraphicsSvgItem.ItemIsSelectable, True)
        self.setTransformOriginPoint(self.boundingRect().center())

        self.set_attributes(svg_file)
        
    def set_attributes(self, svg_file):

        if self.motion_type == 'static':
            self.rotation_direction = None
            self.quadrant = None
            
        if self.motion_type == 'anti' or self.motion_type == 'pro':        
            parts = os.path.basename(self.svg_file).split('_')
            self.motion_type = parts[1]
            self.color = parts[0]
            self.rotation_direction = parts[2]
            self.quadrant = parts[3]
            self.turns = parts[4].split('.')[0]
            self.arrow_start_end_locations = self.get_arrow_start_end_locations(self.svg_file)
            self.start_location, self.end_location = self.arrow_start_end_locations.get(os.path.basename(svg_file), (None, None))

    def get_arrow_start_end_locations(self, svg_file):
        base_name = os.path.basename(svg_file)  
        color = base_name.split('_')[0] 
        arrow_start_end_locations = {
            f"{color}_anti_l_ne_0.svg": ("n", "e"),
            f"{color}_anti_r_ne_0.svg": ("e", "n"),
            f"{color}_anti_l_nw_0.svg": ("w", "n"),
            f"{color}_anti_r_nw_0.svg": ("n", "w"),
            f"{color}_anti_l_se_0.svg": ("e", "s"),
            f"{color}_anti_r_se_0.svg": ("s", "e"),
            f"{color}_anti_l_sw_0.svg": ("s", "w"),
            f"{color}_anti_r_sw_0.svg": ("w", "s"),
            f"{color}_pro_l_ne_0.svg": ("e", "n"),
            f"{color}_pro_r_ne_0.svg": ("n", "e"),
            f"{color}_pro_l_nw_0.svg": ("n", "w"),
            f"{color}_pro_r_nw_0.svg": ("w", "n"),
            f"{color}_pro_l_se_0.svg": ("s", "e"),
            f"{color}_pro_r_se_0.svg": ("e", "s"),
            f"{color}_pro_l_sw_0.svg": ("w", "s"),
            f"{color}_pro_r_sw_0.svg": ("s", "w"),
        }
        return arrow_start_end_locations

    ### SETTERS ###


    def set_orientation(self, orientation):
        self.orientation = orientation
        self.orientationChanged.emit() 

    def set_staff(self, staff):
        self.staff = staff
        
    ### GETTERS ###

    def get_attributes(self):
        self.svg_file = f"images/arrows/shift/{self.motion_type}/{self.color}_{self.motion_type}_{self.rotation_direction}_{self.quadrant}_{self.turns}.svg"
        attributes = {
            'color': self.color,
            'quadrant': self.quadrant if self.quadrant is not None else "None",
            'rotation_direction': self.rotation_direction,
            'motion_type': self.motion_type,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'turns': self.turns
        }
        return attributes

    def get_staff(self):
        return self.staff
    
    def get_arrow_start_position(arrow):
        return arrow.get_attributes().get('start_location')

    def get_arrow_end_position(arrow):
        # Assuming that the 'end_location' attribute of an arrow is a direction
        return arrow.get_attributes().get('end_location')


    ### UPDATERS ###

    def update_locations(self):

        self.start_location, self.end_location = self.arrow_start_end_locations.get(os.path.basename(self.svg_file), (None, None))

    def update_arrow_position(self):
        # Get the current combination of arrows
        current_combination = (self.get_attributes()['color'], self.get_attributes()['quadrant'], self.get_attributes()['rotation_direction'], self.get_attributes()['motion_type'], self.get_attributes()['start_location'], self.get_attributes()['end_location'], self.get_attributes()['turns'])
        optimal_position = None

        # Look up the optimal positions for the current combination
        for pictograph, combinations in self.pictographs.items():
            for combination in combinations:
                if (combination[1]['color'], combination[1]['quadrant'], combination[1]['rotation_direction'], combination[1]['motion_type'], combination[1]['start_location'], combination[1]['end_location']) == current_combination:
                    if len(combination) > 3:
                        optimal_position = combination[3]['optimal_' + self.get_attributes()['color'] + '_location']
                    else:
                        optimal_position = None  # or some other default value
                    break

        if optimal_position:
            # Calculate the position to center the arrow at the optimal position
            pos = QPointF(optimal_position['x'], optimal_position['y']) - self.boundingRect().center()
            self.setPos(pos)
        else:
            # Calculate the position to center the arrow at the quadrant center
            pos = self.graphboard_view.get_quadrant_center(self.get_attributes()['quadrant']) - self.boundingRect().center()
            self.setPos(pos)


    def move_arrows(self):
        items = self.scene().selectedItems()
        for item in items:
            item.moveBy(self.right_input.value() - self.left_input.value(), self.down_input.value() - self.up_input.value())

