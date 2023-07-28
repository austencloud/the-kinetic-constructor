import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QGraphicsItem, QFileDialog
from arrow import Arrow
import os

class UploadManager:
    def upload_svg(self):
        file_path, _ = QFileDialog.getOpenFileName("Open SVG", "images\\arrows", "SVG Files (*.svg)")
        if file_path:
            svg_manager = UploadManager('images\\arrows')
            match = svg_manager.find_match(file_path)
            if match:
                print(f"Match found: {match}")
                arrow = Arrow(match, self.view)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)
                arrow.setScale(self.SVG_SCALE)

                file_name = os.path.basename(match)
                compass_direction = file_name.split('_')[-1].split('.')[0]

                if compass_direction == 'ne':
                    arrow.setPos(530, 170)
                elif compass_direction == 'se':
                    arrow.setPos(530, 530)
                elif compass_direction == 'sw':
                    arrow.setPos(170, 530)
                elif compass_direction == 'nw':
                    arrow.setPos(170, 170)

                self.artboard.addItem(arrow)
            else:
                print("No match found")

    def __init__(self, arrow_dir):
        self.arrow_dir = arrow_dir
        self.d_attributes = self.load_svg_files()

    def load_svg_files(self):
        svg_files = [os.path.join(root, file) for root, dirs, files in os.walk(self.arrow_dir) for file in files if file.endswith('.svg')]
        d_attributes = {}
        for svg_file in svg_files:
            tree = ET.parse(svg_file)
            root = tree.getroot()
            for element in root.iter('{http://www.w3.org/2000/svg}path'):
                d_attributes[svg_file] = element.attrib['d']
        return d_attributes

    def find_match(self, uploaded_file):
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        for element in root.iter('{http://www.w3.org/2000/svg}path'):
            uploaded_d = element.attrib['d']
            for svg_file, d in self.d_attributes.items():
                if d == uploaded_d:
                    return svg_file
        return None
