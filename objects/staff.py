from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem



class Staff(QGraphicsSvgItem):
    def __init__(self, element_id, scene, position, axis, color=None, staff_svg_file=None, initial_visibility=True):
        super().__init__()
        print("staff created: " + element_id)
        self.element_id = element_id
        self.position = position 
        self.renderer = QSvgRenderer(staff_svg_file)
        self.setSharedRenderer(self.renderer)
        self.setElementId(self.element_id)
        scene.addItem(self)
        self.setVisible(initial_visibility)
        self.scene = scene
        self.setPos(position)
        self.arrow = None
        self.setVisible(True)
        rect = self.boundingRect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.setPos(position)
        self.svg_file = staff_svg_file
        self.color = color
        self.axis = axis
        #make them selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)



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