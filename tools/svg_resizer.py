import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from bs4 import BeautifulSoup

class SVGResizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "SVG Resizer"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(900,900)

        # Layout
        layout = QVBoxLayout()
        
        # Stacked Widget for Preview and Directory View
        self.stacked_widget = QStackedWidget()

        # Single SVG Preview
        self.svg_widget = QSvgWidget()
        self.stacked_widget.addWidget(self.svg_widget)

        # Directory View with Large Thumbnails
        self.svg_list = QListWidget()
        self.svg_list.setViewMode(QListWidget.IconMode)
        self.svg_list.setIconSize(QSize(200, 200))  # Adjust size for large thumbnails
        self.stacked_widget.addWidget(self.svg_list)

        layout.addWidget(self.stacked_widget)

        # Upload Button
        upload_button = QPushButton("Upload SVG")
        upload_button.clicked.connect(self.open_file)
        layout.addWidget(upload_button)

        # Select Directory Button
        select_directory_button = QPushButton("Select Directory")
        select_directory_button.clicked.connect(self.select_directory)
        layout.addWidget(select_directory_button)

        self.svg_list.setIconSize(QSize(150, 150))  # Adjust size as needed


        # Slider and Percentage Input Layout
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(200)
        self.slider.setValue(100)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(1)
        self.slider.setPageStep(1)
        self.slider.valueChanged.connect(self.update_slider_text)
        self.slider.valueChanged.connect(self.update_preview)
        slider_layout.addWidget(self.slider)
        self.percentage_input = QLineEdit("100")
        self.percentage_input.setFixedWidth(50)  # Set a fixed width
        self.percentage_input.textChanged.connect(self.update_slider_from_input)
        slider_layout.addWidget(self.percentage_input)
        layout.addLayout(slider_layout)

        # Save Button
        save_button = QPushButton("Save Resized SVG")
        save_button.clicked.connect(self.apply_resizing) # Connect to a new method
        layout.addWidget(save_button)

        # Set Layout
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Show Window
        self.show()

    def update_slider_text(self, value):
        self.percentage_input.setText(str(int(value))) # Convert to integer to remove decimal


    def select_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.stacked_widget.setCurrentIndex(1)  # Switch to directory view
        if directory_path:
            self.directory_path = directory_path
            self.svg_list.clear()
            for filename in os.listdir(directory_path):
                if filename.endswith(".svg"):
                    file_path = os.path.join(directory_path, filename)
                    icon = QIcon(file_path)
                    item = QListWidgetItem(icon, "")
                    self.svg_list.addItem(item)

    def apply_resizing(self):
        scale = self.slider.value() / 100
        if hasattr(self, 'file_path'):  # Single file selected
            resized_path = self.resize_svg_coordinates(file_path, scale, preview=False)

            self.svg_widget.load(resized_path) # Update preview
        if hasattr(self, 'directory_path'): # Directory selected
            self.svg_list.clear() # Clear the existing thumbnails
            for filename in os.listdir(self.directory_path):
                if filename.endswith(".svg"):
                    file_path = os.path.join(self.directory_path, filename)
                    resized_path = self.resize_svg_coordinates(file_path, scale, preview=False)

                    icon = QIcon(resized_path)
                    item = QListWidgetItem(icon, "")
                    self.svg_list.addItem(item) # Add updated thumbnails

                
    def resize_all_in_directory(self):
        scale = self.slider.value() / 100
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".svg"):
                file_path = os.path.join(self.directory_path, filename)
                resized_path = self.resize_svg_coordinates(file_path, scale)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SVG File", "", "SVG Files (*.svg);;All Files (*)")
        self.stacked_widget.setCurrentIndex(0)  # Switch to single SVG preview view

        if file_path:
            self.file_path = file_path
            self.svg_list.clear()
            icon = QIcon(file_path)
            item = QListWidgetItem(icon, "")
            self.svg_list.addItem(item)
            self.update_preview()
                
    def update_preview(self):
        scale = self.slider.value() / 100
        self.percentage_input.setText(str(int(scale * 100)))  # Update percentage input
        icon_size = int(200 * scale)  # Calculate icon size based on scale

        if hasattr(self, 'file_path'):  # Single file selected
            resized_content = self.resize_svg_coordinates(self.file_path, scale, preview=True)
            self.preview_svg(self.svg_widget, resized_content)
        if hasattr(self, 'directory_path'):  # Directory selected
            self.svg_list.clear()  # Clear the existing thumbnails
            self.svg_list.setIconSize(QSize(icon_size, icon_size))  # Set the new icon size
            for filename in os.listdir(self.directory_path):
                if filename.endswith(".svg"):
                    file_path = os.path.join(self.directory_path, filename)
                    resized_content = self.resize_svg_coordinates(file_path, scale, preview=True)
                    pixmap = self.svg_to_pixmap(resized_content, QSize(icon_size, icon_size))
                    icon = QIcon(pixmap)  # Create QIcon from QPixmap
                    item = QListWidgetItem(icon, "")
                    self.svg_list.addItem(item)  # Add updated thumbnails



    def preview_svg(self, widget, svg_content):
        renderer = QSvgRenderer()
        renderer.load(svg_content.encode('utf-8'))
        widget.setFixedSize(renderer.defaultSize())
        widget.load(svg_content.encode('utf-8'))

    def svg_to_pixmap(self, svg_content, size=None):
        renderer = QSvgRenderer()
        renderer.load(svg_content.encode('utf-8'))
        pixmap_size = size if size else renderer.defaultSize()
        pixmap = QPixmap(pixmap_size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap



    def update_slider_from_input(self):
        try:
            value = int(self.percentage_input.text())
            self.slider.setValue(value)
        except ValueError:
            pass

    def save_file(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Resized SVG", "", "SVG Files (*.svg);;All Files (*)", options=options)
        if save_path:
            scale = self.slider.value() / 100
            resized_path = self.resize_svg_coordinates(self.file_path, scale)
            with open(resized_path, 'r') as file:
                content = file.read()
            with open(save_path, 'w') as file:
                file.write(content)
            print(f"Saved resized SVG to {save_path}")

    def resize_svg_coordinates(self, file_path, scale, preview=False):
        with open(file_path, 'r') as file:
            file_content = file.read()
        soup = BeautifulSoup(file_content, 'xml')
        elements = soup.find_all(['circle', 'ellipse', 'line', 'polygon', 'polyline', 'rect', 'path'])

        for element in elements:
            for attr_name in ['cx', 'cy', 'r', 'rx', 'ry', 'x', 'y', 'width', 'height', 'x1', 'y1', 'x2', 'y2']:
                attr_value = element.get(attr_name)
                if attr_value:
                    element[attr_name] = str(float(attr_value) * scale)
            if element.name == 'path':
                d_value = element.get('d')
                if d_value:
                    new_d_value = ''
                    for part in d_value.split():
                        try:
                            scaled_value = str(float(part) * scale)
                            new_d_value += scaled_value + ' '
                        except ValueError:
                            new_d_value += part + ' '
                    element['d'] = new_d_value.strip()
            if element.name in ['polygon', 'polyline']:
                points_value = element.get('points')
                if points_value:
                    new_points_value = ' '.join([str(float(point) * scale) for point in points_value.split()])
                    element['points'] = new_points_value
                    
        if preview:
            return str(soup)  # Return the resized content as a string
        else:
            with open(file_path, 'w') as file:
                file.write(str(soup))
            return file_path  # Return the file path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SVGResizer()
    sys.exit(app.exec_())