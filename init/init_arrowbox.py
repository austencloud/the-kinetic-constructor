#import 
import os
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QFrame, QGridLayout
from settings import *
from objects.arrow import Arrow
from views.arrowbox_view import ArrowBox_View

class Init_ArrowBox: 
    def __init__(self, ui_setup, main_window):
        self.init_arrowbox_view(ui_setup, main_window)
    
    def init_arrowbox_view(self, ui_setup, main_window):
        arrowbox_scene = QGraphicsScene()
        arrowbox_view = ArrowBox_View(arrowbox_scene, ui_setup.graphboard_view, ui_setup.info_tracker, ui_setup.svg_manager)
        arrowbox_frame = QFrame(main_window)
        objectbox_layout = QGridLayout()
        arrowbox_frame.setLayout(objectbox_layout) 


        svgs_full_paths = []
        default_arrows = ['red_pro_r_ne_0.svg', 'red_anti_r_ne_0.svg', 'blue_pro_r_sw_0.svg', 'blue_anti_r_sw_0.svg']
        svg_item_count = 0

        for dirpath, dirnames, filenames in os.walk(ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        svg_item_count_red_pro = 0
        svg_item_count_red_anti = 0
        svg_item_count_blue_pro = 0
        svg_item_count_blue_anti = 0
        spacing = 200 * GRAPHBOARD_SCALE
        y_pos_red = 0
        y_pos_blue = 200 * GRAPHBOARD_SCALE

        for i, svg_file in enumerate(svgs_full_paths):
            file_name = os.path.basename(svg_file)
            if file_name in default_arrows:
                motion_type = file_name.split('_')[1]
                arrow_item = Arrow(svg_file, ui_setup.graphboard_view, ui_setup.info_tracker, ui_setup.svg_manager, ui_setup.arrow_manager, motion_type, ui_setup.staff_manager, None)
                arrow_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
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
                arrowbox_scene.addItem(arrow_item) 


        ui_setup.arrows.append(arrow_item)
        
        objectbox_layout.addWidget(arrowbox_view) 
        arrowbox_frame.setFixedSize(int(500 * GRAPHBOARD_SCALE), int(600 * GRAPHBOARD_SCALE))
        main_window.objectbox_layout.addWidget(arrowbox_frame)