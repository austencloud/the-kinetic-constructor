from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsScene
from data.prop_class_mapping import prop_class_mapping

from constants import *
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.prop_types import PropTypes
from widgets.factories.prop_factory import PropFactory

if TYPE_CHECKING:
    from widgets.sequence_widget.beat_frame.beat import Beat
    from widgets.pictograph.pictograph import Pictograph
    from widgets.sequence_builder.sequence_builder import SequenceBuilder
from objects.motion.motion import Motion
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop


class AddToSequenceManager:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def create_new_beat(self, clicked_option: "Pictograph") -> "Beat":
        from widgets.sequence_widget.beat_frame.beat import Beat

        new_beat = Beat(clicked_option.main_widget)
        new_beat.setSceneRect(clicked_option.sceneRect())
        # pictograph_dict = clicked_option.get.pictograph_dict()
        # new_beat.updater.update_pictograph(pictograph_dict)
        self.sequence_builder.current_pictograph = new_beat
        return new_beat
