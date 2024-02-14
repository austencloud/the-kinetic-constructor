from typing import TYPE_CHECKING
from constants import BLUE, RED

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
        pictograph.red_prop = pictograph.props[RED]
        pictograph.blue_prop = pictograph.props[BLUE]
        pictograph.updater.update_pictograph()
