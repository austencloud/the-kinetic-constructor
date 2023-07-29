from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QBuffer
from PyQt5.QtSvg import QSvgRenderer, QSvgGenerator, QGraphicsSvgItem
from PyQt5.QtWidgets import QFileDialog, QGraphicsItem, QStyleOptionGraphicsItem
import os
import xml.etree.ElementTree as ET
from upload_manager import UploadManager
from arrow import Arrow
from staff import StaffManager
import json
from PyQt5.QtCore import QSize, QRect, QFile, QIODevice
from PyQt5.QtGui import QTransform
from PyQt5.QtXml import QDomDocument



class Handlers:
    arrowMoved = pyqtSignal()

    def __init__(self, artboard, view, grid, scene, main_window, info_tracker):
        self.artboard = artboard
        self.view = view
        self.grid = grid
        self.scene = scene
        self.main_window = main_window
        self.info_tracker = info_tracker

    def rotateArrow(self, direction):
        for item in self.scene.get_selected_items():
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
                pos = self.artboard.getQuadrantCenter(new_quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

        self.view.arrowMoved.emit()
    
    def updatePositionInJson(self, red_position, blue_position):
        with open('letters.json', 'r') as file:
            data = json.load(file)
        current_attributes = []
        for item in self.artboard.scene().items():
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
        with open('letters.json', 'w') as file:
            json.dump(data, file, indent=4)

    def mirrorArrow(self):
        self.view.arrowMoved.emit()
        for item in self.scene.get_selected_items():
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
                pos = self.artboard.getQuadrantCenter(item.quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)
        self.view.arrowMoved.emit()

    def deleteArrow(self):
        for item in self.scene.get_selected_items():
            self.view.scene().removeItem(item)
        self.view.arrowMoved.emit()
        self.view.attributesChanged.emit()

    def bringForward(self):
        for item in self.scene.get_selected_items():
            z = item.zValue()
            item.setZValue(z + 1)

    def swapColors(self):
        self.scene.select_all_arrows()
        arrow_items = [item for item in self.scene.get_selected_items() if isinstance(item, Arrow)]
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
            print("Cannot swap colors with no arrows on the artboard.")
            
        self.view.arrowMoved.emit()

    def selectAll(self):
        for item in self.artboard.items():
            item.setSelected(True)
    
    def deselectAll(self):
        for item in self.artboard.selectedItems():
            item.setSelected(False)

    def exportAsPng(self):
        selectedItems = self.scene.get_selected_items()
        image = QImage(self.view.size(), QImage.Format_ARGB32)
        painter = QPainter(image)

        for item in selectedItems:
            item.setSelected(False)

        self.view.render(painter)
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

        for item in self.artboard.scene().items():
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

    def parse_svg_file(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for element in root.iter():
            print('tag:', element.tag)
            print('attributes:', element.attrib)

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