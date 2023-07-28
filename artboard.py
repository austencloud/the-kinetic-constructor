from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF
from arrow import Arrow
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
import os
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QTimer, Qt
from staff import StaffManager, Staff

class Artboard(QGraphicsView):
    arrowMoved = pyqtSignal()
    attributesChanged = pyqtSignal()

    def __init__(self, scene: QGraphicsScene, grid, infotracker, parent=None):
        super().__init__(scene, parent)
        self.setFocusPolicy(Qt.StrongFocus)  # Add this line
        self.setAcceptDrops(True)
        self.dragging = None
        self.grid = grid
        self.staff_manager = StaffManager(scene)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setInteractive(True)
        scene.setBackgroundBrush(Qt.white) 
        self.infoTracker = infotracker
        self.renderer = QSvgRenderer()
        # Connect the signals to the update_staffs method
        self.arrowMoved.connect(self.update_staffs_and_check_beta)
        self.attributesChanged.connect(self.update_staffs_and_check_beta)
    
    def set_handlers(self, handlers):
        self.handlers = handlers

    def set_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker
    
    def getQuadrantCenter(self, quadrant):
        # Define the centers of the quadrants
        centers = {
            'ne': QPointF(550, 175),
            'se': QPointF(550, 550),
            'sw': QPointF(175, 550),
            'nw': QPointF(175, 175),
        }
        return centers.get(quadrant, QPointF(0, 0))
    
    def getExpandedQuadrantCenter(self, quadrant):
        # Define the centers of the quadrants
        centers = {
            'ne1': QPointF(525, 175),
            'ne2': QPointF(575, 100),
            'se1': QPointF(525, 525),
            'se2': QPointF(575, 600),
            'sw1': QPointF(175, 525),
            'sw2': QPointF(150, 600),
            'nw1': QPointF(175, 175),
            'nw2': QPointF(150, 100),
        }
        return centers.get(quadrant, QPointF(0, 0))
    
    def getCurrentArrowPositions(self):
        red_position = None
        blue_position = None

        for item in self.scene().items():
            if isinstance(item, Arrow):
                if item.color == 'red':
                    red_position = item.pos()
                elif item.color == 'blue':
                    blue_position = item.pos()
        print(red_position, blue_position)
        return red_position, blue_position

    def get_selected_items(self):
        return self.scene().selectedItems()
    
    def select_all_arrows(self):
        for item in self.scene().items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def update_staffs_and_check_beta(self):
        self.staff_manager.remove_beta_staves()
        self.staff_manager.update_staffs(self.scene())
        self.staff_manager.check_and_replace_staves()

    def remove_non_beta_staves(self):
        self.staff_manager.remove_non_beta_staves()

    def set_infoTracker(self, infotracker):
        self.infoTracker = infotracker

    def get_attributes(self):
        attributes = {}
        base_name = os.path.basename(self.svg_file)
        parts = base_name.split('_')

        attributes['color'] = parts[0]
        attributes['type'] = parts[1]
        attributes['rotation'] = 'Clockwise' if parts[2] == 'r' else 'Anti-clockwise'
        attributes['quadrant'] = parts[3].split('.')[0]

        return attributes
    
    def resizeEvent(self, event):
        self.setSceneRect(QRectF(self.rect()))
        super().resizeEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
        item = self.itemAt(event.pos())
        if isinstance(item, Arrow):
            item.in_artboard = True
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        self.last_known_pos = event.pos()  # Store the last known position
        if event.mimeData().hasFormat('text/plain'):
            dropped_svg = event.mimeData().text()
            base_name = os.path.basename(dropped_svg)
            color, type_, rotation, quadrant = base_name.split('_')[:4]
            for item in self.scene().items():
                if isinstance(item, Arrow):
                    if item.color == color:
                        event.ignore()
                        QToolTip.showText(QCursor.pos(), "Cannot add another arrow of the same color.")
                        return
            event.accept()
            QToolTip.hideText()  # Hide the tooltip when the event is accepted
        else:
            event.ignore()

        # Check if the shift key is being held down
        if event.keyboardModifiers() & Qt.ShiftModifier:
            # Get the current position of the dragged item
            current_pos = self.dragging.pos()

            # Calculate the movement of the dragged item
            movement = event.pos() - self.dragStartPosition

            # Constrain the movement to the x-axis or the y-axis
            if abs(movement.x()) > abs(movement.y()):
                new_pos = QPointF(current_pos.x() + movement.x(), current_pos.y())
            else:
                new_pos = QPointF(current_pos.x(), current_pos.y() + movement.y())

            # Set the new position of the dragged item
            self.dragging.setPos(new_pos)

    def dragLeaveEvent(self, event):
        item = self.itemAt(self.last_known_pos)
        if isinstance(item, Arrow):
            item.in_artboard = False
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.setFocus()
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
            dropped_svg = event.mimeData().text()

            self.arrow_item = Arrow(dropped_svg, self, self.infoTracker, self.handlers)
            self.arrow_item.setFlag(QGraphicsSvgItem.ItemIsFocusable, True)
            self.scene().addItem(self.arrow_item)
            pos = self.mapToScene(event.pos()) - self.arrow_item.boundingRect().center()
            self.arrow_item.setPos(pos)

            #deselect all other arrows
            for item in self.scene().items():
                if isinstance(item, Arrow):
                    item.setSelected(False)
            self.arrow_item.setSelected(True)  # Select the new arrow

            if self.arrow_item.pos().y() < self.sceneRect().height() / 2:
                if self.arrow_item.pos().x() < self.sceneRect().width() / 2:
                    quadrant = 'nw'
                else:
                    quadrant = 'ne'
            else:
                if self.arrow_item.pos().x() < self.sceneRect().width() / 2:
                    quadrant = 'sw'
                else:
                    quadrant = 'se'

            base_name = os.path.basename(self.arrow_item.svg_file)

            # Construct the new SVG file path
            if base_name.startswith('red_anti'):
                new_svg = f'images\\arrows\\red_anti_{self.arrow_item.orientation}_{quadrant}.svg'
            elif base_name.startswith('red_iso'):
                new_svg = f'images\\arrows\\red_iso_{self.arrow_item.orientation}_{quadrant}.svg'
            elif base_name.startswith('blue_anti'):
                new_svg = f'images\\arrows\\blue_anti_{self.arrow_item.orientation}_{quadrant}.svg'
            elif base_name.startswith('blue_iso'):
                new_svg = f'images\\arrows\\blue_iso_{self.arrow_item.orientation}_{quadrant}.svg'
            else:
                print(f"Unexpected svg_file: {self.arrow_item.svg_file}")
                new_svg = self.arrow_item.svg_file

            new_renderer = QSvgRenderer(new_svg)

            if new_renderer.isValid():
                self.arrow_item.setSharedRenderer(new_renderer)
                # Update the arrow's attributes
                self.arrow_item.svg_file = new_svg
                # print("new svg file: " + new_svg)
                self.arrow_item.quadrant = quadrant

                # Update the start and end positions
                self.arrow_item.update_positions()

                self.arrow_item.attributesChanged.emit()
                self.arrowMoved.emit()


                # Determine the end position of the arrow
                end_location = self.arrow_item.end_location

                if self.arrow_item.color == "red":
                    color = 'red'
                elif self.arrow_item.color == "blue":
                    color = 'blue'

                # Add the correct staff to the scene by calling the staff_manager.show_staff method
                self.staff_manager.show_staff(end_location + "_staff_" + color)


            else:
                print("Failed to load SVG file:", new_svg)
        else:
            event.ignore()
        self.arrowMoved.emit()  

    def mousePressEvent(self, event):
        self.dragStartPosition = event.pos()
        self.setFocus()
        items = self.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.ItemIsMovable:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                items[0].setSelected(True)
            self.dragging = items[0]
            self.dragOffset = self.mapToScene(event.pos()) - self.dragging.pos()
            self.drag = Update_Quadrant_Preview(self, self.dragging)
        else:
            for item in self.scene().selectedItems():
                item.setSelected(False)
            self.dragging = None

        if event.button() == Qt.LeftButton and not items:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return
        if self.dragging:
            new_pos = self.mapToScene(event.pos()) - self.dragOffset
            movement = new_pos - self.dragging.pos()  # Calculate the movement based on the current position

            # Check if the shift key is being held down
            if event.modifiers() & Qt.ShiftModifier:
                # Constrain the movement to the x-axis or the y-axis
                if abs(movement.x()) > abs(movement.y()):
                    new_pos.setY(self.dragging.pos().y())
                else:
                    new_pos.setX(self.dragging.pos().x())
                movement = new_pos - self.dragging.pos()

            for item in self.scene().selectedItems():
                if isinstance(item, Arrow):
                    item.setPos(item.pos() + movement)

                if isinstance(item, Arrow):
                    if item.pos().y() < self.sceneRect().height() / 2:
                        if item.pos().x() < self.sceneRect().width() / 2:
                            quadrant = 'nw'
                        else:
                            quadrant = 'ne'
                    else:
                        if item.pos().x() < self.sceneRect().width() / 2:
                            quadrant = 'sw'
                        else:
                            quadrant = 'se'

                    item.quadrant = quadrant
                    base_name = os.path.basename(item.svg_file)

                    if base_name.startswith('red_anti'):
                        new_svg = f'images\\arrows\\red_anti_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('red_iso'):
                        new_svg = f'images\\arrows\\red_iso_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('blue_anti'):
                        new_svg = f'images\\arrows\\blue_anti_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('blue_iso'):
                        new_svg = f'images\\arrows\\blue_iso_{item.rotation}_{quadrant}.svg'
                    else:
                        print(f"Unexpected svg_file: {item.svg_file}")
                        new_svg = item.svg_file 
                    
                    new_renderer = QSvgRenderer(new_svg)

                    if new_renderer.isValid():
                        item.setSharedRenderer(new_renderer)
                        item.svg_file = new_svg

                        # Update the start and end positions
                        item.update_positions()

                        item.replacement_arrow_printed = False
                            #print the qualities of the replacement arrow just once
                        if item.replacement_arrow_printed == False:
                            item.replacement_arrow_printed = True

                    # else:
                    #     print("Failed to load SVG file:", new_svg)
                      # emit the signal after the item's position has been updated

                    staff_position = item.calculate_staff_position()  # Use item instead of self.arrow_item
                    staff = Staff("staff", self.scene(), staff_position, None, item.svg_file)  # Use item instead of self.arrow_item

                    staff.show()
                self.arrowMoved.emit()

    def deleteAllArrows(self):
        for item in self.scene().items():
            if isinstance(item, Arrow):
                self.scene().removeItem(item)
                del item
        self.arrowMoved.emit()
        if self.infoTracker is not None:  # Add this line
            self.infoTracker.update()

        # Hide all staffs
        self.staff_manager.hide_all()

    def deleteAllItems(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item
        self.arrowMoved.emit()
        if self.infoTracker is not None:
            self.infoTracker.update()

    def keyPressEvent(self, event):
        key = event.key()
        dx = dy = 0
        if key == Qt.Key_Up:
            dy = -10
        elif key == Qt.Key_Down:
            dy = 10
        elif key == Qt.Key_Left:
            dx = -10
        elif key == Qt.Key_Right:
            dx = 10
        else:
            super().keyPressEvent(event)
            return

        for item in self.scene().selectedItems():
            if isinstance(item, Arrow):
                item.moveBy(dx, dy)
                self.arrowMoved.emit()

class Update_Quadrant_Preview(QDrag):
    def __init__(self, source, arrow_item, *args, **kwargs):
        super().__init__(source, *args, **kwargs)
        self.arrow_item = arrow_item
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePixmap)

    def exec_(self, *args, **kwargs):
        self.timer.start(100)
        result = super().exec_(*args, **kwargs)
        self.timer.stop()
        return result

    def updatePixmap(self):
        mouse_pos = self.source().mapFromGlobal(self.source().cursor().pos())

        if mouse_pos.y() < self.source().sceneRect().height() / 2:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'sw'
            else:
                quadrant = 'se'

        base_name = os.path.basename(self.mimeData().text())

        if base_name.startswith('red_anti'):
            new_svg = f'images\\arrows\\red\\{self.arrow_item.rotation}\\anti\\red_anti_{self.arrow_item.rotation}_{quadrant}.svg'
        elif base_name.startswith('red_iso'):
            new_svg = f'images\\arrows\\red\\{self.arrow_item.rotation}\\iso\\red_iso_{self.arrow_item.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_anti'):
            new_svg = f'images\\arrows\\blue\\{self.arrow_item.rotation}\\anti\\blue_anti_{self.arrow_item.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_iso'):
            new_svg = f'images\\arrows\\blue\\{self.arrow_item.rotation}\\iso\\blue_iso_{self.arrow_item.rotation}_{quadrant}.svg'
        else:
            print(f"Unexpected svg_file: {self.arrow_item.svg_file}")
            new_svg = self.arrow_item.svg_file

        new_svg = f'images\\arrows\\red\\r\\anti\\red_anti_r_{quadrant}.svg'

        new_renderer = QSvgRenderer(new_svg)

        if new_renderer.isValid():
            pixmap = QPixmap(self.pixmap().size())
            painter = QPainter(pixmap)
            new_renderer.render(painter)
            painter.end()
            self.setPixmap(pixmap)

