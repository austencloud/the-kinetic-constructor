from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
import re
class Arrow(QGraphicsSvgItem):
    def __init__(self, view, attr_dict):
        self.svg_file = self.get_svg_file(attr_dict)
        super().__init__(self.svg_file)
        
        self.initialize_svg_renderer(self.svg_file)
        self.initialize_app_attributes(view, attr_dict)
        self.initialize_graphics_flags()

    def get_svg_file(self, attr_dict):
        motion_type = attr_dict['motion_type']
        turns = attr_dict.get('turns', None)
        
        if motion_type in ["pro", "anti"]:
            self.is_shift = True
            return f"images/arrows/shift/{motion_type}_{turns}.svg"
        elif motion_type in ["static"]:
            self.is_static = True
            return f"images/arrows/{motion_type}_blank.svg"

    def initialize_app_attributes(self, view, dict):
        self.view = view
        self.info_frame = view.info_frame
        self.main_widget = view.main_widget
        self.arrow_manager = self.main_widget.arrow_manager
        self.attributes = self.arrow_manager.arrow_attributes
        self.attributes.update_attributes(self, dict)
        self.arrow_manager.arrow = self
        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)
        self.is_ghost = False
        self.staff = None
        self.is_mirrored = False
        self.previous_arrow = None
        self.center = self.boundingRect().center()
        self.setScale(view.view_scale)
        self.update_appearance()

    def initialize_graphics_flags(self):
        flags = [
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
        ]
        
        for flag in flags:
            self.setFlag(flag, True)
        
        self.setTransformOriginPoint(self.center)


    def initialize_svg_renderer(self, svg_file):
        if getattr(self, 'is_shift', False):
            self.renderer = QSvgRenderer(svg_file)
            self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.drag_start_pos = self.pos()  # Store the initial position of the arrow
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        self.setSelected(True) 
        if event.buttons() == Qt.MouseButton.LeftButton:
            from graph_editor.graphboard.graphboard_view import GraphboardView
            from objects.pictograph.pictograph_view import PictographView
            if isinstance(self.view, GraphboardView):
                new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
                self.setPos(new_pos)
                new_quadrant = self.view.get_graphboard_quadrants(new_pos + self.center)  
                if self.quadrant != new_quadrant:
                    self.quadrant = new_quadrant
                    self.update_appearance()
                    self.info_frame.update()
            elif isinstance(self.view, PictographView):
                new_pos = self.mapToScene(event.pos()) - self.drag_offset / 2
                self.setPos(new_pos)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'future_position'):
            self.setPos(self.future_position)
            del self.future_position
        from graph_editor.graphboard.graphboard_view import GraphboardView
        if isinstance(self.view, GraphboardView):
            self.arrow_manager.arrow_positioner.update_arrow_position(self.view)
    
    # UPDATE APPEARANCE          
        
    def update_appearance(self):
        self.update_color()
        self.update_rotation()
     
    def set_svg_color(self, svg_file, new_color):
        color_map = {
            "red": "#ED1C24",
            "blue": "#2E3192"
        }
        new_hex_color = color_map.get(new_color)

        with open(svg_file, 'r') as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(r'\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}', re.DOTALL)
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode('utf-8')     
        
    def update_color(self):
        if self.motion_type in ["pro", "anti"]:
            new_svg_data = self.set_svg_color(self.svg_file, self.color)
            
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)
            
    def update_rotation(self):
        angle = self.get_rotation_angle()
        self.setRotation(angle)

    def get_rotation_angle(self):
        quadrant_to_angle = self.get_quadrant_to_angle_map()
        return quadrant_to_angle.get(self.quadrant, 0)

    def get_quadrant_to_angle_map(self):
        if self.motion_type == 'pro':
            return {
                "r": {"ne": 0, "se": 90, "sw": 180, "nw": 270},
                "l": {"ne": 0, "se": 90, "sw": 180, "nw": 270}
            }.get(self.rotation_direction, {})
        elif self.motion_type == 'anti':
            return {
                "r": {"ne": 0, "se": 90, "sw": 180, "nw": 270},
                "l": {"ne": 0, "se": 90, "sw": 180, "nw": 270}
            }.get(self.rotation_direction, {})
        elif self.motion_type == 'static':
            return {
                "r": {"ne": 0, "se": 0, "sw": 0, "nw": 0},
                "l": {"ne": 0, "se": 0, "sw": 0, "nw": 0}
            }.get(self.rotation_direction, {})
