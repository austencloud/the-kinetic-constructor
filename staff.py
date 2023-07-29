from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from arrow import Arrow

class Staff:
    CYMK_BLUE = '#2e3192'
    CYMK_RED = '#ed1c24'


    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        self.element_id = element_id
        self.position = position 
        self.renderer = QSvgRenderer(staff_svg_file)
        self.item = QGraphicsSvgItem()
        self.item.setSharedRenderer(self.renderer)
        self.item.setElementId(self.element_id)
        self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
        scene.addItem(self.item)

        self.scene = scene
        print("Staff position: ", position)
        self.item.setPos(position)
        self.arrow = None
        self.item.setVisible(True)
        rect = self.item.boundingRect()
        self.item.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.item.setPos(position)

        self.svg_file = staff_svg_file

    def show(self):
        self.item.setVisible(True)
        if self.item.scene() is None:
            self.scene.addItem(self.item)


    def hide(self):
        self.item.setVisible(False)
        if self.item.scene() is not None:
            self.scene.removeItem(self.item)

    def set_arrow(self, arrow):
        self.arrow = arrow

        
    def isVisible(self):
        return self.item.isVisible()

class StaffManager(QObject):
    GRID_OFFSET = 25
    positionChanged = pyqtSignal(str)

    def __init__(self, scene):
        super().__init__()  # Initialize the QObject
        self.scene = scene
        self.beta_staves = []
        self.previous_position = None

        hand_points = {
            'N_hand_point': QPointF(325, 181.9),
            'E_hand_point': QPointF(468.1, 325.),
            'S_hand_point': QPointF(325, 468.1),
            'W_hand_point': QPointF(181.9, 325),
        }

        self.staff_locations = {
            'N_staff': QPointF(hand_points['N_hand_point'].x() + self.GRID_OFFSET + 12.5, hand_points['N_hand_point'].y() + self.GRID_OFFSET - 100),
            'E_staff': QPointF(hand_points['E_hand_point'].x() + self.GRID_OFFSET - 100, hand_points['E_hand_point'].y() + self.GRID_OFFSET + 12.5),
            'S_staff': QPointF(hand_points['S_hand_point'].x() + self.GRID_OFFSET + 12.5, hand_points['S_hand_point'].y() + self.GRID_OFFSET - 100),
            'W_staff': QPointF(hand_points['W_hand_point'].x() + self.GRID_OFFSET - 100, hand_points['W_hand_point'].y() + self.GRID_OFFSET + 12.5),
        }

        # Initialize the staffs attribute
        self.staffs = {
            'N_staff_red': Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_red.svg'),
            'E_staff_red': Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_red.svg'),
            'S_staff_red': Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_red.svg'),
            'W_staff_red': Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_red.svg'),
            'N_staff_blue': Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_blue.svg'),
            'E_staff_blue': Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_blue.svg'),
            'S_staff_blue': Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_blue.svg'),
            'W_staff_blue': Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_blue.svg')
        }

        self.hide_all()


    # write a function to show all the staves
    def show_all(self):
        for staff in self.staffs.values():
            staff.show()
    
    # write a function to hide all the staves
    def hide_all(self):
        for staff in self.staffs.values():
            staff.hide()

    def show_staff(self, direction):
        # capilatlize the first letter of the direction parameter
        direction = direction.capitalize()
        staff = self.staffs[direction]
        staff.show()
        if staff.item.scene() is None:  # If the staff is not in the scene
            self.scene.addItem(staff.item)  # Add it back to the scene

    def remove_beta_staves(self):
        for beta_staff in self.beta_staves:
            self.scene.removeItem(beta_staff)
        self.beta_staves = []

    def remove_non_beta_staves(self):
        for staff in self.staffs.values():
            if staff.isVisible():
                self.scene.removeItem(staff.item)

    def update_staffs(self, scene):

        self.hide_all()
        # Show the staffs that correspond to the current arrows
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                # Determine the end position of the arrow
                end_location = arrow.end_location

                if arrow.color == "#ed1c24" or arrow.color == 'red':
                    color = 'red'
                elif arrow.color == "#2e3192" or arrow.color == 'blue':
                    color = 'blue'
                else:
                    print(f"Unexpected arrow color: {arrow.color}")
                    continue  # Skip this arrow

                # Show the staff that corresponds to the arrow
                self.show_staff(end_location + "_staff_" + color)


    def check_and_replace_staves(self):

        # Map the positions of the staves to their corresponding cardinal direction
        position_to_direction = {
            (self.staff_locations['N_staff'].x(), self.staff_locations['N_staff'].y()): 'n',
            (self.staff_locations['E_staff'].x(), self.staff_locations['E_staff'].y()): 'e',
            (self.staff_locations['S_staff'].x(), self.staff_locations['S_staff'].y()): 's',
            (self.staff_locations['W_staff'].x(), self.staff_locations['W_staff'].y()): 'w',
        }

        # Get the positions of the staves
        staff_positions = [(staff.item.pos().x(), staff.item.pos().y()) for staff in self.staffs.values() if staff.isVisible()]

        # Check if there are two staves in the same compass location
        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:
                # Collect the staves to be removed
                staves_to_remove = [staff for staff in self.staffs.values() if (staff.item.pos().x(), staff.item.pos().y()) == position]
                # Remove the staves
                for staff in staves_to_remove:
                    self.scene.removeItem(staff.item)
                    staff.hide()
                    self.scene.update()
                    

                # Update the staff_positions list
                staff_positions = [(staff.item.pos().x(), staff.item.pos().y()) for staff in self.staffs.values() if staff.isVisible()]

                # Get the cardinal direction corresponding to the position
                try:
                    direction = position_to_direction[position]
                except Exception as e:
                    print(f"Error when getting direction: {e}")
                    continue

                # Get the arrows that end at the direction
                arrows = [arrow for arrow in self.scene.items() if isinstance(arrow, Arrow) and arrow.end_location == direction]

                if len(arrows) != 2:
                    continue  # Skip if there are not exactly two arrows

                # Sort the arrows based on their start position to ensure consistent ordering
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

                # Determine the correct beta SVG file
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

                # Add the beta SVG
                beta_svg = QGraphicsSvgItem(beta_svg_file)
                self.scene.addItem(beta_svg)

                # Adjust the position to center the beta SVG
                if orientation == 'vertical':
                    adjusted_position = QPointF(position[0] - 20, position[1] - 0)
                else:  # orientation is horizontal
                    adjusted_position = QPointF(position[0] - 0, position[1] - 20)

                # Set the position of the beta SVG
                beta_svg.setPos(self.staff_locations[direction.capitalize() + "_staff"])
                beta_svg.setPos(adjusted_position)

                # Add the beta SVG to the list of beta staves
                self.beta_staves.append(beta_svg)
            
            else:
                continue

class StaffTracker(QObject):
    positionChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.position = None

    def update_position(self, new_position):
        self.position = new_position
        self.positionChanged.emit(self.get_position_name())

    # def get_position_name(self):
    #     # return the position name based on self.position