#import 
import os
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from settings import *
from objects.arrow import Arrow
from views.arrowbox_view import ArrowBox_View

class Init_ArrowBox:
    def __init__(self, main_widget, main_window):
        self.main_widget = main_widget
        self.main_window = main_window
        self.arrowbox_scene = QGraphicsScene()
        self.init_arrowbox_view()
        self.configure_arrowbox_frame()
        self.populate_arrows()
        self.finalize_arrowbox_configuration()

    def init_arrowbox_view(self):
        self.arrowbox_view = ArrowBox_View(self.arrowbox_scene, self.main_widget.graphboard_view, self.main_widget.info_tracker, self.main_widget.svg_manager)

    def configure_arrowbox_frame(self):
        self.arrowbox_frame = QFrame(self.main_window)
        self.objectbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.objectbox_layout)

    def populate_arrows(self):
        svgs_full_paths = []
        default_arrows = ['red_pro_r_ne_0.svg', 'red_anti_r_ne_0.svg', 'blue_pro_r_sw_0.svg', 'blue_anti_r_sw_0.svg']

        for dirpath, dirnames, filenames in os.walk(ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for svg_file in svgs_full_paths:
            self.create_and_configure_arrow(svg_file, default_arrows)

    def create_and_configure_arrow(self, svg_file, default_arrows):
        file_name = os.path.basename(svg_file)
        
        svg_item_count_red_pro = 0
        svg_item_count_red_anti = 0
        svg_item_count_blue_pro = 0
        svg_item_count_blue_anti = 0
        spacing = 200 * GRAPHBOARD_SCALE
        y_pos_red = 0
        y_pos_blue = 200 * GRAPHBOARD_SCALE
        
        if file_name in default_arrows:
            
            motion_type = file_name.split('_')[1]
            arrow_item = Arrow(svg_file, self.main_widget.graphboard_view, self.main_widget.info_tracker, self.main_widget.svg_manager, self.main_widget.arrow_manager, motion_type, self.main_widget.staff_manager, None)
            arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            arrow_item.setScale(GRAPHBOARD_SCALE * 0.75)

            if 'red' in file_name:
                if 'pro' in file_name:
                    arrow_item.setPos(svg_item_count_red_pro * spacing, y_pos_red) # Red pro
                    svg_item_count_red_pro += 1
                elif 'anti' in file_name:
                    arrow_item.setPos((svg_item_count_red_anti + 1) * spacing, y_pos_red) # Red Anti
                    svg_item_count_red_anti += 1
            elif 'blue' in file_name:
                if 'pro' in file_name:
                    arrow_item.setPos(svg_item_count_blue_pro * spacing, y_pos_blue) # Blue pro
                    svg_item_count_blue_pro += 1
                elif 'anti' in file_name:
                    arrow_item.setPos((svg_item_count_blue_anti + 1) * spacing, y_pos_blue) # Blue Anti
                    svg_item_count_blue_anti += 1
            self.arrowbox_scene.addItem(arrow_item) 
            self.main_widget.arrows.append(arrow_item)

    def finalize_arrowbox_configuration(self):
        self.objectbox_layout.addWidget(self.arrowbox_view)
        self.arrowbox_frame.setFixedSize(int(500 * GRAPHBOARD_SCALE), int(600 * GRAPHBOARD_SCALE))
        self.arrowbox_view.arrowbox_frame = self.arrowbox_frame
        self.main_widget.arrowbox_view = self.arrowbox_view
