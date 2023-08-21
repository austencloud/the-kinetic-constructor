from PyQt5.QtCore import QPointF, pyqtSignal, Qt, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem, QApplication
from arrow import Arrow
from lxml import etree
from settings import Settings


class Staff(QGraphicsSvgItem):
    attributesChanged = pyqtSignal()  # Define the signal

    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None, initial_visibility=True):
        super().__init__()

        self.element_id = element_id
        self.position = position 
        self.renderer = QSvgRenderer(staff_svg_file)
        self.setSharedRenderer(self.renderer)
        self.setElementId(self.element_id)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
    

        # if the staff isn't already in the scene, add it. Handle errors for QGraphicsScene::addItem: item has already been added to this scene
        if self.scene() is None:
            scene.addItem(self)
        elif self.scene():
            #do nothing
            pass
        

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
        self.is_in_propbox = True
        self.is_in_graphboard = False
        self.svg_file = staff_svg_file
        self.color = color

        # Connect the signal to the update method
        self.attributesChanged.connect(self.update_staff)
    
    def mousePressEvent(self, event):
        # If the staff is in the prop box, initiate the drag operation
        if self.is_in_propbox:
            self.setCursor(Qt.ClosedHandCursor)
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        # If the staff is on the graph board
        if self.is_in_graphboard:
            # Get the current mouse position
            mouse_position = event.scenePos()

            # Get the nearest staff location from the Staff_Handler
            nearest_location = self.staff_manager.get_nearest_staff_location(mouse_position)

            # Set the staff's position to the nearest location
            self.setPos(nearest_location)
        super().mouseReleaseEvent(event)
        
    def mouseReleaseEvent(self, event):
        # Handle mouse release event (snapping functionality will be implemented here later)
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)
        
    def update_attributes(self, new_attributes):
        # Update the attributes
        self.element_id = new_attributes.get('element_id', self.element_id)
        self.position = new_attributes.get('position', self.position)
        self.svg_file = new_attributes.get('svg_file', self.svg_file)
        self.color = new_attributes.get('color', self.color)

        # Emit the signal
        self.attributesChanged.emit()

    def update_staff(self):
        # Update the staff based on the new attributes
        self.setElementId(self.element_id)
        self.setPos(self.position)
        self.renderer.load(self.svg_file)
        self.setSharedRenderer(self.renderer)
        # Add code to update the color if necessary

    def get_width(self):
        return self.boundingRect().width()
    
    def get_height(self):
        return self.boundingRect().height()

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
        # Create a new graphboard_Staff object when the staff is dragged into the graphboard
        # You'll need to replace this with the actual code that implements this behavior
        if self.is_in_graphboard():
            new_staff = Graphboard_Staff(self.element_id, self.scene, self.position, self.color, self.svg_file)
            self.scene.addItem(new_staff)
        super().mouseReleaseEvent(event)

class Staff_Handler(QObject):
    positionChanged = pyqtSignal(str)

    def __init__(self, scene, grid, graphboard, staff):
        super().__init__()  # Initialize the QObject
        self.scene = scene
        self.beta_staves = []
        self.previous_position = None
        self.grid = grid
        self.graphboard = graphboard
        self.staff = staff

    def init_staves(self, scene):
        STAFF_WIDTH = 25
        STAFF_LENGTH = 250
        
        scale = self.grid.scale()
        GRID_WIDTH = self.grid.get_width()
        GRAPHBOARD_WIDTH = self.graphboard.width()
        self.GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (self.graphboard.height() - self.graphboard.width()) / 2
        print("Grid width:", GRID_WIDTH)
        print("Graphboard width:", GRAPHBOARD_WIDTH)
        print(f"GRID_PADDING: {self.GRID_PADDING}")

        N_hand_point_coordinates = self.grid.get_circle_coordinates("N_hand_point")
        E_hand_point_coordinates = self.grid.get_circle_coordinates("E_hand_point")
        S_hand_point_coordinates = self.grid.get_circle_coordinates("S_hand_point")
        W_hand_point_coordinates = self.grid.get_circle_coordinates("W_hand_point")
        

        #print the x value of the N_hand_point
        N_hand_point_x, N_hand_point_y = N_hand_point_coordinates
        E_hand_point_x, E_hand_point_y = E_hand_point_coordinates
        S_hand_point_x, S_hand_point_y = S_hand_point_coordinates
        W_hand_point_x, W_hand_point_y = W_hand_point_coordinates

        #scale the x and y coordinates
        N_hand_point_x = N_hand_point_x * self.grid.scale()
        N_hand_point_y = N_hand_point_y * self.grid.scale()
        E_hand_point_x = E_hand_point_x * self.grid.scale()
        E_hand_point_y = E_hand_point_y * self.grid.scale()
        S_hand_point_x = S_hand_point_x * self.grid.scale()
        S_hand_point_y = S_hand_point_y * self.grid.scale()
        W_hand_point_x = W_hand_point_x * self.grid.scale()
        W_hand_point_y = W_hand_point_y * self.grid.scale()
        

        print("Vertical offset:", self.GRID_V_OFFSET)
        print("N_hand_point_y:", N_hand_point_y)

        # These handpoints are being set according to the grid's coordinates, not the graphboard scene coordinates
        hand_points = {
            'N_hand_point': QPointF(N_hand_point_x, N_hand_point_y),
            'E_hand_point': QPointF(E_hand_point_x, E_hand_point_y),
            'S_hand_point': QPointF(S_hand_point_x, S_hand_point_y),
            'W_hand_point': QPointF(W_hand_point_x, W_hand_point_y)
        }

        print("N_hand_point:", hand_points['N_hand_point'])


        self.staff_locations = {
            'N_staff': QPointF(N_hand_point_x + self.GRID_PADDING - (STAFF_WIDTH / 2), N_hand_point_y + self.GRID_PADDING - (STAFF_LENGTH / 2)),
            'E_staff': QPointF(E_hand_point_x + self.GRID_PADDING - (STAFF_LENGTH / 2), E_hand_point_y + self.GRID_PADDING - (STAFF_WIDTH / 2)),
            'S_staff': QPointF(S_hand_point_x + self.GRID_PADDING - (STAFF_WIDTH / 2), S_hand_point_y + self.GRID_PADDING - (STAFF_LENGTH / 2)),
            'W_staff': QPointF(W_hand_point_x + self.GRID_PADDING - (STAFF_LENGTH / 2), W_hand_point_y + self.GRID_PADDING - (STAFF_WIDTH / 2))
        }

        # Initialize the staffs attribute
        self.graphboard_staffs = {
            'N_staff_red': Graphboard_Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_red.svg'),
            'E_staff_red': Graphboard_Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_red.svg'),
            'S_staff_red': Graphboard_Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_red.svg'),
            'W_staff_red': Graphboard_Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_red.svg'),
            'N_staff_blue': Graphboard_Staff('N_staff', scene, self.staff_locations['N_staff'], None, 'images\\staves\\N_staff_blue.svg'),
            'E_staff_blue': Graphboard_Staff('E_staff', scene, self.staff_locations['E_staff'], None, 'images\\staves\\E_staff_blue.svg'),
            'S_staff_blue': Graphboard_Staff('S_staff', scene, self.staff_locations['S_staff'], None, 'images\\staves\\S_staff_blue.svg'),
            'W_staff_blue': Graphboard_Staff('W_staff', scene, self.staff_locations['W_staff'], None, 'images\\staves\\W_staff_blue.svg')
        }
        
        self.beta_staves = [
            BetaStaff('beta_vertical_w-blue_e-red', scene, self.staff_locations['N_staff'], None, 'images/staves/beta/beta_vertical_w-blue_e-red.svg'),
            BetaStaff('beta_vertical_w-red_e-blue', scene, self.staff_locations['E_staff'], None, 'images/staves/beta/beta_vertical_w-red_e-blue.svg'),
            BetaStaff('beta_horizontal_n-red_s_blue', scene, self.staff_locations['S_staff'], None, 'images/staves/beta/beta_horizontal_n-red_s_blue.svg'),
            BetaStaff('beta_horizontal_n-blue_s-red', scene, self.staff_locations['W_staff'], None, 'images/staves/beta/beta_horizontal_n-blue_s-red.svg')
        ]
        
        self.hide_all_graphboard_staffs()
        
    def connect_to_graphboard(self, graphboard):
        self.graphboard = graphboard

    #get the coordinates of the cy item in the grid.svg file
    def get_grid_cy(self):
        grid_svg = etree.parse('images\\grid\\grid.svg')
        cy = grid_svg.xpath('//circle/@cy')
        cy = float(cy[0])
        return cy
    
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

    def get_nearest_staff_location(self, mouse_position):
        # Find the nearest staff location based on the current mouse position
        nearest_location = None
        min_distance = float('inf')
        for location, position in self.staff_locations.items():
            distance = (mouse_position - position).manhattanLength()
            if distance < min_distance:
                min_distance = distance
                nearest_location = position
        return nearest_location

    def hide_all_graphboard_staffs(self):
        for staff in self.graphboard_staffs.values():
            staff.hide()

    def show_staff(self, direction):
        direction = direction.capitalize()
        staff = self.graphboard_staffs.get(direction)
        if staff:
            staff.show()
        else:
            print(f"No staff found for direction {direction}")


    def remove_beta_staves(self):
        for beta_staff in self.beta_staves:
            if beta_staff.scene is not None:
                ### NOT CAUSING THE ERROR
                self.scene.removeItem(beta_staff)
        self.beta_staves = []

    def remove_non_beta_staves(self):
        for staff in self.graphboard_staffs.values():
            if staff.isVisible() and staff.scene is not None:

                self.scene.removeItem(staff)
                staff.hide()  # Hide the staff



    def update_graphboard_staffs(self, scene):
        self.hide_all_graphboard_staffs()
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
        position_to_direction = {
            (self.staff_locations['N_staff'].x(), self.staff_locations['N_staff'].y()): 'n',
            (self.staff_locations['E_staff'].x(), self.staff_locations['E_staff'].y()): 'e',
            (self.staff_locations['S_staff'].x(), self.staff_locations['S_staff'].y()): 's',
            (self.staff_locations['W_staff'].x(), self.staff_locations['W_staff'].y()): 'w',
        }

        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:
                staves_to_remove = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]
                for staff in staves_to_remove:
                    ### not causing the error ### 
                    self.scene.removeItem(staff)
                    staff.hide()
                    self.scene.update()
                    # Remove the staff from the graphboard_staffs dictionary
                    self.graphboard_staffs = {key: value for key, value in self.graphboard_staffs.items() if value != staff}
                        
                staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

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


class BetaStaff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)
        #make item unselectable
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
    def mouseReleaseEvent(self, event):
        # Snap the staff to its correct placement and orientation
        # You'll need to replace this with the actual code that implements this behavior
        self.setPos(self.correct_position)
        self.setRotation(self.correct_orientation)
        super().mouseReleaseEvent(event)

class StaffTracker(QObject):
    positionChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.position = None

    def update_position(self, new_position):
        self.position = new_position
        self.positionChanged.emit(self.get_position_name())



    def mousePressEvent(self, event):
        # Handle mouse press event for drag-and-drop
        self.setCursor(Qt.ClosedHandCursor)
        self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Handle mouse move event for dragging
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.setPos(self.mapToScene(event.pos() - self.drag_start_position))

    def mouseReleaseEvent(self, event):
        # Handle mouse release event (snapping functionality will be implemented here later)
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)
