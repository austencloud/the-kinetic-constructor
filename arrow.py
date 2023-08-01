from PyQt5.QtWidgets import QGraphicsItem, QMenu
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import pyqtSignal, QPointF
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
import os

class Arrow(QGraphicsSvgItem):
    attributesChanged = pyqtSignal()
    arrowMoved = pyqtSignal()
    orientationChanged = pyqtSignal()

    def __init__(self, svg_file, graphboard, infoTracker, svg_handler, arrow_manipulator):
        super().__init__(svg_file)
        self.setAcceptDrops(True)
        self.svg_file = svg_file
        self.in_graphboard = False
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.graphboard = graphboard
        self.grid = None
        self.dot = None
        self.dragging = False
        self.dragged_item = None
        self.infoTracker = infoTracker
        self.parse_filename()
        self.start_location, self.end_location = self.arrow_positions.get(os.path.basename(svg_file), (None, None))
        self.staff = None
        self.svg_handler = svg_handler
        self.dragStarted = False
        self.arrow_manipulator = arrow_manipulator


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
            raise ValueError(f"Invalid filename: {svg_file}. Filename must contain either 'red' or 'blue'.")




    ### SETTERS ###

    def set_staff(self, staff):
        self.staff = staff
        staff.set_arrow(self)  # Update the staff's arrow attribute

    def set_attributes(self, attributes):
        self.color = attributes.get('color', self.color)
        self.quadrant = attributes.get('quadrant', self.quadrant)
        self.rotation = attributes.get('rotation', self.rotation)
        self.type = attributes.get('type', self.type)
        self.start_location = attributes.get('start_location', self.start_location)
        self.end_location = attributes.get('end_location', self.end_location)

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.orientationChanged.emit() 



    ### GETTERS ###

    def get_attributes(self):
        attributes = {
            'color': self.color,
            'quadrant': self.quadrant,
            'rotation': self.rotation,
            'type': self.type,
            'start_location': self.start_location,
            'end_location': self.end_location,
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
    
    def get_arrow_locations(color):
        return {
            f"{color}_anti_l_ne.svg": ("n", "e"),
            f"{color}_anti_r_ne.svg": ("e", "n"),
            f"{color}_anti_l_nw.svg": ("w", "n"),
            f"{color}_anti_r_nw.svg": ("n", "w"),
            f"{color}_anti_l_se.svg": ("e", "s"),
            f"{color}_anti_r_se.svg": ("s", "e"),
            f"{color}_anti_l_sw.svg": ("s", "w"),
            f"{color}_anti_r_sw.svg": ("w", "s"),
            f"{color}_iso_l_ne.svg": ("e", "n"),
            f"{color}_iso_r_ne.svg": ("n", "e"),
            f"{color}_iso_l_nw.svg": ("n", "w"),
            f"{color}_iso_r_nw.svg": ("w", "n"),
            f"{color}_iso_l_se.svg": ("s", "e"),
            f"{color}_iso_r_se.svg": ("e", "s"),
            f"{color}_iso_l_sw.svg": ("w", "s"),
            f"{color}_iso_r_sw.svg": ("s", "w"),
        }
    
    def get_staff_position(self):
        handpoints = {
            "n": QPointF(325, 181.9),  
            "e": QPointF(468.1, 325),  
            "s": QPointF(325, 468.1),  
            "w": QPointF(181.9, 325),  
        }

        return handpoints.get(self.end_location)

    arrow_positions = {**get_arrow_locations("red"), **get_arrow_locations("blue")}



    ### UPDATERS ###

    def update_locations(self):
        # Update the start and end locations
        self.start_location, self.end_location = self.arrow_positions.get(os.path.basename(self.svg_file), (None, None))
        self.arrowMoved.emit()  # emit the signal when the arrow is dropped

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

    def update_rotation(self):
        if self.type == "iso":
            if self.start_location == "n":
                if self.end_location == "e":
                    self.rotation = "r"
                else: # self.end_location == "w"
                    self.rotation = "l"
            elif self.start_location == "s":
                if self.end_location == "e":
                    self.rotation = "l"
                else: # self.end_location == "w"
                    self.rotation = "r"
            elif self.start_location == "e":
                if self.end_location == "n":
                    self.rotation = "l"
                else: # self.end_location == "s"
                    self.rotation = "r"
            elif self.start_location == "w":
                if self.end_location == "n":
                    self.rotation = "r"
                else:  # self.end_location == "s"
                    self.rotation = "l"
        else:  # self.type == "anti"
            if self.start_location == "n":
                if self.end_location == "e":
                    self.rotation = "l"
                else: # self.end_location == "w"
                    self.rotation = "r"
            elif self.start_location == "s":
                if self.end_location == "e":
                    self.rotation = "r"
                else: # self.end_location == "w"
                    self.rotation = "l"
            elif self.start_location == "e":
                if self.end_location == "n":
                    self.rotation = "r"
                else: # self.end_location == "s"
                    self.rotation = "l"
            elif self.start_location == "w":
                if self.end_location == "n":
                    self.rotation = "l"
                else: # self.end_location == "s"
                    self.rotation = "r"

    def update_staff_position(self):
        new_staff_position = self.get_staff_position()
        self.staff.item.setPos(new_staff_position)

    
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

    def shape(self):
        path = QPainterPath()
        path.addRect(self.renderer().boundsOnElement(self.elementId()))
        return path

    def parse_filename(self):

        parts = os.path.basename(self.svg_file).split('_')
        self.color = parts[0]
        self.type = parts[1]
        self.rotation = parts[2]
        self.quadrant = parts[3].split('.')[0]
