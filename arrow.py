from PyQt5.QtWidgets import QApplication, QGraphicsItem, QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QDrag, QImage, QPainter, QPainterPath, QCursor
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPointF
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem

import os

class Arrow(QGraphicsSvgItem):
    attributesChanged = pyqtSignal()
    arrowMoved = pyqtSignal()  # add this line
    orientationChanged = pyqtSignal()  # Add this line

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.orientationChanged.emit() 

    def __init__(self, svg_file, artboard, infoTracker, handlers):
        super().__init__(svg_file)
        self.setAcceptDrops(True)
        self.svg_file = svg_file
        self.in_artboard = False
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.artboard = artboard
        self.grid = None
        self.dot = None
        self.dragging = False
        self.dragged_item = None
        self.infoTracker = infoTracker
        self.parse_filename()
        self.start_location, self.end_location = self.arrow_positions.get(os.path.basename(svg_file), (None, None))
        self.staff = None
        self.handlers = handlers
        self.dragStarted = False

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
    
    def shape(self):
        path = QPainterPath()
        path.addRect(self.renderer().boundsOnElement(self.elementId()))
        return path

    def parse_filename(self):
        # Assuming filenames are in the format 'color_type_r_quadrant.svg'
        parts = os.path.basename(self.svg_file).split('_')  # use self.svg_file here
        self.color = parts[0]
        self.type = parts[1]
        self.rotation = parts[2]
        self.quadrant = parts[3].split('.')[0]  # remove the '.svg' part

class ArrowGUI(Arrow):
    def __init__(self, svg_file, artboard, infoTracker, handlers):
        super().__init__(svg_file, artboard, infoTracker, handlers)

    def mousePressEvent(self, event):
        self.dragStartPosition = event.pos()
        self.dragOffset = event.pos() - self.boundingRect().center()
        if self.in_artboard:
            super().mousePressEvent(event)
        elif event.button() == Qt.LeftButton:
            self.artboard_start_position = event.pos()

            self.drag = QDrag(self)
            self.dragging = True 
            self.dragged_item = self  # set dragged_item to self when the drag starts
            
            mime_data = QMimeData()
            mime_data.setText(self.svg_file)
            self.drag.setMimeData(mime_data)

            # Create a QImage to render the SVG to
            image = QImage(self.boundingRect().size().toSize(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)  # Fill with transparency to preserve SVG transparency

            # Create a QPainter to paint the SVG onto the QImage
            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)

            # Create a QSvgRenderer with the SVG file and render it onto the QImage
            renderer = QSvgRenderer(self.svg_file)
            if not renderer.isValid():
                print(f"Failed to load SVG file: {self.svg_file}")
                return
            renderer.render(painter)


            painter.end()

            # Convert the QImage to a QPixmap and set it as the drag pixmap
            pixmap = QPixmap.fromImage(image)
            self.drag.setPixmap(pixmap)
            self.drag.setHotSpot(pixmap.rect().center())
        self.dragStarted = False

    def mouseMoveEvent(self, event):
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return
        if self.dragging:
            new_pos = self.mapToScene(event.pos()) - self.dragOffset
            movement = new_pos - self.dragged_item.pos()
        for item in self.scene().selectedItems():
            item.setPos(item.pos() + movement)
        self.infoTracker.check_for_changes()
        if self.in_artboard:
            print("mouse_pos:", mouse_pos)
            super().mouseMoveEvent(event)
        elif not (event.buttons() & Qt.LeftButton):
            return
        elif (event.pos() - self.artboard_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        mouse_pos = self.artboard.mapToScene(self.artboard.mapFromGlobal(QCursor.pos()))
        artboard_rect = self.artboard.sceneRect()

        if artboard_rect.contains(mouse_pos):
            print("artboard contains mouse_pos")
            if mouse_pos.y() < artboard_rect.height() / 2:
                if mouse_pos.x() < artboard_rect.width() / 2:
                    quadrant = 'nw'
                else:
                    quadrant = 'ne'
            else:
                if mouse_pos.x() < artboard_rect.width() / 2:
                    quadrant = 'sw'
                else:
                    quadrant = 'se'

            # print the current quadrant whenever a mouse drags over it
            print(quadrant)
            base_name = os.path.basename(self.svg_file)

            if base_name.startswith('red_anti'):
                new_svg = f'images\\arrows\\red_anti_{self.orientation}_{quadrant}.svg'
            elif base_name.startswith('red_iso'):
                new_svg = f'images\\arrows\\red_iso_{self.orientation}_{quadrant}.svg'
            elif base_name.startswith('blue_anti'):
                new_svg = f'images\\arrows\\blue_anti_{self.orientation}_{quadrant}.svg'
            elif base_name.startswith('blue_iso'):
                new_svg = f'images\\arrows\\blue_iso_{self.orientation}_{quadrant}.svg'
            else:
                print(f"Unexpected svg_file: {self.svg_file}")
                new_svg = self.svg_file
        else:
            new_svg = self.svg_file

        new_renderer = QSvgRenderer(new_svg)

        if new_renderer.isValid():
            pixmap = QPixmap(self.boundingRect().size().toSize())
            painter = QPainter(pixmap)
            new_renderer.render(painter)
            painter.end()
            self.drag.setPixmap(pixmap)

        if not self.dragStarted:
            self.drag.exec_(Qt.CopyAction | Qt.MoveAction)
            self.dragStarted = True
        
    def mouseReleaseEvent(self, event):
        self.dragging = False 
        self.dragged_item = None 
        from main import Info_Tracker
        infoTracker = Info_Tracker()
        #update all the attributes
        self.update_positions()

        # Update the staff position based on the new arrow position
        staff_position = self.get_staff_position()
        self.staff.setPos(staff_position)  # Assuming the Staff class has a setPos method
        print("staff position:", staff_position)
        infoTracker.update() 
        self.arrowMoved.emit()  # emit the signal when the arrow is dropped

    def contextMenuEvent(self, event):
        if len(self.scene().selectedItems()) == 2:
            self.twoSelectedContextMenuEvent(event)
        elif len(self.scene().selectedItems()) == 1:
            menu = QMenu()
            menu.addAction("Move", self.show_move_dialog)  # Add the new option here
            menu.addAction("Delete", self.handlers.deleteArrow)
            menu.exec_(event.screenPos())

    def twoSelectedContextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction("Align horizontally", self.align_horizontally)
        menu.addAction("Align vertically", self.align_vertically)
        menu.addAction("Move", self.show_move_dialog)  # Add the new option here
        menu.exec_(event.screenPos())

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
            
class ArrowAttributes(Arrow):
    def __init__(self, svg_file, artboard, infoTracker, handlers):
        super().__init__(svg_file, artboard, infoTracker, handlers)

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
    
    def set_attributes(self, attributes):
        self.color = attributes.get('color', self.color)
        self.quadrant = attributes.get('quadrant', self.quadrant)
        self.rotation = attributes.get('rotation', self.rotation)
        self.type = attributes.get('type', self.type)
        self.start_location = attributes.get('start_location', self.start_location)
        self.end_location = attributes.get('end_location', self.end_location)

class ArrowPositions(Arrow):
    def __init__(self, svg_file, artboard, infoTracker, handlers):
        super().__init__(svg_file, artboard, infoTracker, handlers)
        arrow_positions = {self.generate_arrow_positions("red"), self.generate_arrow_positions("blue")}

    def generate_arrow_positions(color):
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
    
    def update_positions(self):
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

    def update_positions(self):
        # Update the start and end positions
        self.start_location, self.end_location = self.arrow_positions.get(os.path.basename(self.svg_file), (None, None))
        self.arrowMoved.emit()

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

class ArrowStaff(Arrow):
    def __init__(self, svg_file, artboard, infoTracker, handlers):
        super().__init__(svg_file, artboard, infoTracker, handlers)

    def set_staff(self, staff):
        self.staff = staff
        staff.set_arrow(self) 

    def get_staff_position(self):
        # Determine the position of the staff based on the position of the arrow
        # This is just an example, you would need to implement this based on your specific requirements
        print("getting staff position")
        if self.end_location == 'n':
            return 'N'
        elif self.end_location == 'e':
            return 'E'
        elif self.end_location == 's':
            return 'S'
        elif self.end_location == 'w':
            return 'W'

    def update_staff_position(self):
        new_staff_position = self.calculate_staff_position()
        self.staff.item.setPos(new_staff_position)

    def calculate_staff_position(self):
        end_positions_staff_positions = {
            "n": QPointF(325, 181.9),  
            "e": QPointF(468.1, 325),  
            "s": QPointF(325, 468.1),  
            "w": QPointF(181.9, 325),  
        }

        return end_positions_staff_positions.get(self.end_location)
