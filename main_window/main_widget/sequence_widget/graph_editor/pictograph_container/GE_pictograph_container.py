from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from ..GE_pictograph_view import GE_PictographView, GE_Pictograph

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from ..graph_editor import GraphEditor

# pictograph_container.py


class GraphEditorPictographContainer(QWidget):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setup_pictograph()

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.GE_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def setup_pictograph(self):
        self.GE_pictograph = GE_Pictograph(self)
        self.GE_pictograph_view = GE_PictographView(self, self.GE_pictograph)

    def update_GE_pictograph(self, reference_beat: "Beat") -> None:
        view = self.GE_pictograph_view
        
        if reference_beat.view.is_start_pos:
            view.is_start_pos = True
        else:
            view.is_start_pos = False
            
        view.pictograph.is_blank = False
        view.reference_beat = reference_beat
        view.pictograph.updater.update_pictograph(reference_beat.pictograph_dict)
        if reference_beat.number_manager.beat_number_text != "0":
            beat_number_text = reference_beat.number_manager.beat_number_text
            view.pictograph.number_manager.add_beat_number(beat_number_text)

    def resizeEvent(self, event):
        size = self.graph_editor.height()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
