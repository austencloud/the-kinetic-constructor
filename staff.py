from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from arrow import Arrow
from settings import Settings
from constants import STAFF_WIDTH, STAFF_LENGTH, RED, BLUE

SCALE_FACTOR = Settings.SCALE_FACTOR

class Staff(QGraphicsSvgItem):

    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None, initial_visibility=True):
        super().__init__()
        self.element_id = element_id
        self.position = position 
        self.renderer = QSvgRenderer(staff_svg_file)
        self.setSharedRenderer(self.renderer)
        self.setElementId(self.element_id)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        scene.addItem(self)
        self.setVisible(initial_visibility)
        self.type = "staff"
        self.scene = scene
        self.setPos(position)
        self.arrow = None
        self.setVisible(True)
        rect = self.boundingRect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.setPos(position)
        self.svg_file = staff_svg_file
        self.color = color

        self.is_static = False
        
    def update_attributes(self, new_attributes):
        self.element_id = new_attributes.get('element_id', self.element_id)
        self.position = new_attributes.get('position', self.position)
        self.svg_file = new_attributes.get('svg_file', self.svg_file)
        self.color = new_attributes.get('color', self.color)

    def update_staff(self):
        self.setElementId(self.element_id)
        self.setPos(self.position)
        self.renderer.load(self.svg_file)
        self.setSharedRenderer(self.renderer)

    def set_static(self, is_static):
        self.is_static = is_static


    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def set_arrow(self, arrow):
        self.arrow = arrow
        
    def isVisible(self):
        return super().isVisible()

class Graphboard_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)

class Beta_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)

class PropBox_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file)
        
class Staff_Manager(QObject):
    positionChanged = pyqtSignal(str)

    def __init__(self, graphboard_scene):
        super().__init__()
        self.graphboard_scene = graphboard_scene
        self.beta_staves = []
        self.previous_position = None



    ### INITIALIZERS ###

    def init_graphboard_staffs(self, graphboard_scene):
        
        # Determine the handpoints of the grid
        scale = self.grid.scale()
        GRID_WIDTH = self.grid.get_width()
        GRAPHBOARD_WIDTH = self.graphboard.get_width()
        self.GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (self.graphboard.height() - self.graphboard.width()) / 2

        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + self.GRID_PADDING
            scaled_y = y * scale + self.GRID_V_OFFSET
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)


        # Set the locations of the staffs according to the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH)
        }

        # Initialize the graphboard staffs
        self.graphboard_staffs = {}
        for direction in ['N', 'E', 'S', 'W']:
            for color in [RED, BLUE]:
                if color == RED:
                    color = 'red'
                else: # color == BLUE
                    color = 'blue'
                staff_key = f"{direction}_staff_{color}"
                svg_file = f'images\\\\staves\\\\{direction}_staff_{color}.svg'
                self.graphboard_staffs[staff_key] = Graphboard_Staff(
                    f'{direction}_staff', graphboard_scene, self.staff_locations[f'{direction}_staff'], color, svg_file
                )
             
             
        # Initialize the beta staves     
        self.beta_staves = [
            Beta_Staff('beta_vertical_w-blue_e-red', graphboard_scene, self.staff_locations['N_staff'], None, 'images/staves/beta/beta_vertical_w-blue_e-red.svg'),
            Beta_Staff('beta_vertical_w-red_e-blue', graphboard_scene, self.staff_locations['E_staff'], None, 'images/staves/beta/beta_vertical_w-red_e-blue.svg'),
            Beta_Staff('beta_horizontal_n-red_s_blue', graphboard_scene, self.staff_locations['S_staff'], None, 'images/staves/beta/beta_horizontal_n-red_s_blue.svg'),
            Beta_Staff('beta_horizontal_n-blue_s-red', graphboard_scene, self.staff_locations['W_staff'], None, 'images/staves/beta/beta_horizontal_n-blue_s-red.svg')
        ]

        self.hide_all_graphboard_staffs()

    def init_propbox_staffs(self, propbox_scene):
        self.propbox_staff_locations = {
            'N_staff': QPointF(100, 100),
            'E_staff': QPointF(100, 100),
            'S_staff': QPointF(100, 100),
            'W_staff': QPointF(100, 100)
        }
        
        self.propbox_staffs = {}
        self.red_staff = PropBox_Staff('red_staff', propbox_scene, self.propbox_staff_locations['N_staff'], 'red', 'images\\staves\\N_staff_red.svg')
        self.blue_staff = PropBox_Staff('blue_staff', propbox_scene, self.propbox_staff_locations['N_staff'], 'blue', 'images\\staves\\N_staff_blue.svg')
        self.propbox_staffs['red_staff'] = self.red_staff
        self.propbox_staffs['blue_staff'] = self.blue_staff




    ### CONNECTORS ###

    def connect_grid(self, grid):
        self.grid = grid

    def connect_graphboard(self, graphboard):
        self.graphboard = graphboard

    def connect_propbox(self, propbox):
        self.propbox = propbox

    ### GETTERES ###

    def get_staff_position(self, staff_item):
        print(f"Getting position for staff {staff_item.element_id}")
        # Iterate over all the staffs in the graphboard_staffs dictionary
        for staff_name, graphboard_staff in self.graphboard_staffs.items():
            # If the current graphboard_staff is the same as the input staff_item
            if graphboard_staff is staff_item:
                # Return the position of the staff
                print(f"Found staff {staff_item.element_id} at position {self.staff_locations[staff_name.split('_')[0] + '_staff']}")
                return self.staff_locations[staff_name.split('_')[0] + '_' + staff_name.split('_')[1]]
        
        # If the input staff_item is not found in the graphboard_staffs dictionary, return None
        return None

    def find_staff_by_position(self, position):
        for staff in self.graphboard_staffs.values():
            if staff.position == position:
                return staff
        return None

    ### UPDATERS ###

    def update_staffs_and_check_beta(self):
        self.update_graphboard_staffs(self.graphboard.scene())
        self.check_and_replace_staves()

    def hide_all_graphboard_staffs(self):
        for staff in self.graphboard_staffs.values():
            # remove the staff from the scene
            if staff.scene is not None:
                self.graphboard_scene.removeItem(staff)

            
    def show_staff(self, direction):
        direction = direction.capitalize()
        staff = self.graphboard_staffs.get(direction)
        if staff:
            staff.show()
        else:
            print(f"No staff found for direction {direction}")

    def remove_non_beta_staves(self):
        for staff in self.graphboard_staffs.values():
            if staff.isVisible() and staff.scene is not None:

                staff.hide()  # Hide the staff

    def remove_and_replace_staves(self, staff_positions):
        position_to_direction = {
            (self.staff_locations['N_staff'].x(), self.staff_locations['N_staff'].y()): 'n',
            (self.staff_locations['E_staff'].x(), self.staff_locations['E_staff'].y()): 'e',
            (self.staff_locations['S_staff'].x(), self.staff_locations['S_staff'].y()): 's',
            (self.staff_locations['W_staff'].x(), self.staff_locations['W_staff'].y()): 'w',
        }

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:
                staves_to_remove = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]
                for staff in staves_to_remove:
                    ### not causing the error ### 
                    self.graphboard_scene.removeItem(staff)
                    staff.hide()
                    self.graphboard_scene.update()
                    # Remove the staff from the graphboard_staffs dictionary
                    self.graphboard_staffs = {key: value for key, value in self.graphboard_staffs.items() if value != staff}
                        
                staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

                try:
                    direction = position_to_direction[position]
                except Exception as e:
                    print(f"Error when getting direction: {e}")
                    continue

                arrows = [arrow for arrow in self.graphboard_scene.items() if isinstance(arrow, Arrow) and arrow.end_location == direction]

                if len(arrows) != 2:
                    continue 

                arrows.sort(key=lambda arrow: arrow.start_location)

                arrow1, arrow2 = arrows
                if arrow1.end_location == 'n' or arrow1.end_location == 's':
                    orientation = 'vertical'
                else:
                    orientation = 'horizontal'

                if arrow1.color == "#ed1c24" or arrow1.color == 'red':
                    color1 = 'red'
                else:
                    color1 = 'blue'

                if arrow2.color == "#ed1c24" or arrow2.color == 'red':
                    color2 = 'red'
                else:
                    color2 = 'blue'

                if orientation == 'vertical':
                    if color1 == 'red':
                        beta_svg_file = 'images/staves/beta/beta_vertical_w-blue_e-red.svg'
                    else:
                        beta_svg_file = 'images/staves/beta/beta_vertical_w-red_e-blue.svg'
                else:
                    if color1 == 'red':
                        beta_svg_file = 'images/staves/beta/beta_horizontal_n-red_s_blue.svg'
                    else:
                        beta_svg_file = 'images/staves/beta/beta_horizontal_n-blue_s-red.svg'

                beta_svg = QGraphicsSvgItem(beta_svg_file)
                self.graphboard_scene.addItem(beta_svg)

                if orientation == 'vertical':
                    adjusted_position = QPointF(position[0] - 20, position[1] - 0)
                else:  # orientation is horizontal
                    adjusted_position = QPointF(position[0] - 0, position[1] - 20)

                beta_svg.setPos(self.staff_locations[direction.capitalize() + "_staff"])
                beta_svg.setPos(adjusted_position)

                self.beta_staves.append(beta_svg)
            
            else:
                continue

    def update_graphboard_staffs(self, scene):
        
        # First remove all beta staves from the scene
        for beta_staff in self.beta_staves:
            if beta_staff.scene is not None:
                self.graphboard_scene.removeItem(beta_staff)
        self.beta_staves = []
        
        # Then remove all graphboard staves from the scene
        self.hide_all_graphboard_staffs()
        
        # Then add the graphboard staves back to the scene
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                end_location = arrow.end_location
                end_location = end_location.capitalize()
                if arrow.color == "#ed1c24" or arrow.color == 'red':
                    color = 'red'
                elif arrow.color == "#2e3192" or arrow.color == 'blue':
                    color = 'blue'
                else:
                    print(f"Unexpected arrow color: {arrow.color}")
                    continue 
                
                new_staff = Graphboard_Staff(end_location + "_staff", scene, self.staff_locations[end_location + "_staff"], color, 'images\\staves\\' + end_location + "_staff_" + color + '.svg')
                if new_staff.scene is None:
                    self.scene.addItem(new_staff)
                self.graphboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary

    def check_and_replace_staves(self):
        staff_positions = self.identify_staff_positions()
        self.remove_and_replace_staves(staff_positions)

    def identify_staff_positions(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]
        return staff_positions
