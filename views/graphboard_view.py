import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from objects.staff import Staff
from objects.grid import Grid
from objects.arrow import Arrow
from settings import *
from managers.graphboard_manager import Graphboard_Manager
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
                 json_manager,
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
        self.arrow_manager = arrow_manager
        self.exporter = exporter
        self.json_manager = json_manager
        self.letter_renderers = {}
        
        self.letters = self.json_manager.load_all_letters()

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

        self.arrow_manager.connect_graphboard_scene(self.graphboard_scene)
        self.setFixedSize(GRAPHBOARD_WIDTH, GRAPHBOARD_HEIGHT)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        (self, self.info_tracker)
        
    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setFocus()
        items = self.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.ItemIsMovable:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.clear_selection()
                items[0].setSelected(True)
        else:
            self.clear_selection()
        super().mousePressEvent(event)
        
        # Check if any item got selected after calling the parent class's method
        if items and not items[0].isSelected():
            items[0].setSelected(True)

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
        
        quadrant = self.get_graphboard_quadrants(self.arrow.pos() + self.arrow.boundingRect().center())
        self.arrow.update_arrow_for_new_quadrant(quadrant)
        self.arrow.update_attributes()
        self.arrow.arrow_manager.update_arrow_position(self.arrow)
        self.info_tracker.update()

    ### GETTERS ###

    def get_graphboard_quadrants(self, mouse_pos):
        adjusted_mouse_y = mouse_pos.y() + VERTICAL_OFFSET
        if adjusted_mouse_y < self.sceneRect().height() / 2:
            if mouse_pos.x() < self.sceneRect().width() / 2:
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if mouse_pos.x() < self.sceneRect().width() / 2:
                quadrant = 'sw'
            else:
                quadrant = 'se'
        return quadrant

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
                    'rotation_direction': item.rotation_direction,
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
        # Calculate the layer 2 points on the graphboard based on the grid
        graphboard_layer2_points = {}
        for point_name in ['NE_layer2_point', 'SE_layer2_point', 'SW_layer2_point', 'NW_layer2_point']:
            cx, cy = self.grid.get_circle_coordinates(point_name)
            graphboard_layer2_points[point_name] = QPointF(cx, cy)  # Subtract VERTICAL_OFFSET from y-coordinate

        # Map the quadrants to the corresponding layer 2 points
        centers = {
            'ne': graphboard_layer2_points['NE_layer2_point'],
            'se': graphboard_layer2_points['SE_layer2_point'],
            'sw': graphboard_layer2_points['SW_layer2_point'],
            'nw': graphboard_layer2_points['NW_layer2_point']
        }

        return centers.get(quadrant, QPointF(0, 0))  # Subtract VERTICAL_OFFSET from default y-coordinate

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
            rotate_right_action.triggered.connect(lambda: self.arrow_manager.rotate_arrow("right", selected_items))
            staff_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_manager.rotate_arrow("left", selected_items))
            staff_menu.addAction(rotate_left_action)
            staff_menu.exec_(event.globalPos())

        else: 
            graphboard_menu = QMenu(self)

            swap_colors_action = QAction('Swap Colors', self)
            swap_colors_action.triggered.connect(lambda: self.arrow_manager.swap_colors(self.get_selected_items()))
            graphboard_menu.addAction(swap_colors_action)

            select_all_action = QAction('Select All', self)
            select_all_action.triggered.connect(self.arrow_manager.select_all_arrows)
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

        self.letter_item.setPos(self.width() / 2 - self.letter_item.boundingRect().width() / 2, GRAPHBOARD_WIDTH)

    def clear(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item

