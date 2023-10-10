import os
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtCore import Qt, QPointF, QTimer
from data.ARROW_START_END_LOCATIONS import ARROW_START_END_LOCATIONS
from PyQt5.QtGui import QPixmap, QPainter

class Arrow(QGraphicsSvgItem):
    def __init__(self, svg_file, graphboard_view, info_tracker, svg_manager, arrow_manager, motion_type, staff_manager, dict):
        super().__init__(svg_file)
        
        # Connectors
        self.graphboard_view = graphboard_view
        self.info_tracker = info_tracker
        self.dict = dict
        self.svg_file = svg_file
        self.svg_manager = svg_manager
        
        # Managers
        self.staff_manager = staff_manager
        self.svg_manager = svg_manager
        self.arrow_manager = arrow_manager
        self.arrow_manager.connect_arrow(self)
        
        # Flags
        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)  # Initialize drag_offset

        # Other
        self.staff = None
        self.previous_arrow = None
        
        self.renderer = QSvgRenderer(self.svg_file)    
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsSvgItem.ItemIsMovable, True)
        self.setFlag(QGraphicsSvgItem.ItemIsSelectable, True)
        self.setTransformOriginPoint(self.boundingRect().center())

        if motion_type != 'static':
            self.update_attributes()

    def mousePressEvent(self, event):
        
        self.arrow_manager.prepare_dragging(event)
        self.drag_start_pos = self.pos()  # Store the initial position of the arrow
        self.drag_offset = event.pos() - self.boundingRect().topLeft()

    def mouseMoveEvent(self, event):
        self.setSelected(True)  # Add this line
        if event.buttons() == Qt.LeftButton:
            from views.graphboard_view import Graphboard_View
            if isinstance(self.graphboard_view, Graphboard_View):
                new_pos = self.mapToScene(event.pos()) - self.drag_offset
                self.setPos(new_pos)  # Directly set the new position

                new_quadrant = self.graphboard_view.get_graphboard_quadrants(new_pos)  
                if self.quadrant != new_quadrant:
                    self.update_arrow_for_new_quadrant(new_quadrant)
                    self.info_tracker.update()

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'future_position'):
            self.setPos(self.future_position)  # Set the position when mouse is released
            del self.future_position  # Delete the attribute for future use

    ### ATTRIBUTES ###

    def update_attributes(self):
        if self.dict:
            self.set_attributes_from_dict(self.dict)
        elif self.svg_file: 
            self.set_attributes_from_filename()
        if self.motion_type == 'pro' or self.motion_type == 'anti':
            self.set_start_end_locations()
            
    def set_attributes_from_dict(self, arrow_dict):
        self.color = arrow_dict['color']
        self.motion_type = arrow_dict['motion_type']
        self.rotation_direction = arrow_dict['rotation_direction']
        self.quadrant = arrow_dict['quadrant']
        self.end_location = arrow_dict['end_location']
        self.start_location = arrow_dict['end_location']
        self.turns = int(arrow_dict['turns'])

    def set_attributes_from_filename(self):
        parts = os.path.basename(self.svg_file).split('_')
        self.color, self.motion_type, self.rotation_direction, self.quadrant, self.turns = parts[:5]
        self.turns = int(self.turns.split('.')[0])

    def set_start_end_locations(self):
        self.arrow_start_end_locations = {
            f"{self.color}_{key}": value for key, value in ARROW_START_END_LOCATIONS.items()
        }
        self.start_location, self.end_location = self.arrow_start_end_locations.get(os.path.basename(self.svg_file), (None, None))

    def set_static_attributes_from_deleted_arrow(self, deleted_arrow):
        self.color = deleted_arrow.color
        self.motion_type = 'static'
        self.rotation_direction = 'None'
        self.quadrant = 'None'
        self.start_location = deleted_arrow.end_location
        self.end_location = deleted_arrow.end_location
        self.turns = 0
        self.staff = deleted_arrow.staff
        self.staff.arrow = self

    ### GETTERS ###

    def get_attributes(self):
        self.svg_file = f"images/arrows/shift/{self.motion_type}/{self.color}_{self.motion_type}_{self.rotation_direction}_{self.quadrant}_{self.turns}.svg"
        attributes = {
            'color': self.color,
            'quadrant': self.quadrant,
            'rotation_direction': self.rotation_direction, 
            'motion_type': self.motion_type,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'turns': self.turns
        }
        return attributes

    def get_center_position(self):
        return self.pos() + self.boundingRect().center()

    def update_arrow_for_new_quadrant(self, new_quadrant):
        self.quadrant = new_quadrant

        # Inline the logic for generating the new SVG path
        base_name = os.path.basename(self.svg_file)
        color, motion_type = base_name.split("_", 2)[:2]
        if motion_type in ["pro", "anti"] and color in ["red", "blue"]:
            new_svg_file = f'images\\arrows\\shift\\{self.motion_type}\\{color}_{motion_type}_{self.rotation_direction}_{new_quadrant}_{self.turns}.svg'
        else:
            print(f"Unexpected svg_file: {self.svg_file}")
            new_svg_file = self.svg_file

        self.svg_file = new_svg_file
        self.update_attributes()
        self.set_svg_renderer(self.svg_file)

    def set_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)


    ### UPDATERS ###

    def update_arrow_position(self):
        pos = self.graphboard_view.get_quadrant_center(self.get_attributes()['quadrant']) - self.boundingRect().center()
        self.setPos(pos)

    def update_arrow_image(self):
        if self.motion_type == 'pro' or self.motion_type == 'anti':
            new_filename = f"images\\arrows\\shift\\{self.motion_type}\\{self.color}_{self.motion_type}_{self.rotation_direction}_{self.quadrant}_{self.turns}.svg"
            if os.path.isfile(new_filename):
                self.svg_file = new_filename
                self.setSharedRenderer(self.svg_manager.get_renderer(new_filename))
            else:
                print(f"File {new_filename} does not exist")
