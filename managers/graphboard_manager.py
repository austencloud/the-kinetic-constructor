class Graphboard_Manager():
    def __init__(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.graphboard_scene = graphboard_view.scene()
        
    
    def get_graphboard_quadrants(self, mouse_pos, graphboard_view, arrow):
        offset = (graphboard_view.height() - graphboard_view.width()) / 2
        adjusted_mouse_y = mouse_pos.y() + offset + arrow.boundingRect().height() / 2
        adjusted_mouse_x = mouse_pos.x() + arrow.boundingRect().width() / 2
        if adjusted_mouse_y < graphboard_view.sceneRect().height() / 2:
            if adjusted_mouse_x < graphboard_view.sceneRect().width() / 2:
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if adjusted_mouse_x < graphboard_view.sceneRect().width() / 2:
                quadrant = 'sw'
            else:
                quadrant = 'se'
        return quadrant