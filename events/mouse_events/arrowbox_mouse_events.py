from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtCore import Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication
from resources.constants import GRAPHBOARD_SCALE
from objects.arrow.arrow_drag_preview import ArrowDragPreview
from objects.arrow.arrow import Arrow
from objects.staff.staff import Staff

# import QGraphicsItem
from PyQt6.QtWidgets import QGraphicsItem


class ArrowBoxMouseEvents:
    dragged_arrow = None
    current_rotation_angle = 0

    def __init__(self, arrowbox_view):
        self.arrowbox_view = arrowbox_view
        self.graphboard_view = arrowbox_view.graphboard_view
        self.graphboard_scene = self.graphboard_view.scene()
        self.staff_factory = self.graphboard_view.staff_handler.staff_factory
        self.dragging = False

    def initialize_drag(self, view, arrow, event):
        if not self.is_click_on_arrow(view, event):
            return
        self.graphboard_view.mouse_events.arrow_dragged = True  # Set the flag
        self.setup_dragging(arrow)

    def setup_dragging(self, arrow):
        self.dragging = True
        self.state_saved = False
        self.arrow = arrow
        self.dragged_arrow = arrow
        self.graphboard_view.dragged_arrow = self.dragged_arrow

    def create_and_show_drag_preview(self, view, event, arrow):
        self.drag_preview = ArrowDragPreview(arrow)
        self.drag_preview.setParent(QApplication.instance().activeWindow())
        self.drag_preview.show()
        self.has_entered_graphboard_once = False
        self.arrowbox_view.dragging = True
        self.move_drag_preview_to_cursor(view, event, arrow)

    def move_drag_preview_to_cursor(self, view, event, arrow):
        if hasattr(
            self, "drag_preview"
        ):  # Add this line to check if 'drag_preview' exists
            main_window = view.window()
            local_pos = view.mapTo(main_window, event.pos())
            if self.drag_preview is not None:
                self.drag_preview.move(
                    local_pos - (arrow.center * GRAPHBOARD_SCALE).toPoint()
                )

    def is_click_on_arrow(self, view, event):
        items = view.items(event.pos())
        return any(isinstance(item, Arrow) for item in items)

    def update_arrow_drag_preview(self, view, event):
        over_graphboard = self.is_over_graphboard(view, event)

        if over_graphboard:
            self.handle_drag_inside_graphboard(view, event)

        self.move_drag_preview_to_cursor(view, event, self.arrow)

    def is_over_graphboard(self, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = self.graphboard_view.mapFrom(
            view.window(), pos_in_main_window
        )
        return self.graphboard_view.rect().contains(local_pos_in_graphboard)

    def handle_drag_inside_graphboard(self, view, event):
        if self.drag_preview is not None:
            if self.has_entered_graphboard_once is False:
                self.has_entered_graphboard_once = True

            local_pos_in_graphboard = self.graphboard_view.mapFrom(
                view.window(), view.mapTo(view.window(), event.pos())
            )
            new_quadrant = self.graphboard_view.get_graphboard_quadrants(
                self.graphboard_view.mapToScene(local_pos_in_graphboard)
            )
            for arrow in self.graphboard_scene.items():
                if isinstance(arrow, Arrow) and arrow.color == self.dragged_arrow.color:
                    self.graphboard_scene.removeItem(arrow)
            if self.drag_preview is not None:
                self.update_drag_preview(new_quadrant)

    def update_drag_preview(self, new_quadrant):
        self.drag_preview.in_graphboard = True
        self.drag_preview.quadrant = new_quadrant
        self.rotate_drag_preview()

    def rotate_drag_preview(self):
        renderer = QSvgRenderer(
            self.dragged_arrow.svg_file
        )  # dragged_arrow is the arrow object that we picked up from the arrowbox
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.dragged_arrow.get_rotation_angle(
            self.drag_preview.quadrant,
            self.drag_preview.motion_type,
            self.drag_preview.rotation_direction,
        )

        unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
        unrotated_pixmap = self.drag_preview.label.pixmap().transformed(
            unrotate_transform
        )

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.current_rotation_angle = angle
        self.drag_preview.label.setPixmap(rotated_pixmap)

        (
            self.drag_preview.start_location,
            self.drag_preview.end_location,
        ) = self.dragged_arrow.attributes.get_start_end_locations(
            self.drag_preview.motion_type,
            self.drag_preview.rotation_direction,
            self.drag_preview.quadrant,
        )

    def handle_mouse_move(self, view, event):
        self.update_arrow_drag_preview(view, event)
        if self.drag_preview is not None:
            self.graphboard_view.dragMoveEvent(event, self.drag_preview)

    def handle_mouse_release(self, view, event, drag_preview):
        if hasattr(self, "drag_preview"):
            self.reset_on_mouse_release(view, event)

        over_graphboard = self.is_over_graphboard(view, event)

        if (
            self.dragging
        ):
            if not over_graphboard:
                
                if self.has_entered_graphboard_once:
                    # Create an arrow at the most recent position when it was in the graphboard
                    new_arrow_dict = {
                        "color": self.drag_preview.color,
                        "motion_type": self.drag_preview.motion_type,
                        "rotation_direction": self.drag_preview.rotation_direction,
                        "quadrant": self.drag_preview.quadrant,
                        "start_location": self.drag_preview.start_location,
                        "end_location": self.drag_preview.end_location,
                        "turns": self.drag_preview.turns,
                    }

                    new_arrow = self.graphboard_view.arrow_factory.create_arrow(
                        self.graphboard_view, new_arrow_dict
                    )

                    new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
                    self.graphboard_view.clear_selection()

                    new_arrow.setSelected(True)
                    # find the staff on the graphboard of a matching color and set arrow.staff to that staff
                    for item in self.graphboard_scene.items():
                        if isinstance(item, Arrow):
                            if item.color == new_arrow.color:
                                new_arrow.staff = item.staff
                                item.staff.arrow = new_arrow
                                break

                    self.graphboard_scene.addItem(new_arrow)

                    # find the staff of the smae color on the arrowbox and set arrow.staff to that staff
                    for item in self.arrowbox_view.arrowbox_scene.items():
                        if isinstance(item, Staff):
                            if item.color == new_arrow.color:
                                new_arrow.staff = item
                                break

                    # position the arrow according to its attributes
                    new_arrow.arrow_manager.arrow_positioner.update_arrow_position(
                        self.graphboard_view
                    )

                elif not self.has_entered_graphboard_once:
                    self.drag_preview.deleteLater()
                    self.drag_preview = None
            
            if self.drag_preview is not None:
                self.drag_preview.deleteLater()
                self.drag_preview = None

    def reset_on_mouse_release(self, view, event):
        over_graphboard = self.is_over_graphboard(view, event)

        self.current_rotation_angle = 0
        if over_graphboard:
            self.graphboard_view.mouse_events.handle_drop_event(
                event, self.drag_preview
            )
        self.graphboard_view.mouse_events.arrow_dragged = False  # Reset the flag
