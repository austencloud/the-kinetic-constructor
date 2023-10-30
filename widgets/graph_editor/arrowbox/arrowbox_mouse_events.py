
from PyQt6.QtGui import QPixmap, QPainter,  QTransform
from PyQt6.QtCore import Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication
from constants import GRAPHBOARD_SCALE
from objects.arrow.arrow_drag_preview import ArrowDragPreview


class ArrowBoxMouseEvents():
    dragged_arrow = None
    current_rotation_angle = 0  # Add this line to keep track of the current rotation angle

    def __init__(self, arrowbox_view):
        self.arrowbox_view = arrowbox_view
        self.graphboard_view = arrowbox_view.graphboard_view

    def initialize_drag(self, view, arrow, event):
        print("initialize_drag called")
    
        self.dragging = True
        self.arrow = arrow
        self.dragged_arrow = arrow
        self.graphboard_view.dragged_arrow = self.dragged_arrow

        attr_dict = arrow.attributes.get_attributes(arrow)

        # Create pixmap for drag preview
        self.drag_preview = ArrowDragPreview(self.arrow)
        self.drag_preview.setParent(QApplication.instance().activeWindow())
        self.drag_preview.show()

        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview to the local cursor position
        self.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())

    def update_arrow_drag_preview(self, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = self.graphboard_view.mapFrom(view.window(), pos_in_main_window)
        over_graphboard = self.graphboard_view.rect().contains(local_pos_in_graphboard)

        if over_graphboard:
            new_quadrant = self.graphboard_view.get_graphboard_quadrants(self.graphboard_view.mapToScene(local_pos_in_graphboard))
            self.drag_preview.in_graphboard = True
            self.graphboard_view.current_quadrant = self.graphboard_view.mouse_events.get_current_quadrant(event)
            
            if new_quadrant != self.drag_preview.quadrant:
                self.drag_preview.quadrant = new_quadrant
                renderer = QSvgRenderer(self.dragged_arrow.svg_file)
                scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
                pixmap = QPixmap(scaled_size)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                with painter as painter:
                    renderer.render(painter)

                angle = self.dragged_arrow.get_rotation_angle(new_quadrant, self.drag_preview.motion_type, self.drag_preview.rotation_direction)

                unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
                unrotated_pixmap = self.drag_preview.label.pixmap().transformed(unrotate_transform)

                rotate_transform = QTransform().rotate(angle)
                rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

                self.current_rotation_angle = angle
                self.drag_preview.label.setPixmap(rotated_pixmap)
                
                
            self.drag_preview.start_location, self.drag_preview.end_location = self.dragged_arrow.attributes.get_start_end_locations(self.drag_preview.motion_type, 
                                                                                                                                            self.drag_preview.rotation_direction, 
                                                                                                                                            self.drag_preview.quadrant)
        else:
            self.drag_preview.in_graphboard = False
            
        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())

        # Move the drag preview
        self.drag_preview.move(local_pos - (self.arrow.center*GRAPHBOARD_SCALE).toPoint())


    def handle_mouse_move(self, view, event):
        self.update_arrow_drag_preview(view, event)
        if self.dragging: 
            self.graphboard_view.dragMoveEvent(event, self.drag_preview)
        
            
    def handle_mouse_release(self, view, event, drag_preview):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = self.graphboard_view.mapFrom(view.window(), pos_in_main_window)
        over_graphboard = self.graphboard_view.rect().contains(local_pos_in_graphboard)
        
        self.current_rotation_angle = 0
        
        if over_graphboard:
            self.graphboard_view.mouse_events.handle_drop_event(event, self.drag_preview)
