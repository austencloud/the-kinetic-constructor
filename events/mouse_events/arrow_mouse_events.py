class ArrowMouseEvents:
    def __init__(self, arrow):
        self.arrow = arrow

    def handle_graphboard_view(self, arrow, event):
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

            self.update_staff_attributes(arrow)
            arrow.view.info_handler.update()

    def handle_pictograph_view(self, arrow, event):
        new_pos = arrow.mapToScene(event.pos()) - arrow.drag_offset / 2
        arrow.setPos(new_pos)

    def update_staff_attributes(self, arrow):
        updated_staff_dict = {
            "color": arrow.color,
            "location": arrow.end_location,
            "layer": 1,
        }
        arrow.staff.attributes.update_attributes(arrow.staff, updated_staff_dict)
        arrow.staff.update_appearance()
        arrow.staff.setPos(
            arrow.view.staff_handler.staff_xy_locations[arrow.staff.location]
        )
