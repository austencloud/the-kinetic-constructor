from PyQt5.QtWidgets import QGraphicsItem, QMenu
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import pyqtSignal, QPointF, Qt, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from settings import Settings
import os
import json

class Arrow(QGraphicsSvgItem):
    attributesChanged = pyqtSignal()
    orientationChanged = pyqtSignal()
    arrowCreated = pyqtSignal()

    def __init__(self, svg_file, graphboard, info_tracker, svg_handler, arrow_handler, ui_setup):
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
        self.info_tracker = info_tracker
        self.parse_filename()
        self.start_location, self.end_location = self.arrow_positions.get(os.path.basename(svg_file), (None, None))
        self.staff = None
        self.svg_handler = svg_handler
        self.dragStarted = False
        self.arrow_handler = arrow_handler


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
            raise ValueError(f"Invalid filename: {svg_file}. Filename must contain either 'red' or 'blue'.")




    ### SETTERS ###

    def set_attributes(self, attributes):
        self.color = attributes.get('color', self.color)
        self.quadrant = attributes.get('quadrant', self.quadrant)
        self.rotation = attributes.get('rotation', self.rotation)
        self.type = attributes.get('type', self.type)
        self.start_location = attributes.get('start_location', self.start_location)
        self.end_location = attributes.get('end_location', self.end_location)
        self.attributesChanged.emit()  # Emit the signal here
        self.update_arrow_image() 

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
        self.attributesChanged.emit()  # Emit the signal here after updating the quadrant


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
    #         menu.addAction("Delete", self.arrow_handler.delete_arrow)
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
        current_combination = (self.get_attributes()['color'], self.get_attributes()['quadrant'], self.get_attributes()['rotation'], self.get_attributes()['type'], self.get_attributes()['start_location'], self.get_attributes()['end_location'])

        optimal_position = None

        # Look up the optimal positions for the current combination
        for pictograph, combinations in self.pictographs.items():
            for combination in combinations:
                if (combination[1]['color'], combination[1]['quadrant'], combination[1]['rotation'], combination[1]['type'], combination[1]['start_location'], combination[1]['end_location']) == current_combination:
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
            pos = self.graphboard.get_quadrant_center(self.get_attributes()['quadrant']) - self.boundingRect().center()
            self.setPos(pos)


        self.attributesChanged.emit()

    def update_arrow_image(self):
        # Construct the new filename based on the arrow's attributes
        new_filename = f"images\\arrows\\{self.color}_{self.type}_{self.rotation}_{self.quadrant}.svg"
        
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

    def move_quadrant_up(self):
        if self.quadrant == 'se':
            self.quadrant = 'ne'
        elif self.quadrant == 'sw':
            self.quadrant = 'nw'
        self.update_arrow_position()

        self.attributesChanged.emit()

    def move_quadrant_left(self):
        if self.quadrant == 'ne':
            self.quadrant = 'nw'
        elif self.quadrant == 'se':
            self.quadrant = 'sw'
        self.update_arrow_position()

    def move_quadrant_down(self):
        if self.quadrant == 'ne':
            self.quadrant = 'se'
        elif self.quadrant == 'nw':
            self.quadrant = 'sw'
        self.update_arrow_position()

    def move_quadrant_right(self):
        if self.quadrant == 'nw':
            self.quadrant = 'ne'
        elif self.quadrant == 'sw':
            self.quadrant = 'se'
        self.update_arrow_position()

class Arrow_Handler(QObject):
    arrowMoved = pyqtSignal()
    attributesChanged = pyqtSignal()

    def __init__(self, graphboard_scene, graphboard, staff_manager):
        super().__init__()
        self.graphboard_scene = graphboard_scene
        self.graphboard = graphboard
        self.staff_manager = staff_manager

    def move_arrow_quadrant_up(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        print(self.selected_arrow)
        if self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'nw'
        # Update the arrow's position and orientation on the graphboard
        self.selected_arrow.update_arrow_position()
        # Update the arrow's image

        print(self.selected_arrow.quadrant)
        self.arrowMoved.emit()
        self.attributesChanged.emit()


    def move_arrow_quadrant_left(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'nw'
        elif self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard
        self.selected_arrow.update_arrow_position()
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_down(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'se'
        elif self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard
        self.selected_arrow.update_arrow_position()
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_right(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'se'
        # Update the arrow's position and orientation on the graphboard
        self.selected_arrow.update_arrow_position()
        print(self.selected_arrow.quadrant)

    def rotate_arrow(self, direction, items):
        for item in items:
            print(item.get_attributes())
            old_svg = f"images/arrows/{item.color}_{item.type}_{item.rotation}_{item.quadrant}.svg"
            print(old_svg)
            quadrants = ['ne', 'se', 'sw', 'nw']
            current_quadrant_index = quadrants.index(item.quadrant)
            if direction == "right":
                new_quadrant_index = (current_quadrant_index + 1) % 4
            else:  # direction == "left"
                new_quadrant_index = (current_quadrant_index - 1) % 4
            new_quadrant = quadrants[new_quadrant_index]
            new_svg = item.svg_file.replace(item.quadrant, new_quadrant)

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                item.setSharedRenderer(new_renderer)
                item.svg_file = new_svg
                item.update_locations()
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(new_quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

        self.graphboard.arrowMoved.emit()

    def mirror_arrow(self, items):
        for item in items:
            current_svg = item.svg_file

            if item.rotation == "l":
                new_svg = current_svg.replace("_l_", "_r_").replace("\\l\\", "\\r\\")
                item.rotation = "r"
            elif item.rotation == "r":
                new_svg = current_svg.replace("_r_", "_l_").replace("\\r\\", "\\l\\")
                item.rotation = "l"
            else:
                print("Unexpected svg_file:", current_svg)
                continue

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                item.setSharedRenderer(new_renderer)
                item.svg_file = new_svg
                item.update_locations()
                item.quadrant = item.quadrant.replace('.svg', '')
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(item.quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)
        self.graphboard.arrowMoved.emit()

    def bring_forward(self, items):
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def swap_colors(self, _):
        arrow_items = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow)]
        if len(arrow_items) >= 1:
            for item in arrow_items:
                current_svg = item.svg_file
                base_name = os.path.basename(current_svg)
                color, type_, rotation, quadrant = base_name.split('_')[:4]
                if color == "red":
                    new_color = "blue"
                elif color == "blue":
                    new_color = "red"
                else:
                    print("Unexpected color:", color)
                    continue
                new_svg = current_svg.replace(color, new_color)
                new_renderer = QSvgRenderer(new_svg)
                if new_renderer.isValid():
                    item.setSharedRenderer(new_renderer)
                    item.svg_file = new_svg
                    item.color = new_color
                else:
                    print("Failed to load SVG file:", new_svg)
        else:
            print("Cannot swap colors with no arrows on the graphboard.")
            
        self.graphboard.arrowMoved.emit()

    def selectAll(self):
        for item in self.graphboard.items():
            #if item is an arrow
            if isinstance(item, Arrow):
                item.setSelected(True)
    
    def deselectAll(self):
        for item in self.graphboard.selectedItems():
            item.setSelected(False)

    def connect_to_graphboard(self, graphboard):
        self.graphboard = graphboard
        self.selected_items_len = len(graphboard.get_selected_items())


    def delete_arrow(self, items):
        for item in items:
            self.graphboard.scene().removeItem(item)
        self.graphboard.arrowMoved.emit()
        self.graphboard.attributesChanged.emit()


