from PyQt5.QtWidgets import QGraphicsView, QFrame
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QDrag, QImage, QPainter, QPainterPath, QCursor
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPointF
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from objects.arrow import Arrow
import os
from settings import Settings

SCALE_FACTOR = Settings.SCALE_FACTOR

class ArrowBox_View(QGraphicsView):
    def __init__(self, arrowbox_scene, artboard, info_tracker, svg_manager, parent=None):
        super().__init__(arrowbox_scene, parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.NoFrame)
        self.dragState = {} 
        self.artboard = artboard
        self.arrowbox_scene = arrowbox_scene
        self.info_tracker = info_tracker
        self.svg_manager = svg_manager
        self.scale(SCALE_FACTOR, SCALE_FACTOR)

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
            arrow = arrows[0]
            if arrow in self.dragState:
                state = self.dragState[arrow]
                if (event.pos() - state['dragStartPosition']).manhattanLength() < QApplication.startDragDistance():
                    return
                if self.dragging:
                    new_pos = self.mapToScene(event.pos()) - self.dragOffset
                    movement = new_pos - self.dragged_item.pos()
                for arrow in self.arrowbox_scene.selectedItems():
                    arrow.setPos(arrow.pos() + movement)
                self.info_tracker.check_for_changes()
                if arrow.in_artboard:
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
        if arrow is not None and arrow in self.dragState:
            del self.dragState[arrow]
            self.dragging = False 
            self.dragged_item = None 
            from main import Info_Tracker
            infoTracker = Info_Tracker()

            self.update_positions()
            arrow.end_location = arrow.end_location.capitalize()
            staff_position = arrow.end_location
            self.staff.setPos(staff_position)
            print("staff position:", staff_position)
            infoTracker.update() 
