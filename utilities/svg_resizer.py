
import sys
import xml.etree.ElementTree as ET
from typing import List
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QRect
from PyQt6.QtCore import QRectF
import os
from PyQt6.QtGui import (
    QGuiApplication,
    QColor,
    QPen,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QGraphicsView,
    QGraphicsScene,
    QFileDialog,
    QMessageBox,
    QGraphicsRectItem,
)
import xml.etree.ElementTree as ET
import svg.path
import sys
import cairosvg
from PIL import Image
import io
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import xml.etree.ElementTree as ET

class SvgResizer(QMainWindow):
    """
    A class for resizing SVG files.

    Attributes:
        svg_file_paths (List[str]): The list of selected SVG file paths.

    Methods:
        __init__(): Initializes the SvgResizer class.
        initUI(): Initializes the user interface.
        select_svg_files(): Opens a file dialog to select SVG files.
        load_thumbnails(svg_file_paths): Loads SVG thumbnails into the graphics view.
        apply_resize(): Applies the resize operation to the selected SVG files.
        resize_svg(svg_file_path, new_width, new_height): Resizes an SVG file.
        get_svg_file_paths() -> List[str] | list: Opens a file dialog to select SVG files and returns the selected file paths.
    """

    def __init__(self) -> None:
        super().__init__()
        self.svg_file_paths = []  # To store selected file paths
        self.initUI()

    def initUI(self) -> None:
        """
        Initializes the user interface.
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add widgets to the layout
        self.graphics_view = QGraphicsView()
        self.layout.addWidget(self.graphics_view)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Enter width")
        self.width_input.focusInEvent = lambda e: self.width_input.setPlaceholderText(
            ""
        )
        self.layout.addWidget(self.width_input)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height")
        self.height_input.focusInEvent = lambda e: self.height_input.setPlaceholderText(
            ""
        )
        self.layout.addWidget(self.height_input)

        self.select_files_button = QPushButton("Select SVG Files")
        self.select_files_button.clicked.connect(self.select_svg_files)
        self.layout.addWidget(self.select_files_button)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_resize)
        self.layout.addWidget(self.apply_button)

        self.trim_button = QPushButton("Trim Excess Space")
        self.trim_button.clicked.connect(self.trim_excess_space)
        self.layout.addWidget(self.trim_button)

        # Resize window based on screen size
        app: QGuiApplication = QApplication.instance()
        screen_rect: QRect = app.primaryScreen().availableGeometry()
        self.resize(int(screen_rect.width() * 0.5), int(screen_rect.height() * 0.5))

        self.show()


    def select_svg_files(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)  # Set file mode to select a directory
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly)  # Show only directories
        file_dialog.setDirectory("resources/images/letters")  # Set the default directory
        if file_dialog.exec():
            directory = file_dialog.selectedFiles()[0]  # Get the selected directory
            self.svg_file_paths = self.get_svg_file_paths(directory)
            self.load_thumbnails(self.svg_file_paths)

    def get_svg_file_paths(self, directory: str) -> List[str]:
        svg_file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".svg"):
                    svg_file_paths.append(os.path.join(root, file))
        return svg_file_paths

    def load_thumbnails(self, svg_file_paths) -> None:
        scene = QGraphicsScene(self)
        self.graphics_view.setScene(scene)

        x_offset = 0  # Horizontal offset for arranging thumbnails side by side
        for path in svg_file_paths:
            svg_item = QGraphicsSvgItem(path)
            svg_item.setFlags(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable)
            svg_item.setPos(x_offset, 0)  # Position each item next to the previous one
            scene.addItem(svg_item)

            # Add border for each SVG item
            bbox = svg_item.boundingRect()
            border_rect: QGraphicsRectItem = QGraphicsRectItem(QRectF(0, 0, bbox.width(), bbox.height()), svg_item)
            border_rect.setPen(QPen(QColor(255, 0, 0)))
            border_rect.setZValue(-1)

            x_offset += bbox.width() + 10  # Update offset for the next item

    def apply_resize(self) -> None:
        width_input = self.width_input.text()
        height_input = self.height_input.text()

        try:
            for path in self.svg_file_paths:
                self.resize_svg(path, width_input, height_input)

            self.graphics_view.scene().clear()
            self.load_thumbnails(self.svg_file_paths)

            QMessageBox.information(self, "Success", "SVG files resized successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def resize_svg(self, svg_file_path, new_width, new_height) -> None:
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # Get the original viewBox dimensions
        old_viewbox = root.attrib.get("viewBox", "").split()
        if old_viewbox:
            old_x, old_y, old_width, old_height = map(float, old_viewbox)
        else:
            old_x, old_y = 0, 0
            old_width = float(root.attrib.get("width", "0"))
            old_height = float(root.attrib.get("height", "0"))

        # Calculate new dimensions and adjust viewBox
        new_width = float(new_width) if new_width else old_width
        new_height = float(new_height) if new_height else old_height

        # Calculate the difference and adjust the x and y coordinates of the viewBox
        width_diff = new_width - old_width
        height_diff = new_height - old_height
        new_x = old_x - width_diff / 2
        new_y = old_y - height_diff / 2

        root.attrib["viewBox"] = f"{new_x} {new_y} {new_width} {new_height}"
        if new_width:
            root.attrib["width"] = str(new_width)
        if new_height:
            root.attrib["height"] = str(new_height)

        # Add enable-background style 
        enable_background = f"new 0 0 {new_width} {new_height}"
        style = f'style="enable-background:{enable_background}"'

        # Add style attribute to SVG root
        root.set("style", style)

        # Write updated SVG file
        tree.write(svg_file_path)

    def trim_excess_space(self) -> None:
        try:
            for path in self.svg_file_paths:
                self.trim_svg(path)

            self.graphics_view.scene().clear()
            self.load_thumbnails(self.svg_file_paths)

            QMessageBox.information(self, "Success", "Excess space trimmed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def trim_svg(self, svg_file_path):
        png_data = cairosvg.svg2png(url=svg_file_path)
        image = Image.open(io.BytesIO(png_data))
        image = image.convert("RGBA")
        bbox = image.getbbox()
        if bbox:
            new_viewbox = f"{bbox[0]} {bbox[1]} {bbox[2] - bbox[0]} {bbox[3] - bbox[1]}"
            self.update_viewbox(svg_file_path, new_viewbox)
        else:
            QMessageBox.warning(self, "Warning", "The image appears to be blank.")

    def update_viewbox(self, svg_file_path, new_viewbox):
        tree = ET.parse(svg_file_path)
        root = tree.getroot()
        root.attrib['viewBox'] = new_viewbox
        tree.write(svg_file_path)


    def determine_width_of_svg_contents(self, svg_file_path) -> float:
        """ Determines the width of the contents of an SVG file.

        Args:
            svg_file_path (str): The path to the SVG file to analyze.

        Returns:
            float: The width of the contents of the SVG file.
        """
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # Iterate over each path element and analyze the d attribute
        width = 0
        for path in root.iter('path'):
            d_attribute = path.attrib['d']
            path_obj = svg.path.parse_path(d_attribute)
            path_length = path_obj.length()
            width = max(width, path_length)

        return width

app = QApplication(sys.argv)
svg_resizer = SvgResizer()
sys.exit(app.exec())
