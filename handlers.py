import os
import json
import os
import xml.etree.ElementTree as ET
import json
import re
from PyQt5.QtGui import QImage, QPainter, QPainterPath, QTransform
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Close
from arrow import Arrow
from staff import Staff
from grid import Grid
from lxml import etree
from copy import deepcopy


class Arrow_Handler(QObject):


    arrowDeleted = pyqtSignal()  # New signal to indicate an arrow has been deleted


    def __init__(self, graphboard_view, staff_manager):
        super().__init__()
        self.graphboard_view = graphboard_view
        self.staff_manager = staff_manager

    def connect_graphboard_scene(self, graphboard_scene):
        self.graphboard_scene = graphboard_scene

    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def move_arrow_quadrant_up(self):
        self.selected_arrow = self.graphboard_view.get_selected_items()[0]
        print(self.selected_arrow)
        if self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'nw'
        # Update the arrow's position and orientation on the graphboard_view
        self.selected_arrow.update_arrow_position()
        # Update the arrow's image

        print(self.selected_arrow.quadrant)




    def move_arrow_quadrant_left(self):
        self.selected_arrow = self.graphboard_view.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'nw'
        elif self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard_view
        self.selected_arrow.update_arrow_position()
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_down(self):
        self.selected_arrow = self.graphboard_view.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'se'
        elif self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard_view
        self.selected_arrow.update_arrow_position()
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_right(self):
        self.selected_arrow = self.graphboard_view.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'se'
        # Update the arrow's position and orientation on the graphboard_view
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
                pos = self.graphboard_view.get_quadrant_center(new_quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)



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
                pos = self.graphboard_view.get_quadrant_center(item.quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

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
            print("Cannot swap colors with no arrows on the graphboard_view.")
            

    def selectAll(self):
        for item in self.graphboard_view.items():
            #if item is an arrow
            if isinstance(item, Arrow):
                item.setSelected(True)
    
    def deselectAll(self):
        for item in self.graphboard_view.selectedItems():
            item.setSelected(False)

    def connect_to_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.selected_items_len = len(graphboard_view.get_selected_items())


    def delete_arrow(self, items):
        for item in items:
            if isinstance(item, Arrow):
                # Find the corresponding staff and set it to static
                end_location = item.end_location  # Assuming this gives the end position of the arrow
                staff = self.staff_manager.find_staff_by_position(end_location)  # Assuming you'll implement this method
                if staff:
                    staff.set_static(True)
            self.graphboard_view.scene().removeItem(item)
        
        self.arrowDeleted.emit()  # Emit the signal to update the letter
        print("Deleted arrow(s)")

class Key_Press_Handler:
    def __init__(self, arrow, graphboard_view=None):
        self.arrow = arrow

    def connect_to_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view

class Json_Handler:
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



class Svg_Handler:
    def __init__(self):
        self.renderers = {}

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
        svg_path = Svg_Handler.parse_svg_file(svg_file)
        qpainter_path = Svg_Handler.svg_path_to_qpainterpath(svg_path)
        return qpainter_path.contains(point)
    
    def get_renderer(self, filename):
        if filename not in self.renderers:
            self.renderers[filename] = QSvgRenderer(filename)
        return self.renderers[filename]
    
