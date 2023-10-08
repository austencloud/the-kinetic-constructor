from PyQt5.QtWidgets import QGraphicsView, QFrame
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QDrag, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtSvg import QSvgRenderer
from objects.arrow import Arrow
import os
from settings import Settings

SCALE_FACTOR = Settings.SCALE_FACTOR

class ArrowBox_View(QGraphicsView):
    def __init__(self, arrowbox_scene, graphboard_view, info_tracker, svg_manager, parent=None):
        super().__init__(arrowbox_scene, parent)
        self.drag_state = {} 
        self.graphboard_view = graphboard_view
        self.arrowbox_scene = arrowbox_scene
        self.info_tracker = info_tracker
        self.svg_manager = svg_manager
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.NoFrame)
        self.scale(SCALE_FACTOR, SCALE_FACTOR)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        items = self.scene().items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            arrow = arrows[0]
            if event.button() == Qt.LeftButton:
                self.dragOffset = event.pos() - arrow.boundingRect().center()
                self.artboard_start_position = event.pos()
                self.drag = QDrag(self)
                self.dragging = True 
                self.dragged_item = arrow
                mime_data = QMimeData()
                mime_data.setText(arrow.svg_file)
                self.drag.setMimeData(mime_data)
                image = QImage(arrow.boundingRect().size().toSize(), QImage.Format_ARGB32)
                image.fill(Qt.transparent)
                painter = QPainter(image)
                painter.setRenderHint(QPainter.Antialiasing)
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
        scenePos = self.mapToScene(event.pos())
        items = self.scene().items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            mouse_pos = self.graphboard_view.mapToScene(self.graphboard_view.mapFromGlobal(QCursor.pos()))
            graphboard_view_rect = self.graphboard_view.sceneRect()

            if graphboard_view_rect.contains(mouse_pos):
                print("graphboard_view contains mouse_pos")
                if mouse_pos.y() < graphboard_view_rect.height() / 2:
                    if mouse_pos.x() < graphboard_view_rect.width() / 2:
                        quadrant = 'nw'
                    else:
                        quadrant = 'ne'
                else:
                    if mouse_pos.x() < graphboard_view_rect.width() / 2:
                        quadrant = 'sw'
                    else:
                        quadrant = 'se'
                if hasattr(self, 'svg_file'):
                    base_name = os.path.basename(self.svg_file)

                    if base_name.startswith('red_anti'):
                        new_svg = f'images\\arrows\\shift\\anti\\red_anti_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('red_pro'):
                        new_svg = f'images\\arrows\\shift\\pro\\red_pro_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('blue_anti'):
                        new_svg = f'images\\arrows\\shift\\anti\\blue_anti_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('blue_pro'):
                        new_svg = f'images\\arrows\\shift\\pro\\blue_pro_{self.orientation}_{quadrant}_0.svg'
                    else:
                        print(f"Unexpected svg_file: {self.svg_file}")
                        


            self.drag.exec_(Qt.CopyAction | Qt.MoveAction)
            self.dragStarted = True
        
    def mouseReleaseEvent(self, event):
        arrow = self.itemAt(event.pos())
        if arrow is not None and arrow in self.drag_state:
            del self.drag_state[arrow]
            self.dragging = False 
            self.dragged_item = None 

