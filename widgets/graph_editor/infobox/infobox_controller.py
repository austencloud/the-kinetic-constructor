class InfoboxController:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.graphboard_view = infobox.graphboard_view
        self.infobox_manager = infobox_manager
        self.updater = infobox_manager.updater
        self.button_factory = infobox_manager.button_factory
        self.arrow_manipulator = self.infobox.graphboard_view.arrow_manager.manipulator
        self.setup_buttons()

    def setup_buttons(self):
        button_properties = {
            "swap_colors": {
                "icon": None,
                "text": "↔",
                "callback": self.arrow_manipulator.swap_colors,
            },
            "swap_motion_type_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_motion_type_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "swap_start_end_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_start_end_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "decrement_turns_blue": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "decrement_turns_red": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "increment_turns_blue": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "increment_turns_red": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
        }

        for button_name, properties in button_properties.items():
            self.button_factory.create_and_set_button(button_name, properties)
            button = getattr(self.infobox, f"{button_name}_button")
            button.setVisible(False)  # Set initial visibility to False
