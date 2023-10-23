from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtCore import QPointF
import random
import os
from objects.arrow import Arrow
from managers.export_manager import ExportManager
from managers.staff_managers.pictograph_staff_manager import PictographStaffManager
class Pictograph_Generator():
    def __init__(self, main_widget, graphboard_view, info_frame):
        self.staff_manager = graphboard_view.staff_manager
        self.graphboard_view = graphboard_view
        self.info_frame = info_frame
        self.main_window = main_widget.main_window
        self.arrow_manager = main_widget.arrow_manager
        self.export_manager = main_widget.export_manager
        self.svg_manager = main_widget.svg_manager
        self.grid = main_widget.grid
        self.graphboard_scene = self.graphboard_view.scene()
        self.output_dir = "images/pictographs"
        self.current_letter = None
        self.letters = main_widget.letters

    def generate_all_pictographs(self, staff_manager):
        os.makedirs(self.output_dir, exist_ok=True)

        for letter, combinations in self.letters.items():
            for combination in combinations:
                positions_dict = next((d for d in combination if 'start_position' in d and 'end_position' in d), None)
                if positions_dict is None:
                    continue

                start_position = positions_dict['start_position'].replace('alpha', 'a').replace('beta', 'b').replace('gamma', 'g')
                end_position = positions_dict['end_position'].replace('alpha', 'a').replace('beta', 'b').replace('gamma', 'g')

                motion_types = [arrow_dict['motion_type'] for arrow_dict in combination if 'motion_type' in arrow_dict]
                is_hybrid = motion_types.count('anti') == 1 and motion_types.count('pro') == 1


                for arrow_dict in combination:
                    print("iterating over arrow_dict in combination")
                    if all(key in arrow_dict for key in ['color', 'motion_type', 'rotation_direction', 'quadrant']):
                        color = arrow_dict['color']
                        motion_type = arrow_dict['motion_type']

                        file_name = f"{letter}_{start_position}_{end_position}"
                        if motion_type == 'pro' and is_hybrid and color == 'red':
                            file_name += f"_r-pro_l-anti"
                        elif motion_type == 'anti' and is_hybrid and color == 'red':
                            file_name += f"_r-anti_l-pro"
                        file_name += ".svg"

                        output_file_path = os.path.join(self.output_dir, file_name)
                        self.export_manager = ExportManager(self.graphboard_view, self.graphboard_scene, self.staff_manager, self.grid)
                        print(output_file_path)
                        self.export_manager.export_to_svg(output_file_path)

                
                # Clear the graphboard for the next combination
                self.graphboard_view.clear()

    def open_selection_window(self, letter):
        self.output_dir = "images/pictographs"
        self.graphboard_view.clear()
        
        combinations = self.letters.get(letter, [])
        if not combinations:
            print(f"No combinations found for letter {letter}")
            self.graphboard_view.update_letter(None)
            self.info_frame.update()
            return
        self.current_letter = letter
        print(f"Generating {self.current_letter}")
        self.graphboard_view.update_letter(self.current_letter)
        
        combination_set = random.choice(combinations)
        created_arrows = []
        
        optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
        for combination in combination_set:
            if all(key in combination for key in ['color', 'motion_type', 'rotation_direction', 'quadrant', 'turns']):
                if combination['motion_type'] == 'static':
                    svg_file = f"images/arrows/blank.svg"
                    arrow = Arrow(svg_file, self.graphboard_view, self.info_frame, self.svg_manager, self.arrow_manager, combination['motion_type'], self.staff_manager)
                elif combination['motion_type'] == 'anti' or combination['motion_type'] == 'pro':
                    svg_file = f"images/arrows/shift/{combination['motion_type']}/{combination['color']}_{combination['motion_type']}_{combination['rotation_direction']}_{combination['quadrant']}_{combination['turns']}.svg"
                    arrow = Arrow(svg_file, self.graphboard_view, self.info_frame, self.svg_manager, self.arrow_manager, combination['motion_type'], self.staff_manager, None)
                    arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                    arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)
                created_arrows.append(arrow)

        
        # Add the arrows to the scene
        for arrow in created_arrows:
            if arrow.scene is not self.graphboard_scene:
                self.graphboard_scene.addItem(arrow)
            
        for arrow in created_arrows:
            if optimal_positions:
                optimal_position = optimal_positions.get(f"optimal_{arrow.color}_location")
                if optimal_position:
                    # Calculate the position to center the arrow at the optimal position
                    pos = QPointF(optimal_position['x'], optimal_position['y']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
                else:
                    if arrow.quadrant != "None":
                        pos = self.graphboard_view.get_quadrant_center(arrow.quadrant) - arrow.boundingRect().center()
            else:
                # Calculate the position to center the arrow at the quadrant center
                pos = self.graphboard_view.get_quadrant_center(arrow.quadrant) - arrow.boundingRect().center()
                arrow.setPos(pos)

        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        # created_arrows should be a list
        self.info_frame.update()

    def get_current_letter(self):
        return self.current_letter

    def update_staff(self, arrow, staff_manager):
        arrows = [arrow] if not isinstance(arrow, list) else arrow

        staff_positions = [arrow.end_location.upper() + '_staff_' + arrow.color for arrow in arrows]

        for element_id, staff in staff_manager.graphboard_staffs.items():
            if element_id in staff_positions:
                staff.show()
            else:
                staff.hide()

        self.staff_manager.check_replace_beta_staffs()
