import os
import json
import os
import xml.etree.ElementTree as ET
import json
from PyQt5.QtGui import QImage, QPainter, QPainterPath
from PyQt5.QtSvg import QSvgRenderer, QSvgGenerator
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtCore import QSize, QRect, QIODevice
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import Qt, pyqtSignal, QBuffer, QSize, QRect
from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Close
from arrow import Arrow

class Handlers:
    arrowMoved = pyqtSignal()

    def __init__(self, graphboard, view, grid, graphboard_scene, main_window, info_tracker):
        self.graphboard = graphboard
        self.view = view
        self.grid = grid
        self.graphboard_scene = graphboard_scene
        self.main_window = main_window
        self.info_tracker = info_tracker


        self.arrowManipulator = Arrow_Manipulator(graphboard_scene, self.graphboard)
        self.keyPressHandler = Key_Press_Handler(Arrow_Manipulator(graphboard_scene, self.graphboard))
        self.jsonUpdater = JsonUpdater(graphboard_scene)
        self.exporter = Exporter(self.graphboard, graphboard_scene)
        self.svgHandler = SvgHandler()

class Arrow_Manipulator:
    def __init__(self, graphboard_scene, graphboard):
        self.graphboard_scene = graphboard_scene
        self.graphboard = graphboard

    def rotateArrow(self, direction):
        for item in self.graphboard_scene.get_selected_items():
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
                item.update_positions()
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(new_quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

        self.graphboard.arrowMoved.emit()

    def mirrorArrow(self):
        for item in self.graphboard_scene.get_selected_items():
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
                item.update_positions()
                item.quadrant = item.quadrant.replace('.svg', '')
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(item.quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)
        self.graphboard.arrowMoved.emit()

    def delete_arrow(self):
        for item in self.graphboard_scene.get_selected_items():
            self.graphboard.scene().removeItem(item)
        self.graphboard.arrowMoved.emit()
        self.graphboard.attributesChanged.emit()

    def bringForward(self):
        for item in self.graphboard_scene.get_selected_items():
            z = item.zValue()
            item.setZValue(z + 1)

    def swapColors(self):
        self.graphboard.select_all_arrows()
        arrow_items = [item for item in self.graphboard_scene.get_selected_items() if isinstance(item, Arrow)]
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
            item.setSelected(True)
    
    def deselectAll(self):
        for item in self.graphboard.selectedItems():
            item.setSelected(False)

class Key_Press_Handler:
    def __init__(self, arrowHandler):
        self.arrowHandler = arrowHandler

    def handleKeyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.arrowHandler.delete_arrow()

class JsonUpdater:
    def __init__(self, graphboard_scene):
        self.graphboard_scene = graphboard_scene


    def updatePositionInJson(self, red_position, blue_position):
        with open('pictographs.json', 'r') as file:
            data = json.load(file)
        current_attributes = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                current_attributes.append(item.get_attributes())
        current_attributes = sorted(current_attributes, key=lambda x: x['color'])

        print("Current attributes:", current_attributes)

        for letter, combinations in data.items():
            for i, combination_set in enumerate(combinations):
                arrow_attributes = [d for d in combination_set if 'color' in d]
                combination_attributes = sorted(arrow_attributes, key=lambda x: x['color'])

                if combination_attributes == current_attributes:
                    new_optimal_red = {'x': red_position.x(), 'y': red_position.y()}
                    new_optimal_blue = {'x': blue_position.x(), 'y': blue_position.y()}
                    new_optimal_positions = {
                        "optimal_red_location": new_optimal_red,
                        "optimal_blue_location": new_optimal_blue
                    }

                    optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
                    if optimal_positions is not None:
                        optimal_positions.update(new_optimal_positions)
                        print(f"Updated optimal positions for letter {letter}")
                    else:
                        combination_set.append(new_optimal_positions)
                        print(f"Added optimal positions for letter {letter}")
        with open('pictographs.json', 'w') as file:
            json.dump(data, file, indent=4)

class Exporter:
    def __init__(self, graphboard, graphboard_scene):
        self.graphboard_scene = graphboard_scene
        self.graphboard = graphboard

    def exportAsPng(self):
        selectedItems = self.graphboard_scene.get_selected_items()
        image = QImage(self.graphboard.size(), QImage.Format_ARGB32)
        painter = QPainter(image)

        for item in selectedItems:
            item.setSelected(False)

        self.graphboard.render(painter)
        painter.end()
        image.save("export.png")

        for item in selectedItems:
            item.setSelected(True)

    def exportAsSvg(self):
        final_svg = QDomDocument()

        svg_element = final_svg.createElement('svg')
        svg_element.setAttribute('width', '750')
        svg_element.setAttribute('height', '750')
        svg_element.setAttribute('viewBox', '0 0 750 750')
        final_svg.appendChild(svg_element)

        for item in self.graphboard.scene().items():
            if isinstance(item, Arrow):
                buffer = QBuffer()
                buffer.open(QIODevice.WriteOnly)

                generator = QSvgGenerator()
                generator.setOutputDevice(buffer)
                generator.setSize(QSize(750, 750))
                generator.setViewBox(QRect(0, 0, 750, 750))
                painter = QPainter(generator)
                painter.translate(item.pos())
                painter.setTransform(item.transform(), True)
                item.paint(painter, QStyleOptionGraphicsItem(), None)
                painter.end()

                arrow_svg = QDomDocument()
                buffer.close()
                arrow_svg.setContent(buffer.data())

                g_element = arrow_svg.firstChildElement('svg').firstChildElement('g')

                g_element.setAttribute('id', os.path.basename(item.svg_file))

                g_element = final_svg.importNode(g_element, True)
                svg_element.appendChild(g_element)

        with open('output.svg', 'w') as file:
            file.write(final_svg.toString())

class SvgHandler:
    @staticmethod
    def parse_svg_file(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for element in root.iter('{http://www.w3.org/2000/svg}path'):
            print('tag:', element.tag)
            print('attributes:', element.attrib)
            return element.attrib.get('d')

    @staticmethod
    def compare_svg_paths(file_path_1, file_path_2):
        tree_1 = ET.parse(file_path_1)
        root_1 = tree_1.getroot()

        tree_2 = ET.parse(file_path_2)
        root_2 = tree_2.getroot()

        path_data_1 = None
        for element in root_1.iter('{http://www.w3.org/2000/svg}path'):
            path_data_1 = element.attrib.get('d')
            break 

        path_data_2 = None
        for element in root_2.iter('{http://www.w3.org/2000/svg}path'):
            path_data_2 = element.attrib.get('d')
            break

        if path_data_1 == path_data_2:
            print('The SVG paths are identical.')
        else:
            print('The SVG paths are different.')

    @staticmethod
    def svg_path_to_qpainterpath(svg_path):
        qpainter_path = QPainterPath()
        for segment in svg_path:
            if isinstance(segment, Line):
                qpainter_path.lineTo(segment.end.real, segment.end.imag)
            elif isinstance(segment, CubicBezier):
                qpainter_path.cubicTo(segment.control1.real, segment.control1.imag,
                                    segment.control2.real, segment.control2.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, QuadraticBezier):
                qpainter_path.quadTo(segment.control.real, segment.control.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, Arc):
                # QPainterPath doesn't support arcs, so we need to approximate the arc with cubic beziers
                # This is a complex task and might require a separate function
                pass
            elif isinstance(segment, Close):
                qpainter_path.closeSubpath()
        return qpainter_path

    @staticmethod
    def get_main_element_id(svg_file):
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Get the first element with an 'id' attribute
        for element in root.iter():
            if 'id' in element.attrib:
                return element.attrib['id']
        return None
    
    @staticmethod
    def point_in_svg(point, svg_file):
        svg_path = SvgHandler.parse_svg_file(svg_file)
        qpainter_path = SvgHandler.svg_path_to_qpainterpath(svg_path)
        return qpainter_path.contains(point)
    
class Context_Menu_Handler:
    def __init__(self, scene):
        self.scene = scene

    def create_context_menu(self, event, selected_items):
        menu = QMenu()
        if len(selected_items) == 2:
            menu.addAction("Align horizontally", self.align_horizontally)
            menu.addAction("Align vertically", self.align_vertically)
        menu.addAction("Move", self.show_move_dialog)
        menu.addAction("Delete", self.handlers.delete_arrow)
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
        items = self.scene.selectedItems()
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
