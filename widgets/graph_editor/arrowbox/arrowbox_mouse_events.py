
from PyQt6.QtGui import QPixmap, QPainter,  QTransform, QCursor
from PyQt6.QtCore import Qt, QPointF, QPoint
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication
from constants import GRAPHBOARD_SCALE
from objects.arrow.arrow_drag_preview import ArrowDragPreview
import sys



class ArrowBoxMouseEvents():
    dragged_arrow = None
    current_rotation_angle = 0  # Add this line to keep track of the current rotation angle

    def __init__(self, arrowbox_view):
        self.arrowbox_view = arrowbox_view


    def initialize_drag(self, view, arrow, event):
        print("initialize_drag called")
    
        self.arrow = arrow
        view.artboard_start_position = event.pos()
        view.dragged_arrow = arrow
        view.graphboard_view.dragged_arrow = view.dragged_arrow
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

        view.drag_preview = ArrowDragPreview(pixmap, self.arrow)
        view.drag_preview.setParent(QApplication.instance().activeWindow())
        view.drag_preview.show()

        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview to the local cursor position
        view.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())

    
    def update_drag_preview(self, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = view.graphboard_view.mapFrom(view.window(), pos_in_main_window)
        over_graphboard = view.graphboard_view.rect().contains(local_pos_in_graphboard)

        if over_graphboard:
            new_quadrant = view.graphboard_view.get_graphboard_quadrants(view.graphboard_view.mapToScene(local_pos_in_graphboard))
            
            if new_quadrant != view.current_quadrant:
                view.current_quadrant = new_quadrant
                renderer = QSvgRenderer(view.dragged_arrow.svg_file)
                scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
                pixmap = QPixmap(scaled_size)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                with painter as painter:
                    renderer.render(painter)

                angle = view.dragged_arrow.get_rotation_angle(new_quadrant, view.drag_preview.motion_type, view.drag_preview.rotation_direction)

                unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
                unrotated_pixmap = view.drag_preview.label.pixmap().transformed(unrotate_transform)

                rotate_transform = QTransform().rotate(angle)
                rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

                self.current_rotation_angle = angle
                view.drag_preview.setPixmap(rotated_pixmap)
                
        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview
        view.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())

            
    def handle_mouse_release(self, view, event):
        arrow = view.itemAt(event.pos())
        if arrow is not None and arrow in view.drag_state:
            del view.drag_state[arrow]
            view.dragged_arrow = None
            view.graphboard_view.temp_arrow = None
            view.graphboard_view.temp_staff = None
        if view.drag_preview is not None:
            view.drag_preview.close()
            view.drag_preview = None
        self.current_rotation_angle = 0

