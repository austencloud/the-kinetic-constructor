from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem, QApplication
from PyQt6.QtGui import QCursor, QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from resources.constants import GRAPHBOARD_SCALE, STATIC
from events.drag.drag_preview import DragPreview
from objects.staff.staff import Staff


class DragManager:
    ### INITIALIZATION ###

    def __init__(self):
        self.reset_drag_state()

    def initialize_dependencies(self, graphboard_view, arrowbox_view):
        self.graphboard_view = graphboard_view
        self.arrowbox_view = arrowbox_view
        self.graphboard_scene = self.graphboard_view.scene()
        self.arrow_factory = (
            self.graphboard_view.main_widget.arrow_manager.arrow_factory
        )
        self.info_handler = self.graphboard_view.info_handler
        self.staff_handler = self.graphboard_view.staff_handler
        self.staff_factory = self.graphboard_view.staff_handler.staff_factory

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0
        self.has_entered_graphboard_once = False

    ### DRAG EVENT HANDLING ###

    def start_drag(self, view, arrow, event):
        if not self.is_click_on_arrow(view, event):
            return
        self.drag_preview = DragPreview(self, arrow)
        self.arrow_dragged = True  # Set the flag
        self.dragging = True
        self.arrow = arrow
        self.graphboard_view.dragged_arrow = self.arrow
        self.create_and_show_drag_preview(arrow)
        self.drag_preview.move_to_cursor(view, event, self.arrow)  # Add this line

    def handle_mouse_press(self, event):
        self.graphboard_view.setFocus()
        items = self.graphboard_view.items(event.pos())
        self.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard_view.clear_selection()

    def handle_mouse_move(self, view, event):
        if self.drag_preview is not None:
            self.update_arrow_drag_preview(view, event)
            self.graphboard_view.dragMoveEvent(event, self.drag_preview)

            if self.has_entered_graphboard_once:
                new_arrow_dict = self.create_new_arrow_dict()
                self.invisible_arrow.arrow_manager.arrow_attributes.update_attributes(
                    self.invisible_arrow, new_arrow_dict
                )  # Implement a method to update arrow's properties
                board_state = self.graphboard_view.get_state()
                self.staff_handler.staff_positioner.reposition_staffs(
                    self.graphboard_scene, board_state
                )
                self.info_handler.update()

    def handle_drag_inside_graphboard(self, view, event):
        if not self.drag_preview:
            return

        if not self.has_entered_graphboard_once:
            self.has_entered_graphboard_once = True

            new_arrow_dict = self.create_new_arrow_dict()
            self.invisible_arrow = self.create_and_add_arrow(new_arrow_dict)
            self.invisible_arrow.setVisible(False)

        local_pos_in_graphboard = self.get_local_pos_in_graphboard(view, event)
        new_quadrant = self.graphboard_view.get_graphboard_quadrants(
            self.graphboard_view.mapToScene(local_pos_in_graphboard)
        )

        self.remove_matching_arrows_from_scene()
        self.drag_preview.update_rotation_for_quadrant(new_quadrant)

    def handle_mouse_release(self, view, event, drag_preview):
        if not hasattr(self, "drag_preview"):
            return

        self.handle_drop_event(event)
        self.reset_drag_state()

    ### HELPER METHODS ###

    def create_and_show_drag_preview(self, arrow):
        self.drag_preview = DragPreview(self, arrow)
        self.drag_preview.setParent(QApplication.instance().activeWindow())
        self.drag_preview.show()

    def is_click_on_arrow(self, view, event):
        from objects.arrow.arrow import Arrow

        items = view.items(event.pos())

        return any(isinstance(item, Arrow) for item in items)

    def update_arrow_drag_preview(self, view, event):
        over_graphboard = self.is_over_graphboard(view, event)

        if over_graphboard:
            self.handle_drag_inside_graphboard(view, event)

        self.drag_preview.move_to_cursor(view, event, self.arrow)

    def is_over_graphboard(self, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = self.graphboard_view.mapFrom(
            view.window(), pos_in_main_window
        )
        return self.graphboard_view.rect().contains(local_pos_in_graphboard)

    def get_local_pos_in_graphboard(self, view, event):
        return self.graphboard_view.mapFrom(
            view.window(), view.mapTo(view.window(), event.pos())
        )

    def remove_matching_arrows_from_scene(self):
        from objects.arrow.arrow import Arrow

        for arrow in self.graphboard_scene.items():
            if isinstance(arrow, Arrow) and arrow.color == self.arrow.color:
                self.graphboard_scene.removeItem(arrow)

    ### OBJECT CREATION AND UPDATE ###

    def create_new_arrow_dict(self):
        return {
            "color": self.drag_preview.color,
            "motion_type": self.drag_preview.motion_type,
            "rotation_direction": self.drag_preview.rotation_direction,
            "quadrant": self.drag_preview.quadrant,
            "start_location": self.drag_preview.start_location,
            "end_location": self.drag_preview.end_location,
            "turns": self.drag_preview.turns,
        }

    def create_new_staff_dict(self):
        return {
            "color": self.drag_preview.color,
            "location": self.drag_preview.end_location,
            "layer": 1,
        }

    def create_and_add_arrow(self, arrow_dict):
        new_arrow = self.arrow_factory.create_arrow(self.graphboard_view, arrow_dict)
        new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard_scene.addItem(new_arrow)
        return new_arrow

    def create_and_add_staff(self, staff_dict):
        new_staff = self.staff_factory.create_staff(self.graphboard_scene, staff_dict)
        self.graphboard_scene.addItem(new_staff)

        for staff in self.staff_handler.staffs_on_board:
            if staff.color == new_staff.color:
                self.staff_handler.staffs_on_board.remove(staff)

        self.staff_handler.staffs_on_board.append(new_staff)

        return new_staff

    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow

    def get_current_quadrant(self, event):
        return self.graphboard_view.get_graphboard_quadrants(
            self.graphboard_view.mapToScene(event.position().toPoint())
        )

    def update_temp_staff(self, drag_preview):
        if not self.arrow_dragged:
            return

        if self.graphboard_view.temp_staff:
            self.prev_staff_state = {
                "color": self.graphboard_view.temp_staff.color,
                "location": self.graphboard_view.temp_staff.location,
                "layer": self.graphboard_view.temp_staff.layer,
            }

        for temp_staff in self.graphboard_scene.items():
            if isinstance(temp_staff, Staff) and temp_staff.color == drag_preview.color:
                self.graphboard_scene.removeItem(temp_staff)

        temp_staff_dict = {
            "color": drag_preview.color,
            "location": drag_preview.end_location,
            "layer": 1,
        }

        self.temp_staff = self.staff_factory.create_staff(
            self.graphboard_view.graphboard_scene, temp_staff_dict
        )
        self.graphboard_view.temp_staff = self.temp_staff
        self.graphboard_scene.addItem(self.temp_staff)
        self.temp_staff.setPos(
            self.staff_handler.staff_xy_locations[drag_preview.end_location]
        )
        self.drag_preview = drag_preview
        self.graphboard_view.update_letter(
            self.info_handler.determine_current_letter_and_type()[0]
        )

    def handle_graphboard_view_drag(self, arrow, event):
        new_pos = arrow.mapToScene(event.pos()) - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        new_quadrant = arrow.view.get_graphboard_quadrants(new_pos + arrow.center)
        if arrow.quadrant != new_quadrant:
            arrow.quadrant = new_quadrant
            arrow.update_appearance()
            (
                arrow.start_location,
                arrow.end_location,
            ) = arrow.attributes.get_start_end_locations(
                arrow.motion_type, arrow.rotation_direction, arrow.quadrant
            )
            arrow.staff.location = arrow.end_location

            arrow.staff.attributes.update_attributes_from_arrow(arrow)
            arrow.view.info_handler.update()

    def handle_pictograph_view_drag(self, arrow, event):
        new_pos = arrow.mapToScene(event.pos()) - arrow.drag_offset / 2
        arrow.setPos(new_pos)

    def select_or_deselect_items(self, event, items):
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if (
                event.button() == Qt.MouseButton.LeftButton
                and event.modifiers() == Qt.KeyboardModifier.ControlModifier
            ):
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.graphboard_view.clear_selection()
                items[0].setSelected(True)

    ### DROP EVENT HANDLING ###

    def handle_drop_event(self, event):
        if not self.dragging:
            return

        if self.has_entered_graphboard_once:
            self.set_focus_and_accept_event(event)
            new_arrow_dict = self.create_new_arrow_dict()
            new_staff_dict = self.create_new_staff_dict()

            new_arrow = self.create_and_add_arrow(new_arrow_dict)
            new_staff = self.create_and_add_staff(new_staff_dict)

            self.graphboard_view.clear_selection()
            new_arrow.setSelected(True)

            self.link_arrow_and_staff(new_arrow, new_staff)

        self.cleanup_and_update_scene()
        self.update_info_handler()

    def set_focus_and_accept_event(self, event):
        self.graphboard_view.setFocus()
        event.accept()

    def cleanup_and_update_scene(self):
        self.drag_preview.deleteLater()
        self.graphboard_scene.removeItem(self.graphboard_view.temp_staff)
        self.graphboard_view.update_letter(
            self.info_handler.determine_current_letter_and_type()[0]
        )

        from objects.arrow.arrow import Arrow

        for item in self.graphboard_view.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.arrow_manager.arrow_positioner.update_arrow_position(
                    self.graphboard_view
                )

        for item in self.graphboard_view.graphboard_scene.items():
            if isinstance(item, Staff):
                item.setPos(
                    self.graphboard_view.staff_handler.staff_xy_locations[item.location]
                )

    def update_info_handler(self):
        self.graphboard_view.info_handler.update()
