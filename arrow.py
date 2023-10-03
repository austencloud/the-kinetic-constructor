from PyQt5.QtWidgets import QGraphicsItem, QMenu
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import pyqtSignal, QPointF, Qt 
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
import os
import json

class Arrow(QGraphicsSvgItem):
    orientationChanged = pyqtSignal()


    def __init__(self, svg_file, graphboard_view, info_tracker, svg_handler, arrow_manipulator, motion_type, staff_manager):
        super().__init__(svg_file)
        self.setAcceptDrops(True)
        self.svg_file = svg_file
        self.in_graphboard = False
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.graphboard_view = graphboard_view
        self.grid = None
        self.dot = None
        self.dragging = False
        self.dragged_item = None
        self.info_tracker = info_tracker
        self.motion_type = motion_type
        self.parse_filename()
        self.staff_manager = staff_manager
        self.staff = None
        self.quadrant = None
        self.svg_handler = svg_handler
        self.dragStarted = False
        self.arrow_manipulator = arrow_manipulator

        self.turns = 0
        # Assuming `arrow` is an instance of the Arrow class


        with open('pictographs.json') as f:
            self.pictographs = json.load(f)

        if "_l_" in svg_file:
            self.orientation = "l"
        elif "_r_" in svg_file:
            self.orientation = "r"
        else:
            print("Unexpected svg_file:", svg_file)
            self.orientation = "r"

        if "grid" not in svg_file:
            self.setFlag(QGraphicsSvgItem.ItemIsMovable, True)
            self.setFlag(QGraphicsSvgItem.ItemIsSelectable, True)
            self.setTransformOriginPoint(self.boundingRect().center())

        if 'red' in svg_file:
            self.color = 'red'
        elif 'blue' in svg_file:
            self.color = 'blue'
        else:
            if svg_file == "images/arrows/blank.svg":
                self.color = None
            else:
                raise ValueError(f"Invalid filename: {svg_file}. Filename must contain either 'red' or 'blue'.")

        self.get_arrow_start_end_locations(self.svg_file)
        self.start_location, self.end_location = self.arrow_start_end_locations.get(os.path.basename(svg_file), (None, None))

    def get_arrow_start_end_locations(self, svg_file):
        base_name = os.path.basename(svg_file)  
        color = base_name.split('_')[0] 
        self.arrow_start_end_locations = {
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
        return self.arrow_start_end_locations

    ### SETTERS ###

    def set_attributes(self, attributes):
        self.color = attributes.get('color', self.color)
        self.quadrant = self.svg_file.split('_')[3]
        self.quadrant = attributes.get('quadrant', self.quadrant)
        self.rotation_direction = self.svg_file.split('_')[2]
        self.arrow_turns = self.svg_file.split('_')[-1].replace('.svg', '')
        self.motion_type = attributes.get('motion_type', self.motion_type)
        self.start_location = attributes.get('start_location', self.start_location)
        self.end_location = attributes.get('end_location', self.end_location)
        self.update_arrow_image() 

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.orientationChanged.emit() 

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

    
    def get_arrow_start_position(arrow):
        # Assuming that the 'start_location' attribute of an arrow is a direction
        return arrow.get_attributes().get('start_location')

    def get_arrow_end_position(arrow):
        # Assuming that the 'end_location' attribute of an arrow is a direction
        return arrow.get_attributes().get('end_location')

    def get_position_from_locations(direction1, direction2):
        # Define the mapping from pairs of directions to positions
        location_to_position = {
            ("n", "s"): "alpha",
            ("s", "n"): "alpha",
            ("w", "e"): "alpha",
            ("e", "w"): "alpha",
            ("e", "e"): "beta",
            ("s", "s"): "beta",
            ("w", "w"): "beta",
            ("n", "n"): "beta",
            ("n", "e"): "gamma",
            ("e", "n"): "gamma",
            ("e", "s"): "gamma",
            ("s", "e"): "gamma",
            ("s", "w"): "gamma",
            ("w", "s"): "gamma",
            ("w", "n"): "gamma",
            ("n", "w"): "gamma",
        }

        # Return the position corresponding to the pair of directions
        return location_to_position.get((direction1, direction2))
    
    ### UPDATERS ###

    def update_locations(self):
        # Update the start and end locations
        self.start_location, self.end_location = self.arrow_start_end_locations.get(os.path.basename(self.svg_file), (None, None))

    def update_quadrant(self):
        # Determine the quadrant based on the start and end positions
        if self.start_location == "n":
            if self.end_location == "e":
                self.quadrant = "ne"
            else:  # self.end_location == "w"
                self.quadrant = "nw"
        elif self.start_location == "s":
            if self.end_location == "e":
                self.quadrant = "se"
            else:  # self.end_location == "w"
                self.quadrant = "sw"
        elif self.start_location == "e":
            if self.end_location == "n":
                self.quadrant = "ne"
            else:
                self.quadrant = "se"
        elif self.start_location == "w":
            if self.end_location == "n":
                self.quadrant = "nw"
            else:
                self.quadrant = "sw"


     # def contextMenuEvent(self, event):
    #     if len(self.scene().selectedItems()) == 2:
    #         menu = QMenu()
    #         menu.addAction("Align horizontally", self.align_horizontally)
    #         menu.addAction("Align vertically", self.align_vertically)
    #         menu.addAction("Move", self.show_move_dialog)  # Add the new option here
    #         menu.exec_(event.screenPos())
    #     elif len(self.scene().selectedItems()) == 1:
    #         menu = QMenu()
    #         menu.addAction("Move", self.show_move_dialog)  # Add the new option here
    #         menu.addAction("Delete", self.arrow_manipulator.delete_arrow)
    #         menu.exec_(event.screenPos())

    def show_move_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        # Create the input fields
        self.up_input = QSpinBox()
        self.down_input = QSpinBox()
        self.left_input = QSpinBox()
        self.right_input = QSpinBox()

        # Add the input fields to the dialog
        layout.addRow("Up:", self.up_input)
        layout.addRow("Down:", self.down_input)
        layout.addRow("Left:", self.left_input)
        layout.addRow("Right:", self.right_input)

        # Create the buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the buttons to their slots
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # Add the buttons to the dialog
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # Show the dialog and wait for the user to click a button
        result = dialog.exec_()

        # If the user clicked the OK button, move the arrows
        if result == QDialog.Accepted:
            self.move_arrows()

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


    def update_arrow_image(self):
        # Construct the new filename based on the arrow's attributes
        new_filename = f"images\\arrows\\shift\\{self.motion_type}\\{self.color}_{self.motion_type}_{self.rotation_direction}_{self.quadrant}_{self.turns}.svg"

        # Check if the file exists
        if os.path.isfile(new_filename):
            # Load the new SVG file
            self.svg_file = new_filename
            self.setSharedRenderer(self.svg_handler.get_renderer(new_filename))
        else:

            print(f"File {new_filename} does not exist")

    def move_arrows(self):
        items = self.scene().selectedItems()
        for item in items:
            item.moveBy(self.right_input.value() - self.left_input.value(), self.down_input.value() - self.up_input.value())

    def align_horizontally(self):
        items = self.scene().selectedItems()
        average_y = sum(item.y() for item in items) / len(items)
        for item in items:
            item.setY(average_y)

    def align_vertically(self):
        items = self.scene().selectedItems()
        average_x = sum(item.x() for item in items) / len(items)
        for item in items:
            item.setX(average_x)



    def parse_filename(self):
        if self.motion_type == 'static':
            self.rotation_direction = None
            self.quadrant = None
        elif self.motion_type == 'anti' or self.motion_type == 'pro':        
            parts = os.path.basename(self.svg_file).split('_')
            self.color = parts[0]
            self.motion_type = parts[1]
            self.rotation_direction = parts[2]
            self.quadrant = parts[3].split('.')[0]





