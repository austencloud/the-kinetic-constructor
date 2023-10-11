#import the modules i need
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

def init_layouts(main_window):
    main_window.main_layout = QHBoxLayout()
    main_window.right_layout = QVBoxLayout()  # Change this to QHBoxLayout
    main_window.upper_layout = QHBoxLayout()  # This will contain graphboard and buttons
    main_window.lower_layout = QVBoxLayout()  # Sequence
    main_window.top_of_lower_layout = QHBoxLayout()
    main_window.objectbox_layout = QVBoxLayout()
    main_window.graphboard_layout = QVBoxLayout()
    main_window.button_layout = QHBoxLayout()  # Change this to QHBoxLayout
    main_window.info_layout = QVBoxLayout()
    main_window.word_label_layout = QHBoxLayout()
    main_window.upper_graphboard_with_panel_layout = QVBoxLayout()
    
    main_window.upper_graphboard_with_panel_layout.addLayout(main_window.graphboard_layout)
    main_window.upper_graphboard_with_panel_layout.addLayout(main_window.button_layout)  # Add button_layout after graphboard_layout
    main_window.upper_layout.addLayout(main_window.objectbox_layout)
    main_window.upper_layout.addLayout(main_window.upper_graphboard_with_panel_layout)
    main_window.top_of_lower_layout.addLayout(main_window.word_label_layout)
    main_window.lower_layout.addLayout(main_window.top_of_lower_layout)
    main_window.right_layout.addLayout(main_window.upper_layout)
    main_window.upper_layout.addLayout(main_window.info_layout)
    main_window.right_layout.addLayout(main_window.lower_layout)  # Add info_layout to right_layout
    main_window.main_layout.addLayout(main_window.right_layout)

    main_window.upper_layout.addStretch()
    main_window.objectbox_layout.addStretch()
    main_window.objectbox_layout.addStretch()
    main_window.setLayout(main_window.main_layout)