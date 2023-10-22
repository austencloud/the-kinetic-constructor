from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from settings import GRAPHBOARD_SCALE, PICTOGRAPH_SCALE
from settings import STAFF_WIDTH, STAFF_LENGTH
class Staff(QGraphicsSvgItem):
    def __init__(self, scene, xy_location, color, location=None, context=None):
        super().__init__()
        image_file = f'images/staffs/staff.svg'
        self.xy_location = xy_location 
        self.renderer = QSvgRenderer(image_file)
        self.setSharedRenderer(self.renderer)
        scene.addItem(self)
        self.arrow = None
        self.setVisible(True)

        #after rotating, make sure the transform origin posint is set to the center
        self.setTransformOriginPoint(0, 0)
        self.svg_file = image_file
        self.set_color(color)
        self.location = location
        
        if context == 'graphboard':
            if location == 'N' or location == 'S':
                self.axis = 'vertical'
                self.setRotation(90)
                self.setPos(self.xy_location.x() + (STAFF_WIDTH/2) * GRAPHBOARD_SCALE, self.xy_location.y() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE)
            elif location == 'E' or location == 'W':
                self.axis = 'horizontal'
                self.setPos(self.xy_location.x() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE, self.xy_location.y() - (STAFF_WIDTH/2) * GRAPHBOARD_SCALE)
        elif context == 'pictograph':
            if location == 'N' or location == 'S':
                self.axis = 'vertical'
                self.setRotation(90)
                self.setPos(self.xy_location.x() + (STAFF_WIDTH/2) * PICTOGRAPH_SCALE, self.xy_location.y() - (STAFF_LENGTH/2) * PICTOGRAPH_SCALE)
            elif location == 'E' or location == 'W':
                self.axis = 'horizontal'
                self.setPos(self.xy_location.x(), self.xy_location.y())
                self.setPos(self.xy_location.x() - (STAFF_LENGTH/2) * PICTOGRAPH_SCALE, self.xy_location.y() - (STAFF_WIDTH/2) * PICTOGRAPH_SCALE)
        else:
            if location == 'N' or location == 'S':
                self.axis = 'vertical'
                self.setRotation(90)
                self.setPos(self.xy_location.x() + (STAFF_WIDTH/2) * GRAPHBOARD_SCALE, self.xy_location.y() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE)
            elif location == 'E' or location == 'W':
                self.axis = 'horizontal'
                self.setPos(self.xy_location.x() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE, self.xy_location.y() - (STAFF_WIDTH/2) * GRAPHBOARD_SCALE)
                
        self.color = color
        self.context = context
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)


        if context == 'pictograph':
            self.setScale(PICTOGRAPH_SCALE)  
        else:
            self.setScale(GRAPHBOARD_SCALE)


    def mousePressEvent(self, event):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setPos(event.scenePos())
            #drag by the center point of the object, not the top left
            if self.axis == 'vertical':
                self.setPos(event.scenePos().x() + (STAFF_WIDTH/2) * GRAPHBOARD_SCALE, event.scenePos().y() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE)
            elif self.axis == 'horizontal':
                self.setPos(event.scenePos().x() - (STAFF_LENGTH/2) * GRAPHBOARD_SCALE, event.scenePos().y() - (STAFF_WIDTH/2) * GRAPHBOARD_SCALE)
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # Add your snapping logic here
        super().mouseReleaseEvent(event)
    

    def set_element(self, element_id, color):
        self.setElementId(element_id)
        self.color = color
        if color:
            self.set_color(color)


    def set_color(self, new_color):
        # Map the color names to their corresponding hex values
        color_map = {
            "red": "#ed1c24",
            "blue": "#2E3192"
        }

        # Get the hex value for the color name, if it exists in the map
        hex_color = color_map.get(new_color, new_color)

        # Read the SVG file into a string
        with open(self.svg_file, 'r') as f:
            svg_data = f.read()

        # Colors you want to replace
        old_colors = ["#ed1c24", "#2E3192"]

        # Replace the colors
        for old_color in old_colors:
            svg_data = svg_data.replace(old_color, hex_color)

        # Reload the SVG renderer
        self.renderer.load(svg_data.encode('utf-8'))

        # Update the color attribute
        self.color = hex_color



    def hide(self):
        self.setVisible(False)

    def set_arrow(self, arrow):
        self.arrow = arrow
        
    def isVisible(self):
        return super().isVisible()
    
    def set_arrow(self, arrow):
        self.arrow = arrow

    def get_arrow(self):
        return self.arrow