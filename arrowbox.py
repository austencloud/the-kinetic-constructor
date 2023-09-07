from PyQt5.QtWidgets import QGraphicsView, QFrame
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QDrag, QImage, QPainter, QPainterPath, QCursor
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPointF
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from arrow import Arrow
import os


class Arrow_Box(QGraphicsView):
    def __init__(self, arrowbox_scene, artboard, info_tracker, svg_handler, parent=None):
        super().__init__(arrowbox_scene, parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.NoFrame)
        self.dragState = {}  # Store the state of drag operations
        self.artboard = artboard
        self.arrowbox_scene = arrowbox_scene
        self.info_tracker = info_tracker
        self.svg_handler = svg_handler

    def mousePressEvent(self, event):
        # Convert the mouse event position to scene coordinates
        scenePos = self.mapToScene(event.pos())
        # Get all items at the scene position
        items = self.scene().items(scenePos)
        # Filter out items that are not Arrow instances
        arrows = [item for item in items if isinstance(item, Arrow)]
        # If there are any arrows under the mouse, take the topmost one
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
                image.fill(Qt.transparent)  # Fill with transparency to preserve SVG transparency

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
        # Convert the mouse event position to scene coordinates
        scenePos = self.mapToScene(event.pos())
        # Get all items at the scene position
        items = self.scene().items(scenePos)
        # Filter out items that are not Arrow instances
        arrows = [item for item in items if isinstance(item, Arrow)]
        # If there are any arrows under the mouse, take the topmost one
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

                # print the current quadrant whenever a mouse drags over it
                print(quadrant)
                base_name = os.path.basename(self.svg_file)

                if base_name.startswith('red_anti'):
                    new_svg = f'images\\arrows\\red_anti_{self.orientation}_{quadrant}.svg'
                elif base_name.startswith('red_iso'):
                    new_svg = f'images\\arrows\\red_iso_{self.orientation}_{quadrant}.svg'
                elif base_name.startswith('blue_anti'):
                    new_svg = f'images\\arrows\\blue_anti_{self.orientation}_{quadrant}.svg'
                elif base_name.startswith('blue_iso'):
                    new_svg = f'images\\arrows\\blue_iso_{self.orientation}_{quadrant}.svg'
                else:
                    print(f"Unexpected svg_file: {self.svg_file}")
                    
            else:
                new_svg = arrow.svg_file

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
            #update all the attributes
            self.update_positions()

            # Update the staff position based on the new arrow position
            arrow.end_location = arrow.end_location.capitalize()
            staff_position = arrow.end_location
            self.staff.setPos(staff_position)  # Assuming the Staff class has a setPos method
            print("staff position:", staff_position)
            infoTracker.update() 
            self.arrowMoved.emit()  # emit the signal when the arrow is dropped
