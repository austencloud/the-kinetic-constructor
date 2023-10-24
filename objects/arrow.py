from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QPointF
from managers.arrow_management.arrow_attributes import ArrowAttributes
from data.start_end_location_mapping import start_end_location_mapping

class Arrow(QGraphicsSvgItem):
    def __init__(self, svg_file, view, arrow_dict):
        super().__init__(svg_file)
        
        self.initialize_app_attributes(svg_file, view)
        self.initialize_dict_attributes(arrow_dict)
        self.initialize_svg_renderer()
        self.initialize_graphics_flags()
        self.attributes = ArrowAttributes(self, arrow_dict)

    def initialize_dict_attributes(self, arrow_dict):
        self.color = arrow_dict.get('color', 'default_color')
        self.motion_type = arrow_dict.get('motion_type', 'default_motion_type')
        self.rotation_direction = arrow_dict.get('rotation_direction', 'default_rotation_direction')
        self.quadrant = arrow_dict.get('quadrant', 'default_quadrant')
        self.end_location = arrow_dict.get('end_location', 'default_end_location')
        self.start_location = arrow_dict.get('start_location', 'default_start_location')
        self.turns = int(arrow_dict.get('turns', 0))

    def initialize_app_attributes(self, svg_file, view):
        self.view = view
        self.info_frame = view.info_frame
        self.svg_file = svg_file
        self.main_widget = view.main_widget
        self.svg_manager = self.main_widget.svg_manager
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_manager.arrow = self
        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)
        self.is_ghost = False
        self.staff = None
        self.is_mirrored = False
        self.previous_arrow = None
        self.center = self.boundingRect().center()

    def initialize_graphics_flags(self):
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setTransformOriginPoint(self.boundingRect().center())

    def initialize_svg_renderer(self):
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
                    self.update_appearance()
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
    

    # UPDATE APPEARANCE          
        
    def update_appearance(self):
        self.update_color()
        self.update_rotation()
        
    def update_color(self):
        if self.motion_type in ["pro", "anti"]:
            new_svg_data = self.svg_manager.set_svg_color(self.svg_file, self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)
            
    def update_rotation(self):
        r_quadrant_to_angle = {
            "ne": 0,
            "se": 90,
            "sw": 180,
            "nw": 270
        }
        
        l_quadrant_to_angle = {
            "ne": 0,
            "se": 270,
            "sw": 180,
            "nw": 90
        }

        if self.rotation_direction == "r":
            angle = r_quadrant_to_angle.get(self.quadrant, 0)
        else:
            angle = l_quadrant_to_angle.get(self.quadrant, 0)
        self.setRotation(angle)
    
    
