import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import QGraphicsView, QFrame, QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from resources.constants import GRAPHBOARD_SCALE, ARROWBOX_SCALE
from events.mouse_events.arrowbox_mouse_events import ArrowBoxMouseEvents
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from objects.arrow.arrow import Arrow

class ArrowBoxView(QGraphicsView):
    def __init__(self, main_widget, graphboard_view, info_frame, arrow_manager):
        super().__init__()
        self.info_frame = info_frame
        self.drag_preview = None
        self.drag_state = {} 
        self.dragging = False
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
        self.view_scale = ARROWBOX_SCALE
        self.populate_arrows()
        self.objectbox_layout.addWidget(self)
        self.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.current_quadrant = None
        self.mouse_events = ArrowBoxMouseEvents(self)

    def configure_arrowbox_frame(self):
        self.arrowbox_frame = QFrame(self.main_window)
        self.objectbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.objectbox_layout)

    def populate_arrows(self):
        
        arrow1 = {
            'color': 'red',
            'motion_type': 'pro',
            'rotation_direction': 'r',
            'quadrant': 'ne',
            'start_location': 'n',
            'end_location': 'e',
            'turns': 0
        }
        
        arrow2 = {
            'color': 'blue',
            'motion_type': 'anti',
            'rotation_direction': 'l',
            'quadrant': 'ne',
            'start_location': 'n',
            'end_location': 'e',
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
        
    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        items = self.scene().items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            self.dragged_item = arrows[0]
        if arrows and event.button() == Qt.MouseButton.LeftButton:
            self.mouse_events.initialize_drag(self, self.dragged_item, event)
            self.dragging = True
        else:
            event.ignore()


    def mouseMoveEvent(self, event):
        self.mouse_events.handle_mouse_move(self, event)

    def mouseReleaseEvent(self, event):
        self.mouse_events.handle_mouse_release(self, event, self.drag_preview)
        self.dragging = False