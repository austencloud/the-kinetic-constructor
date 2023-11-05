from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFrame

class InfoboxWidgets():
    def __init__(self, infobox, info_manager):
        self.infobox = infobox
        self.info_manager = info_manager
        self.labels = info_manager.labels
        
    def setup_widgets(self):
        self.blue_attributes_widget = QFrame()
        self.blue_attributes_widget.setFrameShape(QFrame.Shape.Box)
        self.blue_attributes_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.red_attributes_widget = QFrame()
        self.red_attributes_widget.setFrameShape(QFrame.Shape.Box)
        self.red_attributes_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.blue_attributes_widget.setVisible(True)
        self.red_attributes_widget.setVisible(True)

    def construct_attributes_widget(self, attributes, color):
        (
            motion_type_label,
            rotation_direction_label,
            start_end_label,
            turns_label,
        ) = self.labels.create_labels_for_attributes(attributes)

        start_end_layout = QHBoxLayout()
        start_end_button = getattr(self.infobox, f"swap_start_end_{color}_button")
        start_end_layout.addWidget(start_end_button)
        start_end_layout.addWidget(start_end_label)

        turns_layout = QHBoxLayout()
        decrement_button = getattr(self.infobox, f"decrement_turns_{color}_button")
        increment_button = getattr(self.infobox, f"increment_turns_{color}_button")
        turns_layout.addWidget(decrement_button)
        turns_layout.addWidget(turns_label)
        turns_layout.addWidget(increment_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(motion_type_label)
        main_layout.addWidget(rotation_direction_label)
        main_layout.addWidget(start_end_label)
        main_layout.addLayout(turns_layout)  # Add the turns layout here

        info_widget = QWidget()
        info_widget.setLayout(main_layout)
        return info_widget
    
    def update_info_widget_content(self, widget, attributes):
        self.buttons = self.info_manager.buttons
        if widget.layout().count() == 0:
            new_content = self.labels.construct_info_string_label(attributes)
            widget.setLayout(new_content.layout())
            return
        self.labels.update_labels(widget, attributes)
        self.buttons.update_buttons(attributes)
