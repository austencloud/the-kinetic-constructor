from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsScene
from data.prop_class_mapping import prop_class_mapping

from constants import *
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.prop_types import PropTypes
from widgets.factories.prop_factory import PropFactory

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
from objects.motion.motion import Motion
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop


class AddToSequenceManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        
    def add_to_sequence_callback(self) -> None:
        new_beat = self.create_new_beat()
        self.pictograph.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(
            new_beat
        )

    def create_new_beat(self) -> QGraphicsScene:
        from widgets.pictograph.pictograph import Pictograph

        new_beat = Pictograph(self.pictograph.main_widget)
        new_beat.setSceneRect(self.pictograph.sceneRect())

        pictograph_dict = {
            LETTER: self.pictograph.letter,
            RED_START_ORI: self.pictograph.motions[RED].end_ori,
            BLUE_START_ORI: self.pictograph.motions[BLUE].end_ori,
            RED_TURNS: 0,
            BLUE_TURNS: 0,
        }
        new_beat.updater.update_pictograph(pictograph_dict)

        return new_beat

    def _create_prop(self, color: Colors, prop_type: PropTypes) -> Prop:
        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")
        prop_attributes = {
            COLOR: color,
            PROP_TYPE: prop_type,
            LOC: None,
            ORI: None,
        }
        prop: Prop = prop_class(self.pictograph, prop_attributes, None)
        self.pictograph.motions[color].prop = prop
        prop.motion = self.pictograph.motions[color]
        self.pictograph.addItem(prop)
        prop.hide()
        return prop
