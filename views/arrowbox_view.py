import os
from PyQt6.QtWidgets import QGraphicsView, QFrame, QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from PyQt6.QtGui import QPixmap, QDrag, QImage, QPainter, QCursor, QColor
from PyQt6.QtCore import Qt, QMimeData, QPointF
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow import Arrow
from settings import *



class ArrowBox_View(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        self.drag = None
        self.drag_state = {} 
        self.graphboard_view = main_widget.graphboard_view
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.arrowbox_scene = QGraphicsScene()
        self.setScene(self.arrowbox_scene)
        self.configure_arrowbox_frame()
        self.populate_arrows()
        self.finalize_arrowbox_configuration()

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
                mime_data = QMimeData()
                mime_data.setText(arrow.svg_file)
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
                        new_svg = f'images/arrows/shift/anti/red_anti_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('red_pro'):
                        new_svg = f'images/arrows/shift/pro/red_pro_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('blue_anti'):
                        new_svg = f'images/arrows/shift/anti/blue_anti_{self.orientation}_{quadrant}_0.svg'
                    elif base_name.startswith('blue_pro'):
                        new_svg = f'images/arrows/shift/pro/blue_pro_{self.orientation}_{quadrant}_0.svg'
                    else:
                        print(f"Unexpected svg_file: {self.svg_file}")
                        

        try:
            # Assuming self.drag is the QDrag object
            if self.drag is not None:
                # Execute the drag and drop operation
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
        default_arrows = ['red_pro_r_ne_0.svg', 'red_anti_r_ne_0.svg', 'blue_pro_r_sw_0.svg', 'blue_anti_r_sw_0.svg']

        for dirpath, dirnames, filenames in os.walk(ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for svg_file in svgs_full_paths:
            self.create_and_configure_arrow(svg_file, default_arrows)

    def create_and_configure_arrow(self, svg_file, default_arrows):
        file_name = os.path.basename(svg_file)
        
        svg_item_count_red_pro = 0
        svg_item_count_red_anti = 0
        svg_item_count_blue_pro = 0
        svg_item_count_blue_anti = 0
        spacing = 200 * GRAPHBOARD_SCALE
        y_pos_red = 0
        y_pos_blue = 200 * GRAPHBOARD_SCALE
        
        if file_name in default_arrows:
            
            motion_type = file_name.split('_')[1]
            arrow_item = Arrow(svg_file, self.main_widget.graphboard_view, self.main_widget.info_tracker, self.main_widget.svg_manager, self.main_widget.arrow_manager, motion_type, self.main_widget.staff_manager, None)
            arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            arrow_item.setScale(GRAPHBOARD_SCALE * 0.75)

            if 'red' in file_name:
                if 'pro' in file_name:
                    arrow_item.setPos(svg_item_count_red_pro * spacing, y_pos_red) # Red pro
                    svg_item_count_red_pro += 1
                elif 'anti' in file_name:
                    arrow_item.setPos((svg_item_count_red_anti + 1) * spacing, y_pos_red) # Red Anti
                    svg_item_count_red_anti += 1
            elif 'blue' in file_name:
                if 'pro' in file_name:
                    arrow_item.setPos(svg_item_count_blue_pro * spacing, y_pos_blue) # Blue pro
                    svg_item_count_blue_pro += 1
                elif 'anti' in file_name:
                    arrow_item.setPos((svg_item_count_blue_anti + 1) * spacing, y_pos_blue) # Blue Anti
                    svg_item_count_blue_anti += 1
            self.arrowbox_scene.addItem(arrow_item) 
            self.main_widget.arrows.append(arrow_item)

    def finalize_arrowbox_configuration(self):
        self.objectbox_layout.addWidget(self)
        self.arrowbox_frame.setFixedSize(int(500 * GRAPHBOARD_SCALE), int(600 * GRAPHBOARD_SCALE))
        self.arrowbox_frame = self.arrowbox_frame

