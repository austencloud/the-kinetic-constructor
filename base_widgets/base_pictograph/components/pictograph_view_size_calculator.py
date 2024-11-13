from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base_widgets.base_pictograph.components.pictograph_view import PictographView


class PictographViewSizeCalculator:
    def __init__(self, pictograph_view: "PictographView") -> None:
        self.pictograph_view = pictograph_view
        self.pictograph = pictograph_view.pictograph

    def calculate_view_size(self) -> int:
        if self.pictograph.parent_widget:
            COLUMN_COUNT = self.pictograph.parent_widget.COLUMN_COUNT
        else:
            COLUMN_COUNT = 8

        spacing = (
            self.pictograph.main_widget.manual_builder.option_picker.scroll_area.spacing
        )

        calculated_width = int(
            (self.pictograph.main_widget.manual_builder.width() / COLUMN_COUNT)
            - spacing
        )

        view_width = (
            calculated_width
            if calculated_width
            < self.pictograph.main_widget.manual_builder.height() // 8
            else self.pictograph.main_widget.manual_builder.height() // 8
        )

        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))

        view_width = view_width - (outer_border_width) - (inner_border_width) - spacing

        return view_width
