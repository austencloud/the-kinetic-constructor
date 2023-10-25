import os
from PyQt6.QtWidgets import QGraphicsView, QFrame, QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from PyQt6.QtGui import QPixmap, QDrag, QImage, QPainter, QCursor, QColor
from PyQt6.QtCore import Qt, QMimeData, QPointF
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow import Arrow
from constants import ARROW_DIR, GRAPHBOARD_SCALE



class ArrowBoxView(QGraphicsView):
    def __init__(self, main_widget, graphboard_view, info_frame, arrow_manager):
        super().__init__()
        self.info_frame = info_frame
        self.drag = None
        self.drag_state = {} 
        self.graphboard_view = graphboard_view
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.arrowbox_scene = QGraphicsScene()
        self.setScene(self.arrowbox_scene)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.arrow_manager = arrow_manager
        self.arrow_factory = self.arrow_manager.arrow_factory
        
        self.configure_arrowbox_frame()
        self.view_scale = GRAPHBOARD_SCALE * 0.75
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
            self.populate_arrows(svg_file)

    def populate_arrows(self):
        
        arrow1 = {
            'color': 'red',
            'motion_type': 'pro',
            'rotation_direction': 'r',
            'quadrant': 'ne',
            'start_location': None,
            'end_location': None,
            'turns': 0
        }
        
        arrow2 = {
            'color': 'blue',
            'motion_type': 'anti',
            'rotation_direction': 'r',
            'quadrant': 'ne',
            'start_location': None,
            'end_location': None,
            'turns': 0
        }
        
        red_iso_arrow = self.arrow_factory.create_arrow(self, arrow1)
        blue_anti_arrow = self.arrow_factory.create_arrow(self, arrow2)
        
        arrows = [red_iso_arrow, blue_anti_arrow]
        
        for arrow in arrows:
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.arrowbox_scene.addItem(arrow) 
            self.main_widget.arrows.append(arrow)

        #set positions
        red_iso_arrow.setPos(100, 50)
        blue_anti_arrow.setPos(50, 50)