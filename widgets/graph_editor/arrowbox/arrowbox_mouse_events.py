
from PyQt6.QtGui import QPixmap, QPainter,  QTransform, QCursor
from PyQt6.QtCore import Qt, QPointF, QPoint
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication
from constants import GRAPHBOARD_SCALE
from objects.arrow.arrow_drag_preview import ArrowDragPreview
import sys



class ArrowBoxMouseEvents():
    dragged_arrow = None
    
    def __init__(self, arrowbox_view):
        self.arrowbox_view = arrowbox_view


    def initialize_drag(self, view, arrow, event):
        print("initialize_drag called")
    
        global dragged_arrow  # Declare that we're using the global variable
        dragged_arrow = arrow
    
        self.arrow = arrow
        view.artboard_start_position = event.pos()
        view.dragging = True
        view.dragged_arrow = arrow
        view.graphboard_view.dragged_arrow = view.dragged_arrow
        view.dragged_arrow_scale = GRAPHBOARD_SCALE
        view.dragged_arrow_color = arrow.color
        view.current_quadrant = None

        # Create pixmap for drag preview
        new_svg_data = view.dragged_arrow.set_svg_color(view.dragged_arrow.svg_file, view.dragged_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        view.drag_preview = ArrowDragPreview(pixmap)
        view.drag_preview.setParent(QApplication.instance().activeWindow())
        view.drag_preview.show()

        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview to the local cursor position
        view.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())

    
    def update_drag_preview(self, view, event):
        over_graphboard = view.graphboard_view.rect().contains(view.graphboard_view.mapFromGlobal(view.mapToGlobal(event.pos())))
        new_quadrant = view.graphboard_view.get_graphboard_quadrants(view.graphboard_view.mapToScene(event.pos())) if over_graphboard else view.current_quadrant
        
        if over_graphboard:
            if new_quadrant != view.current_quadrant:
                view.current_quadrant = new_quadrant
                renderer = QSvgRenderer(view.dragged_arrow.svg_file)
                scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
                pixmap = QPixmap(scaled_size)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                with painter as painter:
                    renderer.render(painter)

                angle = view.dragged_arrow.get_rotation_angle(new_quadrant)
                transform = QTransform().rotate(angle)
                rotated_pixmap = view.drag_preview.label.pixmap().transformed(transform)
                view.drag_preview.setPixmap(rotated_pixmap)
                
        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview
        view.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())

            
    def handle_mouse_release(self, view, event):
        arrow = view.itemAt(event.pos())
        if arrow is not None and arrow in view.drag_state:
            del view.drag_state[arrow]
            view.dragging = False
            view.dragged_arrow = None
            view.graphboard_view.temp_arrow = None
            view.graphboard_view.temp_staff = None
        if view.drag_preview is not None:
            view.drag_preview.close()
            view.drag_preview = None

