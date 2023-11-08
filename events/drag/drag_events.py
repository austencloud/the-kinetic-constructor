from events.drag.drag_preview import DragPreview
from settings.string_constants import *
from PyQt6.QtWidgets import QGraphicsItem


class DragEvents:
    def __init__(self, drag):
        self.drag = drag
        self.graphboard = drag.graphboard
        self.arrowbox = drag.arrowbox
        self.scene_updater = drag.scene_updater
        self.drag_preview = None
        self.previous_quadrant = None
        self.init_invisible_arrow()

    def init_invisible_arrow(self):
        from objects.arrow.arrow import Arrow

        self.invisible_arrow = Arrow(self.graphboard, None)
        self.invisible_arrow.setVisible(False)
        self.graphboard.addItem(self.invisible_arrow)

    ### DRAG INITIALIZATION ###

    def start_drag(self, scene, target_arrow, event_pos):
        self.drag_preview = DragPreview(self.drag, target_arrow)
        self.drag_preview.setParent(scene.main_widget)
        self.drag_preview.move_to_cursor(scene, event_pos, target_arrow)
        self.drag_preview.show()

    ### DRAG INTO GRAPHBOARD ###

    def handle_drag_into_graphboard(self, view, event):
        if self.drag_preview:
            self.update_drag_preview_for_graphboard(view, event)

    def update_drag_preview_for_graphboard(self, view, event):
        if not self.drag_preview.has_entered_graphboard_once:
            self.just_entered_graphboard = True
            self.drag_preview.has_entered_graphboard_once = True

        local_pos_in_graphboard = self.helpers.get_local_pos_in_graphboard(view, event)
        scene_pos = self.graphboard.view.mapToScene(local_pos_in_graphboard)

        current_quadrant = self.graphboard.determine_quadrant(
            scene_pos.x(), scene_pos.y()
        )

        if self.previous_quadrant != current_quadrant:
            self.update_drag_preview_for_new_quadrant(current_quadrant)

    def update_drag_preview_for_new_quadrant(self, current_quadrant):
        for arrow in self.graphboard.arrows[
            :
        ]:  # Copy the list to avoid iteration issues
            if arrow.color == self.drag_preview.color:
                self.graphboard.removeItem(arrow)
                self.graphboard.arrows.remove(arrow)

        self.drag_preview.update_rotation_for_quadrant(current_quadrant)
        new_arrow = self.invisible_arrow.create_dict_from_arrow(self.drag_preview)
        self.invisible_arrow.update_attributes(new_arrow)
        self.previous_quadrant = current_quadrant
        self.update_staffs()

    def update_staffs(self):
        for staff in self.graphboard.staffs:
            if staff.color == self.drag_preview.color:
                staff.update_attributes({COLOR: self.drag_preview.color, LOCATION: self.invisible_arrow.end_location, LAYER: 1})
                staff.arrow = self.invisible_arrow
                self.invisible_arrow.staff = staff
                staff.setVisible(True)
                staff.update_appearance()

        self.graphboard.update_staffs()

    ### MOUSE MOVE ###

    def handle_mouse_move(self, scene, event, event_pos):
        if self.drag_preview:
            self.update_drag_preview(scene, event_pos)

    def update_drag_preview(self, scene, event_pos):
        over_graphboard = self.drag.helpers.is_over_graphboard(scene, event_pos)
        self.drag_preview.move_to_cursor(
            scene, event_pos, self.drag_preview.target_arrow
        )

        if over_graphboard:
            local_pos_in_graphboard = self.drag.helpers.get_local_pos_in_graphboard(
                scene, event_pos
            )
            scene_pos = self.graphboard.view.mapToScene(local_pos_in_graphboard)
            current_quadrant = self.graphboard.determine_quadrant(
                scene_pos.x(), scene_pos.y()
            )

            if self.previous_quadrant != current_quadrant:
                self.update_drag_preview_for_new_quadrant(current_quadrant)

    ### MOUSE RELEASE ###

    def handle_mouse_release(self, view_pos):
        if self.drag_preview:
            if view_pos not in self.arrowbox.view.rect():
                self.place_arrow_on_graphboard()
            else:
                self.drag_preview.deleteLater()

            self.scene_updater.cleanup_and_update_scene()
            self.drag.reset_drag_state()

    def handle_drop_event(self, event, event_pos):
        if self.dragging and event_pos:
            if (
                event_pos not in self.arrowbox.view.rect()
                and self.drag_preview.has_entered_graphboard_once
            ):
                self.place_arrow_on_graphboard(event)
                self.scene_updater.cleanup_and_update_scene()
            else:
                self.drag_preview.deleteLater()
                self.drag_preview = None

    def place_arrow_on_graphboard(self):
        self.invisible_arrow.setVisible(True)
        self.graphboard.clearSelection()
        self.invisible_arrow.setSelected(True)
        self.graphboard.arrows.append(self.invisible_arrow)

    def handle_mouse_press(self, event_pos):
        items = self.graphboard.items(event_pos)
        self.drag.select_or_deselect_items(items)
        if not items or not items[0].isSelected():
            self.graphboard.clear_selection()
