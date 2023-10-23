import os
import re
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF, QByteArray
from data.start_end_location_mapping import start_end_location_mapping
class Arrow(QGraphicsSvgItem):
    def __init__(self, svg_file, view, info_frame, svg_manager, arrow_manager, motion_type, staff_manager, color, quadrant, rotation_direction, turns, arrow_dict):
        super().__init__(svg_file)
        self.initialize_attributes(svg_file, view, info_frame, svg_manager, arrow_manager, motion_type, staff_manager, color, quadrant, rotation_direction, turns, arrow_dict)
        self.set_flags()
        self.set_renderer()
        self.update_appearance()

    def initialize_attributes(self, svg_file, view, info_frame, svg_manager, arrow_manager, motion_type, staff_manager, color, quadrant, rotation_direction, turns, arrow_dict):
        self.view = view
        self.info_frame = info_frame
        self.dict = arrow_dict
        self.svg_file = svg_file
        self.svg_manager = svg_manager
        self.motion_type = motion_type
        self.color = color
        self.quadrant = quadrant
        self.rotation_direction = rotation_direction
        self.turns = turns
        self.staff_manager = staff_manager
        self.arrow_manager = arrow_manager
        self.arrow_manager.arrow = self
        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)
        self.is_ghost = False
        self.staff = None
        self.previous_arrow = None
        self.center = self.boundingRect().center()

    def set_flags(self):
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setTransformOriginPoint(self.boundingRect().center())

    def set_renderer(self):
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.drag_start_pos = self.pos()  # Store the initial position of the arrow
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        self.setSelected(True) 
        if event.buttons() == Qt.MouseButton.LeftButton:
            from views.graphboard_view import GraphboardView
            from views.pictograph_view import PictographView
            if isinstance(self.view, GraphboardView):
                new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
                self.setPos(new_pos)
                new_quadrant = self.view.get_graphboard_quadrants(new_pos + self.center)  
                if self.quadrant != new_quadrant:
                    self.update_arrow_for_new_quadrant(new_quadrant)
                    self.info_frame.update()
            elif isinstance(self.view, PictographView):
                new_pos = self.mapToScene(event.pos()) - self.drag_offset / 2
                self.setPos(new_pos)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'future_position'):
            self.setPos(self.future_position)
            del self.future_position
        from views.graphboard_view import GraphboardView
        if isinstance(self.view, GraphboardView):
            self.arrow_manager.arrow_positioner.update_arrow_position(self.view)
        
    ### ATTRIBUTES ###

    def update_arrow_for_new_quadrant(self, new_quadrant):
        if new_quadrant in start_end_location_mapping:
            if self.rotation_direction in start_end_location_mapping[new_quadrant]:
                if self.motion_type in start_end_location_mapping[new_quadrant][self.rotation_direction]:
                    self.quadrant = new_quadrant
                    self.start_location, self.end_location = start_end_location_mapping[self.quadrant][self.rotation_direction][self.motion_type]
                    self.update_appearance()


    def update_attributes(self):
        if self.dict:
            self.set_attributes_from_dict(self.dict)
        if self.svg_file: 
            self.set_attributes_from_filename()
        if self.motion_type == 'pro' or self.motion_type == 'anti':
            self.set_start_end_locations()
        self.update_appearance()
    
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
        self.motion_type, self.turns = parts[:2]
        self.turns = int(self.turns.split('.')[0])

    def set_start_end_locations(self):
        self.start_location, self.end_location = start_end_location_mapping.get(self.quadrant, {}).get(self.rotation_direction, {}).get(self.motion_type, (None, None))

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

    def set_svg_file_from_attributes(self):
        if self.motion_type in ["pro", "anti"] and self.color in ["red", "blue"]:
            self.svg_file = f"images/arrows/shift/{self.motion_type}/{self.color}_{self.motion_type}_{self.rotation_direction}_{self.quadrant}_{self.turns}.svg"
        elif self.motion_type == 'static':
            self.svg_file = None




    ### GETTERS ###

    def get_attributes(self):
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



    def update_appearance(self):
        self.update_color()
        self.update_rotation()
        
    def update_color(self):
        if self.motion_type in ["pro", "anti"]:
            new_svg_data = self.svg_manager.set_svg_color(self.svg_file, self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)
            
    def update_rotation(self):
        quadrant_to_angle = {
            "ne": 0,
            "se": 90,
            "sw": 180,
            "nw": 270
        }
        angle = quadrant_to_angle.get(self.quadrant, 0)

        self.setRotation(angle)
    
    def mirror(self):
        svg_file_path = os.path.join(self.svg_file)
        with open(svg_file_path, 'r') as f:
            svg_data = f.read()
        new_svg_data = self.mirror_svg_data(svg_data)  # Assuming svg_manager is accessible here
        byte_array = QByteArray(new_svg_data.encode())
        self.renderer.load(byte_array)

        self.rotation_direction = 'l' if self.rotation_direction == 'r' else 'r'


        self.update_appearance()

    def mirror_svg_data(self, svg_data):
        # Find the transform attribute of the path with id "blue_pro_r_ne"
        pattern = re.compile(r'(transform=")([^"]+)(")')
        match = pattern.search(svg_data)
        if match:
            original_transform = match.group(2)
            width = self.boundingRect().width()  # Replace with the actual width of the image if it's not 270
            new_transform = f'scale(-1, 1) translate({width}, 0) rotate(90) {original_transform}'
            svg_data = pattern.sub(f'\\1{new_transform}\\3', svg_data)
        return svg_data