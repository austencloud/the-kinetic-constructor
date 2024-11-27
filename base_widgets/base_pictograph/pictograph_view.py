from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_widget.beat_frame.styled_border_overlay import (
    StyledBorderOverlay,
)


if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.temp_beat_frame.temp_beat_frame import (
        TempBeatFrame,
    )
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from main_window.main_widget.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )
    from main_window.main_widget.sequence_builder.option_picker.option_picker import (
        OptionPicker,
    )
    from main_window.main_widget.sequence_builder.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    original_style: str
    parent: Union[
        "OptionPicker",
        "LearnWidget",
        "GraphEditor",
        "StartPosPicker",
        "AdvancedStartPosPicker",
        "SequenceWidgetBeatFrame",
        "TempBeatFrame",
    ]
    option_picker: "OptionPicker" = None
    learn_widget: "LearnWidget" = None
    graph_editor: "GraphEditor" = None
    start_pos_picker: "StartPosPicker" = None
    advanced_start_pos_picker: "AdvancedStartPosPicker" = None
    sequence_widget_beat_frame: "SequenceWidgetBeatFrame" = None
    temp_beat_frame: "TempBeatFrame" = None
    view_scale: float

    def __init__(self, pictograph: "BasePictograph", parent) -> None:
        super().__init__(pictograph, parent)
        self.pictograph = pictograph
        self.pictograph.container.layout().addWidget(self)
        # self.pictograph.styled_border_overlay = StyledBorderOverlay(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Trigger fitInView whenever the widget is resized."""
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
