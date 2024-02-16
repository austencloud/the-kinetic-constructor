from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from main import MainWindow


class PropTypeChanger:
    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window

    def replace_props(self, new_prop_type, pictograph: Pictograph):
        for color, prop in pictograph.props.items():
            new_prop = pictograph.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type
            )
            pictograph.props[color].deleteLater()
            pictograph.props[color].hide()
            pictograph.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.motions[color].prop = pictograph.props[color]
            pictograph.props[color].motion.attr_manager.update_prop_ori()
            pictograph.props[color].updater.update_prop()
        pictograph.red_prop = pictograph.props[Color.RED]
        pictograph.blue_prop = pictograph.props[Color.BLUE]
        pictograph.updater.update_pictograph()

    def apply_prop_type(self) -> None:
        prop_type = self.main_window.settings_manager.get_prop_type()
        self.main_window.main_widget.prop_type = prop_type
        self.update_props_to_type(prop_type)

    def update_props_to_type(self, new_prop_type) -> None:
        for pictograph_list in self.main_window.main_widget.all_pictographs.values():
            for pictograph in pictograph_list.values():
                if pictograph.view.isVisible():
                    self.replace_props(new_prop_type, pictograph)

        for beat_view in self.main_window.main_widget.sequence_widget.beats:
            if beat_view.is_filled:
                self.replace_props(new_prop_type, beat_view.beat)
                beat_view.beat.updater.update_pictograph()

        start_pos = (
            self.main_window.main_widget.sequence_widget.beat_frame.start_pos_view.start_pos
        )
        if start_pos.view.is_filled:
            self.replace_props(new_prop_type, start_pos)
