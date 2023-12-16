from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer

from data.letter_engine_data import letter_types
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from constants.string_constants import (
    BLUE,
    COLOR,
    END_LOCATION,
    LETTER_SVG_DIR,
    MOTION_TYPE,
    RED,
    ROTATION_DIRECTION,
    START_LOCATION,
    TURNS,
    START_ORIENTATION,
    END_ORIENTATION,
    START_LAYER,
    END_LAYER,
    ARROW_LOCATION,
)
from utilities.TypeChecking.Letters import Letters
from utilities.letter_engine import LetterEngine
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
    MotionAttributesDicts,
    List,
    Optional,
    Tuple,
)
from objects.pictograph.pictograph import Pictograph
from objects.pictograph.pictograph_menu_handler import PictographMenuHandler
from objects.pictograph.position_engines.arrow_positioner import ArrowPositioner
from objects.pictograph.position_engines.prop_positioner import PropPositioner
from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget", Sequence: "BeatFrame") -> None:
        super().__init__(main_widget, main_widget.graph_editor_widget.graph_editor)
        self.main_widget = main_widget
        self.sequence = Sequence

        self.setup_scene()
        self.setup_components(main_widget)
