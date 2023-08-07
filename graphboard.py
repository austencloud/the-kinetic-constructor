from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QTransform, QImage
from staff import Staff
from grid import Grid
from arrow import Arrow
import os
from handlers import Arrow_Handler
from exporter import Exporter


class Graphboard(QGraphicsView):
    arrowMoved = pyqtSignal()
    attributesChanged = pyqtSignal()

    def __init__(self, graphboard_scene, grid, info_tracker, staff_manager, svg_handler, ui_setup, generator, sequence_manager, parent=None):
        super().__init__(graphboard_scene, parent)
        self.setAcceptDrops(True)
        self.dragging = None
        self.grid = grid
        self.staff_manager = staff_manager
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setInteractive(True)
        self.original_width = 750
        self.original_height = 900
        self.graphboard_scene = graphboard_scene
        self.graphboard_scene.setBackgroundBrush(Qt.white) 
        self.info_tracker = info_tracker
        self.svg_handler = svg_handler
        self.generator = generator
        self.ui_setup = ui_setup
        self.renderer = QSvgRenderer()
        self.arrowMoved.connect(self.update_staffs_and_check_beta)
        self.attributesChanged.connect(self.update_staffs_and_check_beta)
        self.exporter = Exporter(self, graphboard_scene, self.staff_manager, self.grid)
        self.sequence_manager = sequence_manager
        self.letter_renderers = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUV':
            renderer = QSvgRenderer(f'images/letters/{letter}.svg')
            self.letter_renderers[letter] = renderer
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # Create a new QGraphicsSvgItem for the letter and add it to the scene
        self.letter_item = QGraphicsSvgItem()
        self.graphboard_scene.addItem(self.letter_item)
        self.arrow_handler = Arrow_Handler(self.graphboard_scene, self, self.staff_manager)
        self.original_width = 750
        self.original_height = 900
        self.resizing = True
        self.setFixedSize(750, 900)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphboard_scene.addItem(self.grid)
        self.drag = Quadrant_Preview_Drag(self, self.dragging, self.info_tracker)


    ### MOUSE EVENTS ###

    def resizeEvent(self, event):
        # Get the new size of the graphboard
        new_size = event.size()

        # Calculate the aspect ratio
        aspect_ratio = self.width() / self.height()

        # Calculate the new width and height while maintaining the aspect ratio
        new_width = min(new_size.width(), new_size.height() * aspect_ratio)
        new_height = new_width / aspect_ratio

        # Set the new size for the graphboard
        self.setFixedSize(new_width, new_height)

        # Scale the contents within the graphboard
        self.scale_contents(new_width, new_height)

        super().resizeEvent(event)
    
    def scale_contents(self, new_width, new_height):
        # Calculate the scaling factor based on the width (or height, since you're maintaining the aspect ratio)
        scale_factor = new_width / self.original_width

        # Iterate through all items in the graphboard and scale them
        for item in self.scene().items():
            item.setScale(scale_factor)

        # You can also update the SVG content here if needed


    def mousePressEvent(self, event):
        if self.is_near_corner(event.pos()):
            self.resizing = True
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
            
        else:
            for item in self.scene().selectedItems():
                item.setSelected(False)
            self.dragging = None


        if items:
            # print(f"Clicked on an object of type {type(items[0])}")
            # print(f"Object top-left position: {items[0].scenePos()}")
            # print(f"Object center: {items[0].scenePos() + items[0].boundingRect().center()}")
            if hasattr(items[0], 'svg_file'):
                print(f"Object svg: {items[0].svg_file}")

        if event.button() == Qt.LeftButton and not items:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_near_corner(event.pos()):
            # Change the cursor to a resizing cursor
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            # Restore the original cursor
            self.setCursor(Qt.ArrowCursor)
            
        if self.resizing:
            # Get the current mouse position
            x, y = event.pos().x(), event.pos().y()

            # Calculate the new width and height while maintaining the aspect ratio
            aspect_ratio = self.original_width / self.original_height
            new_width = min(x, y * aspect_ratio)
            new_height = new_width / aspect_ratio

            # Resize the graphboard
            self.setFixedSize(int(new_width), int(new_height))

            # Scale the contents within the graphboard
            self.scale_contents(new_width, new_height)

            super().mouseMoveEvent(event)
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return
        if self.dragging:
            new_pos = self.mapToScene(event.pos()) - self.dragOffset
            movement = new_pos - self.dragging.pos()

            for item in self.scene().selectedItems():
                if isinstance(item, Arrow):
                    old_quadrant = item.quadrant  # Store the current quadrant
                    item.setPos(item.pos() + movement)
                    center_pos = item.pos() + item.boundingRect().center()

                    quadrant = self.drag.get_graphboard_quadrants(center_pos)

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
                        item.update_locations()
                    if old_quadrant != item.quadrant:  # Check if the quadrant has changed
                        self.info_tracker.update()
                        self.arrowMoved.emit()

    def mouseReleaseEvent(self, event):
        self.resizing = False



    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
        item = self.itemAt(event.pos())
        if isinstance(item, Arrow):
            item.in_graphboard = True
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        self.last_known_pos = event.pos() 
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
            QToolTip.hideText() 
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        item = self.itemAt(self.last_known_pos)
        if isinstance(item, Arrow):
            item.in_graphboard = False
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.setFocus()
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
            dropped_svg = event.mimeData().text()

            self.arrow_item = Arrow(dropped_svg, self, self.info_tracker, self.svg_handler,  self.arrow_handler)
            self.arrow_item.setFlag(QGraphicsSvgItem.ItemIsFocusable, True)
            self.scene().addItem(self.arrow_item)
            pos = self.mapToScene(event.pos()) - self.arrow_item.boundingRect().center()
            self.arrow_item.setPos(pos)

            for item in self.scene().items():
                if isinstance(item, Arrow):
                    item.setSelected(False)
            self.arrow_item.setSelected(True)
            end_location = self.arrow_item.end_location
            self.staff_manager.show_staff(end_location + "_staff_" + self.arrow_item.color)
        else:
            event.ignore()

        # Adjust the y-coordinate of the arrow's position to account for the new position of the grid
        adjusted_arrow_pos = self.arrow_item.pos() + QPointF(0, 75)
        quadrant = self.drag.get_graphboard_quadrants(adjusted_arrow_pos)
        self.arrow_item.quadrant = quadrant
        self.drag.update_arrow_svg(self.arrow_item, quadrant)  # Update the arrow's SVG file
        self.info_tracker.update()
        self.arrowMoved.emit()


    ### GETTERS ###


    def get_state(self):
        state = {
            'arrows': [],
            'staffs': [],
            'grid': None
        }
        for item in self.scene().items():
            if isinstance(item, Arrow):
                state['arrows'].append({
                    'color': item.color,
                    'position': item.pos(),
                    'quadrant': item.quadrant,
                    'rotation': item.rotation,
                    'svg_file': item.svg_file
                })
            elif isinstance(item, Staff):
                state['staffs'].append({
                    'position': item.pos(),
                    'color': item.color,
                    'svg_file': item.svg_file
                })
            elif isinstance(item, Grid):
                state['grid'] = {
                    'position': item.pos(),
                    'svg_file': item.svg_file
                }
        return state
    
    def get_quadrant_center(self, quadrant):
        centers = {
            'ne': QPointF(550, 175),
            'se': QPointF(550, 550),
            'sw': QPointF(175, 550),
            'nw': QPointF(175, 175),
        }
        return centers.get(quadrant, QPointF(0, 0))
    
    def get_expanded_quadrant_center(self, quadrant):
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
    
    def get_current_arrow_positions(self):
        red_position = None
        blue_position = None

        for item in self.scene().items():
            if isinstance(item, Arrow):
                # Calculate the center of the arrow
                center = item.pos() + item.boundingRect().center()
                if item.color == 'red':
                    red_position = center
                elif item.color == 'blue':
                    blue_position = center
        print(red_position, blue_position)
        return red_position, blue_position

    def get_selected_items(self):
        return self.graphboard_scene.selectedItems()
    
    def get_bounding_box(self):
        # return all QGraphicsItem objects that represent bounding boxes in the scene
        bounding_boxes = []
        for item in self.scene().items():
            if isinstance(item, QGraphicsRectItem):  # or whatever class represents your bounding boxes
                bounding_boxes.append(item)
        return bounding_boxes

    def get_attributes(self):
        attributes = {}
        base_name = os.path.basename(self.svg_file)
        parts = base_name.split('_')

        attributes['color'] = parts[0]
        attributes['type'] = parts[1]
        attributes['rotation'] = 'Clockwise' if parts[2] == 'r' else 'Anti-clockwise'
        attributes['quadrant'] = parts[3].split('.')[0]

        return attributes
    

    ### SELECTORS ###

    def select_all_items(self):
        for item in self.scene().items():
            item.setSelected(True)

    def select_all_arrows(self):
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def clear_selection(self):
        for item in self.scene().selectedItems():
            item.setSelected(False)


    ### INITIALIZERS ###

    def set_handlers(self, handlers):
        self.handlers = handlers

    def set_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker

    def setGenerator(self, generator):
        self.generator = generator


    ### EVENTS ###

    def resizeEvent(self, event): # KEEP THIS TO POSITION THE GRID

        super().resizeEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        dx = dy = 0
        if key == Qt.Key_Up:
            dy = -15
        elif key == Qt.Key_Down:
            dy = 15
        elif key == Qt.Key_Left:
            dx = -15
        elif key == Qt.Key_Right:
            dx = 15
        else:
            super().keyPressEvent(event)
            return

        for item in self.scene().selectedItems():
            if isinstance(item, Arrow):
                item.moveBy(dx, dy)
                self.arrowMoved.emit()

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.get_selected_items()
        if isinstance(clicked_item, Arrow):
            arrow_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_handler.delete_arrow(selected_items))
            arrow_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_handler.rotate_arrow("right", selected_items))
            arrow_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_handler.rotate_arrow("left", selected_items))
            arrow_menu.addAction(rotate_left_action)

            mirror_action = QAction('Mirror', self)
            mirror_action.triggered.connect(lambda: self.arrow_handler.mirror_arrow(selected_items))
            arrow_menu.addAction(mirror_action)

            bring_forward_action = QAction('Bring Forward', self)
            bring_forward_action.triggered.connect(lambda: self.arrow_handler.bringForward(selected_items))
            arrow_menu.addAction(bring_forward_action)
            arrow_menu.exec_(event.globalPos())

        elif isinstance(clicked_item, Staff):
            staff_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_handler.delete_arrow(selected_items))
            staff_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_handler.rotateArrow("right", selected_items))
            staff_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_handler.rotateArrow("left", selected_items))
            staff_menu.addAction(rotate_left_action)
            staff_menu.exec_(event.globalPos())

        else: 
            graphboard_menu = QMenu(self)

            swap_colors_action = QAction('Swap Colors', self)
            swap_colors_action.triggered.connect(lambda: self.arrow_handler.swap_colors(self.get_selected_items()))
            graphboard_menu.addAction(swap_colors_action)

            select_all_action = QAction('Select All', self)
            select_all_action.triggered.connect(self.arrow_handler.selectAll)
            graphboard_menu.addAction(select_all_action)

            add_to_sequence_action = QAction('Add to Sequence', self)
            add_to_sequence_action.triggered.connect(lambda _: self.sequence_manager.add_to_sequence(self))
            graphboard_menu.addAction(add_to_sequence_action)

            export_to_png_action = QAction('Export to PNG', self)
            export_to_png_action.triggered.connect(self.exporter.export_to_png)
            graphboard_menu.addAction(export_to_png_action)

            export_to_svg_action = QAction('Export to SVG', self)
            export_to_svg_action.triggered.connect(self.exporter.export_to_svg)
            graphboard_menu.addAction(export_to_svg_action)

            graphboard_menu.exec_(event.globalPos())


    ### OTHER ###

    def update_staffs_and_check_beta(self):
        self.staff_manager.remove_beta_staves()
        self.staff_manager.update_graphboard_staffs(self.scene())
        self.staff_manager.check_and_replace_staves()

    def update_letter(self, letter):
        print(f"Updating letter to {letter}")
        # Path to the letter's SVG file
        svg_file = f'images/letters/{letter}.svg'
        
        # Create a renderer for the SVG file
        renderer = QSvgRenderer(svg_file)
        
        # Check that the SVG file is valid
        if not renderer.isValid():
            print(f"Invalid SVG file: {svg_file}")
            return
        
        # Update the item's renderer
        self.letter_item.setSharedRenderer(renderer)
        
        # Center the item horizontally and place it 750 pixels down
        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width() / 2, 750)

    def clear(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item
        self.arrowMoved.emit()


    def is_near_corner(self, pos):
        sensitivity = 10  # Number of pixels within which the cursor is considered near a corner

        # Get the coordinates of the cursor
        x, y = pos.x(), pos.y()

        # Get the width and height of the graphboard
        width, height = self.width(), self.height()

        # Check if the cursor is near the top-left corner
        near_top_left = x < sensitivity and y < sensitivity

        # Check if the cursor is near the top-right corner
        near_top_right = x > width - sensitivity and y < sensitivity

        # Check if the cursor is near the bottom-left corner
        near_bottom_left = x < sensitivity and y > height - sensitivity

        # Check if the cursor is near the bottom-right corner
        near_bottom_right = x > width - sensitivity and y > height - sensitivity

        # Return True if the cursor is near any of the corners
        return near_top_left or near_top_right or near_bottom_left or near_bottom_right


class Quadrant_Preview_Drag(QDrag):
    def __init__(self, source, arrow_item, info_tracker, *args, **kwargs):
        super().__init__(source, *args, **kwargs)
        self.arrow_item = arrow_item
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pixmap)
        self.info_tracker = info_tracker

    def exec_(self, *args, **kwargs):
        self.timer.start(100)
        result = super().exec_(*args, **kwargs)
        self.timer.stop()
        return result

    def update_pixmap(self):
        mouse_pos = self.source().mapFromGlobal(self.source().cursor().pos())

        quadrant, base_name = self.get_graphboard_quadrants(mouse_pos)
        self.update_arrow_svg(self.arrow_item, quadrant)
        new_svg = f'images\\arrows\\red\\r\\anti\\red_anti_r_{quadrant}.svg'

        new_renderer = QSvgRenderer(new_svg)
        #delete the old svg from the screen
        self.arrow_item.setSharedRenderer(new_renderer)

        if new_renderer.isValid():
            pixmap = QPixmap(self.pixmap().size())
            painter = QPainter(pixmap)
            new_renderer.render(painter)
            painter.end()
            self.setPixmap(pixmap)



    def get_graphboard_quadrants(self, mouse_pos):
        mime_data = self.mimeData()
        if mime_data is not None:
            base_name = os.path.basename(mime_data.text())
        else:
            base_name = ""
        # Adjust the y-coordinate of the mouse position to account for the new position of the grid
        adjusted_mouse_y = mouse_pos.y() + 75
        if adjusted_mouse_y < self.source().sceneRect().height() / 2:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'sw'
            else:
                quadrant = 'se'
        return quadrant
 
    def update_arrow_svg(self, arrow, quadrant):
        base_name = os.path.basename(arrow.svg_file)

        if base_name.startswith('red_anti'):
            new_svg = f'images\\arrows\\red_anti_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('red_iso'):
            new_svg = f'images\\arrows\\red_iso_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_anti'):
            new_svg = f'images\\arrows\\blue_anti_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_iso'):
            new_svg = f'images\\arrows\\blue_iso_{arrow.rotation}_{quadrant}.svg'
        else:
            print(f"Unexpected svg_file: {arrow.svg_file}")
            new_svg = arrow.svg_file 

        new_renderer = QSvgRenderer(new_svg)
        if new_renderer.isValid():
            arrow.setSharedRenderer(new_renderer)
            arrow.svg_file = new_svg
            arrow.update_locations()

