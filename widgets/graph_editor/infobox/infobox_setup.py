# import the missing modules
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers
from widgets.graph_editor.infobox.infobox_button_manager import InfoboxButtonManager
import logging
from resources.constants import GRAPHBOARD_SCALE

class InfoboxSetup:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.helpers = infobox_manager.helpers
        self.updater = infobox_manager.updater

    def initialize(self):
        self.setup_dimensions()
        self.setup_labels()
        self.setup_layouts()
        self.setup_widgets()
        self.setup_buttons()

    def setup_dimensions(self):
        self.infobox.set_dimensions()

    def setup_labels(self):
        self.infobox.setup_labels()

    def setup_layouts(self):
        self.infobox.setup_layouts()

    def setup_widgets(self):
        # Pre-create widgets
        self.blue_info_widget = self.helpers.construct_info_string_label({})
        self.red_info_widget = self.helpers.construct_info_string_label({})

        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()

        self.blue_info_layout.addWidget(self.infobox.blue_details_label)
        self.red_info_layout.addWidget(self.infobox.red_details_label)

        self.blue_info_layout.addWidget(self.blue_info_widget)
        self.red_info_layout.addWidget(self.red_info_widget)

        self.infobox.content_layout.addLayout(self.blue_info_layout)
        self.infobox.content_layout.addLayout(self.red_info_layout)

        self.blue_info_widget.setVisible(False)
        self.red_info_widget.setVisible(False)

    def setup_buttons(self):
        self.infobox_manager.button_manager.setup_buttons()

    def setup_ui_elements(self):
        self.button_manager = InfoboxButtonManager(
            self, self.updater.arrow_manipulator, self.infobox.graphboard_view
        )
        self.helpers = InfoboxHelpers()
        self.setup_labels()
        self.setup_layouts()
        self.infobox.setLayout(self.infobox.grid_layout)
        self.infobox.set_dimensions()
        self.button_manager.setup_buttons()
        logging.debug("InfoFrame setup_ui_elements")

        # Pre-create widgets
        self.blue_info_widget = self.helpers.construct_info_string_label({})
        self.red_info_widget = self.helpers.construct_info_string_label({})

        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()

        self.blue_info_layout.addWidget(self.blue_details_label)
        self.red_info_layout.addWidget(self.red_details_label)

        self.blue_info_layout.addWidget(self.blue_info_widget)
        self.red_info_layout.addWidget(self.red_info_widget)

        self.content_layout.addLayout(self.blue_info_layout)
        self.content_layout.addLayout(self.red_info_layout)

        self.blue_info_widget.setVisible(False)
        self.red_info_widget.setVisible(False)

    def setup_labels(self):
        self.blue_details_label = self.helpers.create_label("Left", "blue")
        self.red_details_label = self.helpers.create_label("Right", "red")
        self.type_position_label = self.helpers.create_label()
        
    def setup_layouts(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(10)

        header_layout = self.helpers.create_horizontal_layout(
            [self.blue_details_label, self.red_details_label]
        )
        self.content_layout = self.helpers.create_horizontal_layout()
        type_position_layout = self.helpers.create_horizontal_layout(
            [self.type_position_label]
        )

        self.helpers.add_widgets_to_grid(
            self.grid_layout, [header_layout, self.content_layout, type_position_layout]
        )
        
    def set_dimensions(self):
        self.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.setFixedHeight(int(900 * GRAPHBOARD_SCALE))

