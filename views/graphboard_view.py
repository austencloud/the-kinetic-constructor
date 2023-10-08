import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from objects.staff import Staff
from objects.grid import Grid
from objects.arrow import Arrow
from settings import Settings, Graphboard_Constants



SCALE_FACTOR = Settings.SCALE_FACTOR

class Graphboard_View(QGraphicsView):
    def __init__(self,
                 graphboard_scene,
                 grid,
                 info_tracker,
                 staff_manager,
                 svg_manager,
                 arrow_manager,
                 ui_setup,
                 generator,
                 sequence_manager,
                 exporter,
                 parent=None):
        
        super().__init__(graphboard_scene, parent)
        self.setAcceptDrops(True)
        self.setInteractive(True)
        self.dragging = None
        self.grid = grid
        self.graphboard_scene = graphboard_scene
        self.staff_manager = staff_manager
        self.info_tracker = info_tracker
        self.svg_manager = svg_manager
        self.generator = generator
        self.ui_setup = ui_setup
        self.sequence_manager = sequence_manager
        

        self.constants = Graphboard_Constants(self)
        self.exporter = exporter
        self.letter_renderers = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUV':
             self.letter_renderers[letter] = QSvgRenderer(f'images/letters/{letter}.svg')
        self.letter_item = QGraphicsSvgItem()
        from views.mini_graphboard_view import Mini_Graphboard_View
        if isinstance(self, Mini_Graphboard_View):
            self.graphboard_scene.setBackgroundBrush(Qt.transparent)
        elif self.graphboard_scene is not None:
            self.graphboard_scene.setBackgroundBrush(Qt.white) 
            self.graphboard_scene.addItem(self.letter_item)
            self.graphboard_scene.addItem(self.grid)
        self.arrow_manager = arrow_manager
        self.arrow_manager.connect_graphboard_scene(self.graphboard_scene)
        self.setFixedSize(int(750), int(900))
        self.VERTICAL_OFFSET = self.constants.VERTICAL_OFFSET
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.drag = Quadrant_Preview_Drag(self, self.dragging, self.info_tracker)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.drag_start_position = event.pos()
        self.setFocus()
        items = self.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.ItemIsMovable:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                for arrow in self.scene().selectedItems():
                    arrow.setSelected(False)
                items[0].setSelected(True)
            self.dragging = items[0]
            self.dragOffset = self.mapToScene(event.pos()) - self.dragging.pos()
            
        else:
            self.clear_selection()
            self.dragging = None

        if event.button() == Qt.LeftButton and not items:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToScene(event.pos()) - self.dragOffset
            movement = new_pos - self.dragging.pos()

            for arrow in self.scene().selectedItems():
                if isinstance(arrow, Arrow):
                    arrow.setPos(arrow.pos() + movement)
                    new_quadrant = self.drag.get_graphboard_quadrants(arrow.get_center_position())
                    
                    if arrow.quadrant != new_quadrant:
                        arrow.update_arrow_for_new_quadrant(new_quadrant)
                        self.info_tracker.update()

    def dragMoveEvent(self, event):
        dropped_svg = event.mimeData().text()
        base_name = os.path.basename(dropped_svg)
        color = base_name.split('_')[0]

        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                if arrow.color == color:
                    event.ignore()
                    QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
                    return
        event.accept()
        QToolTip.hideText() 

    def dropEvent(self, event):
        self.setFocus()
        event.setDropAction(Qt.CopyAction)
        event.accept()
        
        dropped_arrow_svg = event.mimeData().text()
        self.arrow = Arrow(dropped_arrow_svg, self, self.info_tracker, self.svg_manager, self.arrow_manager, None, self.staff_manager, None)
        self.scene().addItem(self.arrow)
        pos = self.mapToScene(event.pos()) - self.arrow.boundingRect().center()
        self.arrow.setPos(pos)

        self.clear_selection()
        self.arrow.setSelected(True)

        adjusted_arrow_pos = self.arrow.pos() + self.arrow.boundingRect().center()
        quadrant = self.drag.get_graphboard_quadrants(adjusted_arrow_pos)
        self.drag.update_arrow_svg(self.arrow, quadrant)
        self.arrow.update_attributes()

        self.info_tracker.update()

    ### GETTERS ###


    def get_state(self):
        state = {
            'arrows': [],
            'staffs': [],
            'grid': None
        }
        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                state['arrows'].append({
                    'color': arrow.color,
                    'position': arrow.pos(),
                    'quadrant': arrow.quadrant,
                    'rotation_direction': arrow.rotation_direction,
                    'svg_file': arrow.svg_file
                })
            elif isinstance(arrow, Staff):
                state['staffs'].append({
                    'position': arrow.pos(),
                    'color': arrow.color,
                    'svg_file': arrow.svg_file
                })
            elif isinstance(arrow, Grid):
                state['grid'] = {
                    'position': arrow.pos(),
                    'svg_file': arrow.svg_file
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
    
    def get_current_arrow_positions(self):
        red_position = None
        blue_position = None

        for arrow in self.scene().items():
            if isinstance(arrow, Arrow):
                center = arrow.pos() + arrow.boundingRect().center()
                if arrow.color == 'red':
                    red_position = center
                elif arrow.color == 'blue':
                    blue_position = center
        print(red_position, blue_position)
        return red_position, blue_position

    def get_selected_items(self):
        return self.graphboard_scene.selectedItems()
    
    def get_selected_arrows(self):
        selected_arrows = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                selected_arrows.append(item)
        return selected_arrows
    
    def get_selected_staffs(self):
        selected_staffs = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Staff):
                selected_staffs.append(item)
        return selected_staffs
    
    def get_bounding_box(self):
        bounding_boxes = []
        for arrow in self.scene().items():
            if isinstance(arrow, QGraphicsRectItem):
                bounding_boxes.append(arrow)
        return bounding_boxes

    def get_attributes(self):
        attributes = {}
        base_name = os.path.basename(self.svg_file)
        parts = base_name.split('_')

        attributes['color'] = parts[0]
        attributes['type'] = parts[1]
        attributes['rotation_direction'] = 'Clockwise' if parts[2] == 'r' else 'Anti-clockwise'
        attributes['quadrant'] = parts[3].split('.')[0]

        return attributes
    

    ### SELECTION ###

    def select_all_items(self):
        for item in self.scene().items():
            item.setSelected(True)

    def select_all_arrows(self):
        for arrow in self.graphboard_scene.items():
            if isinstance(arrow, Arrow):
                arrow.setSelected(True)

    def clear_selection(self):
        for arrow in self.scene().selectedItems():
            arrow.setSelected(False)



    ### SETTERS ###


    def set_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker

    def connect_generator(self, generator):
        self.generator = generator


    ### EVENTS ###

    def resizeEvent(self, event): # KEEP THIS TO POSITION THE GRID
        self.setSceneRect(QRectF(self.rect()))
        super().resizeEvent(event)

    def fkeyPressEvent(self, event):
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

        for arrow in self.scene().selectedItems():
            if isinstance(arrow, Arrow):
                arrow.moveBy(dx, dy)

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.get_selected_items()
        if isinstance(clicked_item, Arrow):
            arrow_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_manager.delete_arrow(selected_items))
            arrow_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_manager.rotate_arrow("right", selected_items))
            arrow_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_manager.rotate_arrow("left", selected_items))
            arrow_menu.addAction(rotate_left_action)

            mirror_action = QAction('Mirror', self)
            mirror_action.triggered.connect(lambda: self.arrow_manager.mirror_arrow(selected_items))
            arrow_menu.addAction(mirror_action)

            bring_forward_action = QAction('Bring Forward', self)
            bring_forward_action.triggered.connect(lambda: self.arrow_manager.bringForward(selected_items))
            arrow_menu.addAction(bring_forward_action)
            arrow_menu.exec_(event.globalPos())

        elif isinstance(clicked_item, Staff):
            staff_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_manager.delete_staff(selected_items))
            staff_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_manager.rotateArrow("right", selected_items))
            staff_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_manager.rotateArrow("left", selected_items))
            staff_menu.addAction(rotate_left_action)
            staff_menu.exec_(event.globalPos())

        else: 
            graphboard_menu = QMenu(self)

            swap_colors_action = QAction('Swap Colors', self)
            swap_colors_action.triggered.connect(lambda: self.arrow_manager.swap_colors(self.get_selected_items()))
            graphboard_menu.addAction(swap_colors_action)

            select_all_action = QAction('Select All', self)
            select_all_action.triggered.connect(self.arrow_manager.selectAll)
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

    def update_letter(self, letter):
        if letter is None or letter == 'None':
            svg_file = f'images/letters/blank.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        if letter is not None and letter != 'None':
            svg_file = f'images/letters/{letter}.svg'
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                print(f"Invalid SVG file: {svg_file}")
                return
            self.letter_item.setSharedRenderer(renderer)

        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width() / 2, 750)

    def clear(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item

class Quadrant_Preview_Drag(QDrag):
    def __init__(self, source, arrow, info_tracker, *args, **kwargs):
        super().__init__(source, *args, **kwargs)
        self.arrow = arrow
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
        self.update_arrow_svg(self.arrow, quadrant)
        new_svg = f'images\\arrows\\red\\r\\anti\\red_anti_r_{quadrant}.svg'
        arrow_renderer = QSvgRenderer(new_svg)
        self.arrow.setSharedRenderer(arrow_renderer)

        if arrow_renderer.isValid():
            pixmap = QPixmap(self.pixmap().size())
            painter = QPainter(pixmap)
            arrow_renderer.render(painter)
            painter.end()
            self.setPixmap(pixmap)

    def get_graphboard_quadrants(self, mouse_pos):
        mime_data = self.mimeData()
        if mime_data is not None:
            base_name = os.path.basename(mime_data.text())
        else:
            base_name = ""
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
            new_svg = f'images\\arrows\\shift\\{arrow.motion_type}\\red_anti_{arrow.rotation_direction}_{quadrant}_{arrow.turns}.svg'
        elif base_name.startswith('red_pro'):
            new_svg = f'images\\arrows\\shift\\{arrow.motion_type}\\red_pro_{arrow.rotation_direction}_{quadrant}_{arrow.turns}.svg'
        elif base_name.startswith('blue_anti'):
            new_svg = f'images\\arrows\\shift\\{arrow.motion_type}\\blue_anti_{arrow.rotation_direction}_{quadrant}_{arrow.turns}.svg'
        elif base_name.startswith('blue_pro'):
            new_svg = f'images\\arrows\\shift\\{arrow.motion_type}\\blue_pro_{arrow.rotation_direction}_{quadrant}_{arrow.turns}.svg'
        else:
            print(f"update_arrow_svg -- Unexpected svg_file: {arrow.svg_file}")
            new_svg = arrow.svg_file 

        arrow_renderer = QSvgRenderer(new_svg)
        if arrow_renderer.isValid():
            arrow.setSharedRenderer(arrow_renderer)
            arrow.svg_file = new_svg
        if arrow.motion_type == 'pro' or arrow.motion_type == 'anti':
            arrow.set_attributes_from_filename()
            arrow.quadrant = self.get_graphboard_quadrants(arrow.pos() + arrow.boundingRect().center())
            pos = self.source().get_quadrant_center(quadrant) - arrow.boundingRect().center()
            arrow.setPos(pos)

