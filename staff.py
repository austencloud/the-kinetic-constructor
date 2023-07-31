from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from arrow import Arrow

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

        # Add a "staff" attribute to the item
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

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def set_arrow(self, arrow):
        self.arrow = arrow
        
    def isVisible(self):
        return super().isVisible()

class Artboard_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)

    def mouseReleaseEvent(self, event):
        # Snap the staff to its correct placement and orientation
        # You'll need to replace this with the actual code that implements this behavior
        self.setPos(self.correct_position)
        self.setRotation(self.correct_orientation)
        super().mouseReleaseEvent(event)

class PropBox_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file)

    def mouseReleaseEvent(self, event):
        # Create a new Artboard_Staff object when the staff is dragged into the artboard
        # You'll need to replace this with the actual code that implements this behavior
        if self.is_in_artboard():
            new_staff = Artboard_Staff(self.element_id, self.scene, self.position, self.color, self.svg_file)
            self.scene.addItem(new_staff)
        super().mouseReleaseEvent(event)

class Staff_Manager(QObject):
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
        self.artboard_staffs = {
            'N_staff_red': Artboard_Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_red.svg'),
            'E_staff_red': Artboard_Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_red.svg'),
            'S_staff_red': Artboard_Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_red.svg'),
            'W_staff_red': Artboard_Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_red.svg'),
            'N_staff_blue': Artboard_Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_blue.svg'),
            'E_staff_blue': Artboard_Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_blue.svg'),
            'S_staff_blue': Artboard_Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_blue.svg'),
            'W_staff_blue': Artboard_Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_blue.svg')
        }

        self.hide_all_artboard_staffs()

    def hide_all_artboard_staffs(self):
        for staff in self.artboard_staffs.values():
            staff.hide()

    def show_staff(self, direction):
        direction = direction.capitalize()
        staff = self.artboard_staffs.get(direction)
        if staff:
            staff.show()
        else:
            print(f"No staff found for direction {direction}")


    def remove_beta_staves(self):
        for beta_staff in self.beta_staves:
            if beta_staff.scene() is not None:
                self.scene.removeItem(beta_staff)
        self.beta_staves = []

    def remove_non_beta_staves(self):
        for staff in self.artboard_staffs.values():
            if staff.isVisible() and staff.scene() is not None:
                self.scene.removeItem(staff)
                staff.hide()  # Hide the staff


    def update_artboard_staffs(self, scene):
        self.hide_all_artboard_staffs()
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
                
                new_staff = Artboard_Staff(end_location + "_staff", scene, self.staff_locations[end_location + "_staff"], color, 'images\\staves\\' + end_location + "_staff_" + color + '.svg')
                if new_staff.scene is None:
                    self.scene.addItem(new_staff)
                self.artboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary

    
    def check_and_replace_staves(self):
        position_to_direction = {
            (self.staff_locations['N_staff'].x(), self.staff_locations['N_staff'].y()): 'n',
            (self.staff_locations['E_staff'].x(), self.staff_locations['E_staff'].y()): 'e',
            (self.staff_locations['S_staff'].x(), self.staff_locations['S_staff'].y()): 's',
            (self.staff_locations['W_staff'].x(), self.staff_locations['W_staff'].y()): 'w',
        }

        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.artboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:
                staves_to_remove = [staff for staff in self.artboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]
                for staff in staves_to_remove:
                    self.scene.removeItem(staff)
                    staff.hide()
                    self.scene.update()
                    # Remove the staff from the artboard_staffs dictionary
                    self.artboard_staffs = {key: value for key, value in self.artboard_staffs.items() if value != staff}
                        
                staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.artboard_staffs.values() if staff.isVisible()]

                try:
                    direction = position_to_direction[position]
                except Exception as e:
                    print(f"Error when getting direction: {e}")
                    continue

                arrows = [arrow for arrow in self.scene.items() if isinstance(arrow, Arrow) and arrow.end_location == direction]

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
                self.scene.addItem(beta_svg)

                if orientation == 'vertical':
                    adjusted_position = QPointF(position[0] - 20, position[1] - 0)
                else:  # orientation is horizontal
                    adjusted_position = QPointF(position[0] - 0, position[1] - 20)

                beta_svg.setPos(self.staff_locations[direction.capitalize() + "_staff"])
                beta_svg.setPos(adjusted_position)

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

