from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsScene
from data.prop_class_mapping import prop_class_mapping

from constants import *
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.prop_types import PropTypes

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
        for motion in self.pictograph.motions.values():
            new_beat.motions[motion.color] = Motion(
                new_beat, motion.attr_manager.get_attributes()
            )

            new_arrow = Arrow(
                new_beat,
                motion.arrow.attr_manager.get_arrow_attributes(),
            )

            new_prop = self._create_prop(motion.color, motion.prop.prop_type)

            new_beat.arrows[new_arrow.color] = new_arrow
            new_beat.props[new_prop.color] = new_prop

            new_beat.motions[motion.color].arrow = new_arrow
            new_beat.motions[motion.color].prop = new_prop

            new_beat.arrows[motion.color] = new_arrow
            new_beat.props[motion.color] = new_prop

            if new_arrow.loc:
                new_arrow.updater.update_arrow()

            if new_prop.loc:
                new_prop.updater.update_prop()

            new_arrow.motion = new_beat.motions[motion.color]
            new_prop.motion = new_beat.motions[motion.color]

            motion_dict = self.pictograph.motions[
                motion.color
            ].attr_manager.get_attributes()
            motion_dict[ARROW] = new_arrow
            motion_dict[PROP] = new_prop
            motion_dict[MOTION_TYPE] = new_arrow.motion.motion_type
            new_arrow.motion.turns = motion_dict[TURNS]
            new_arrow.motion.updater.update_motion(motion_dict)

            new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())

            new_arrow.updater.update_arrow()
        new_beat.updater.update_pictograph()

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