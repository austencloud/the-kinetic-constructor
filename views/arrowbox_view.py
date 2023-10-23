import os
from PyQt6.QtWidgets import QGraphicsView, QFrame, QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from PyQt6.QtGui import QPixmap, QDrag, QImage, QPainter, QCursor, QColor
from PyQt6.QtCore import Qt, QMimeData, QPointF
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow import Arrow
from settings import *



class ArrowBoxView(QGraphicsView):
    def __init__(self, main_widget, graphboard_view, info_frame):
        super().__init__()
        self.info_frame = info_frame
        self.drag = None
        self.drag_state = {} 
        self.graphboard_view = graphboard_view
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.arrowbox_scene = QGraphicsScene()
        self.setScene(self.arrowbox_scene)
        self.configure_arrowbox_frame()
        self.populate_arrows()
        self.objectbox_layout.addWidget(self)
        self.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        items = self.scene().items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            arrow = arrows[0]
            if event.button() == Qt.MouseButton.LeftButton:
                self.dragOffset = QPointF(event.pos()) - arrow.boundingRect().center()
                self.artboard_start_position = event.pos()
                self.drag = QDrag(self)
                self.dragging = True 
                self.dragged_item = arrow
                self.dragged_arrow_color = arrow.color  # Store the color
                mime_data = QMimeData()
                mime_data.setText(arrow.svg_file)
                mime_data.setData("color", arrow.color.encode())  # Pass the color
                self.drag.setMimeData(mime_data)
                image = QImage(arrow.boundingRect().size().toSize() * GRAPHBOARD_SCALE, QImage.Format.Format_ARGB32)
                image.fill(QColor(Qt.GlobalColor.transparent))
                painter = QPainter(image)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                renderer = QSvgRenderer(arrow.svg_file)
                if not renderer.isValid():
                    print(f"Failed to load SVG file: {self.svg_file}")
                    return
                renderer.render(painter)
                painter.end()
                pixmap = QPixmap.fromImage(image)
                self.drag.setPixmap(pixmap)
                self.drag.setHotSpot(pixmap.rect().center())
            self.dragStarted = False
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        try:
            if self.drag is not None:
                self.drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)
        except RuntimeError as e:
            event.ignore()
        
    def mouseReleaseEvent(self, event):
        arrow = self.itemAt(event.pos())
        if arrow is not None and arrow in self.drag_state:
            del self.drag_state[arrow]
            self.dragging = False 
            self.dragged_item = None 

    def configure_arrowbox_frame(self):
        self.arrowbox_frame = QFrame(self.main_window)
        self.objectbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.objectbox_layout)

    def populate_arrows(self):
        svgs_full_paths = []

        for dirpath, dirnames, filenames in os.walk(ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for svg_file in svgs_full_paths:
            self.create_and_configure_arrow(svg_file)

    def create_and_configure_arrow(self, svg_file):
        file_name = os.path.basename(svg_file)
        motion_type = file_name.split('_')[0]
        arrow_item = Arrow(svg_file, self.graphboard_view, self.info_frame, self.main_widget.svg_manager, self.main_widget.arrow_manager, motion_type, self.graphboard_view.staff_manager, "red", None, "r", None, 0)
        arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        arrow_item.setScale(GRAPHBOARD_SCALE * 0.75)
        self.arrowbox_scene.addItem(arrow_item) 
        self.main_widget.arrows.append(arrow_item)
