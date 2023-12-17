from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget", beat_frame: "BeatFrame") -> None:
        super().__init__(
            main_widget, main_widget.graph_editor_widget.graph_editor, "beat"
        )
        self.main_widget = main_widget
        self.beat_frame = beat_frame
