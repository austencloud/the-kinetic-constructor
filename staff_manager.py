from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtSvg import QGraphicsSvgItem
from arrow import Arrow
from constants import STAFF_WIDTH, STAFF_LENGTH, RED, BLUE
from staff import Graphboard_Staff, PropBox_Staff, Staff, Beta_Staff

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
        GRAPHBOARD_WIDTH = self.graphboard_view.get_width()
        self.GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (self.graphboard_view.height() - self.graphboard_view.width()) / 2

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
            for color in ['red', 'blue']:
                staff_key = f"{direction}_staff_{color}"
                self.graphboard_staffs[staff_key] = Graphboard_Staff(
                    f"{direction}_staff",
                    self.graphboard_scene,
                    self.staff_locations[f"{direction}_staff"],
                    color,
                    f'images\\staves\\{direction}_staff_{color}.svg'
                )
                self.graphboard_staffs[staff_key].hide()

 
 
        # Initialize the beta staves     
        self.beta_staves = [
            Beta_Staff('beta_vertical_w-blue_e-red', graphboard_scene, self.staff_locations['N_staff'], None, 'images/staves/beta/beta_vertical_w-blue_e-red.svg'),
            Beta_Staff('beta_vertical_w-red_e-blue', graphboard_scene, self.staff_locations['E_staff'], None, 'images/staves/beta/beta_vertical_w-red_e-blue.svg'),
            Beta_Staff('beta_horizontal_n-red_s_blue', graphboard_scene, self.staff_locations['S_staff'], None, 'images/staves/beta/beta_horizontal_n-red_s_blue.svg'),
            Beta_Staff('beta_horizontal_n-blue_s-red', graphboard_scene, self.staff_locations['W_staff'], None, 'images/staves/beta/beta_horizontal_n-blue_s-red.svg')
        ]


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

    def connect_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view

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

    def update_staffs(self, arrows = []):
        print("=== Entering update_staffs ===")
        print("Arrows: " + str(arrows))
            
        # Get the staff locations
        staff_positions = [arrow.end_location.upper() + '_staff_' + arrow.color for arrow in arrows]
        
        for element_id, staff in self.graphboard_staffs.items():
            if element_id in staff_positions:
                staff.show()
                print(f"Showing staff {element_id}")
            else:
                staff.hide()
                    
                
        self.update_graphboard_staffs(self.graphboard_scene)
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]
        self.remove_and_replace_staves(staff_positions)
        self.track_visible_staves()  # Track the number of visible staves here
        print("=== Exiting update_staffs ===")

    def update_graphboard_staffs(self, scene):
        print("=== Entering update_graphboard_staffs ===")
        self.hide_all_staffs()
        new_staff_keys = set()

        for arrow in scene.items():
            if not isinstance(arrow, Arrow):
                continue

            end_location = arrow.end_location.capitalize()
            color = arrow.color.lower() if arrow.color in ['#ed1c24', 'red', '#2e3192', 'blue'] else None

            if color is None:
                print(f"Unexpected arrow color: {arrow.color}")
                continue

            staff_key = f"{end_location}_staff_{color}"
            new_staff_keys.add(staff_key)

            print(f"Staff key: {staff_key}")  # Debug

            staff = self.graphboard_staffs.get(staff_key)
            print(staff)
            staff.show()
            #set the staff coordinates
            staff.setPos(self.staff_locations[end_location + "_staff"])
            
                
        print("=== Exiting update_graphboard_staffs ===")

    def hide_all_staffs(self):
        print("=== Entering hide_all_staffs ===")
        for staff in self.graphboard_staffs.values():
            if staff.scene == self.graphboard_scene:
                staff.hide()
        # First remove all beta staves from the scene
        for beta_staff in self.beta_staves:
            if beta_staff.scene is not None:
                beta_staff.hide()
        self.beta_staves = []
        print("=== Exiting hide_all_staffs ===")    

    def show_staff(self, end_location):
        end_location = end_location.capitalize()
        staff = self.graphboard_staffs.get(end_location)
        if staff:
            staff.show()
        else:
            print(f"No staff found for end_location {end_location}")

    def hide_staff(self, end_location):
        print(f"=== Hiding Staff: {self.element_id} ===")
        end_location = end_location.capitalize()
        staff = self.graphboard_staffs.get(end_location)
        if staff:
            staff.hide()
        else:
            print(f"No staff found for end_location {end_location}")

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

    def track_visible_staves(self):
        visible_count = 0
        for staff in self.graphboard_staffs.values():
            if staff.isVisible():
                visible_count += 1
        print(f"Number of visible staves on the graphboard: {visible_count}")
