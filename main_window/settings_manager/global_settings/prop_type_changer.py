from typing import TYPE_CHECKING
from data.constants import BLUE, RED
from widgets.base_widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from ..settings_manager import SettingsManager


class PropTypeChanger:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.main_window = settings_manager.main_window

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
        pictograph.red_prop = pictograph.props[RED]
        pictograph.blue_prop = pictograph.props[BLUE]
        pictograph.updater.update_pictograph()

    def apply_prop_type(self) -> None:
        prop_type = self.main_window.settings_manager.global_settings.get_prop_type()
        self.main_window.main_widget.prop_type = prop_type
        self.update_props_to_type(prop_type)

    def update_props_to_type(self, new_prop_type) -> None:
        for pictograph_list in self.main_window.main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if pictograph.view.isVisible():
                    self.replace_props(new_prop_type, pictograph)
                    pictograph.prop_type = new_prop_type

        for (
            beat_view
        ) in (
            self.main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beats
        ):
            if beat_view.is_filled:
                self.replace_props(new_prop_type, beat_view.beat)
                beat_view.beat.updater.update_pictograph()
                beat_view.beat.prop_type = new_prop_type

        start_pos_view = (
            self.main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.start_pos_view
        )
        if hasattr(start_pos_view, "start_pos"):
            start_pos = start_pos_view.start_pos
            if start_pos.view.is_filled:
                self.replace_props(new_prop_type, start_pos)

        json_manager = self.main_window.main_widget.json_manager
        json_manager.updater.update_prop_type_in_json(new_prop_type)
