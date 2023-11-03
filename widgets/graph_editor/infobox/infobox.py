from PyQt6.QtWidgets import QFrame
from widgets.graph_editor.infobox.infobox_manager import InfoboxManager

class InfoboxFrame(QFrame):
    def __init__(self, main_widget, graphboard_view):
        super().__init__()
        self.main_widget = main_widget
        self.graphboard_view = graphboard_view
        self.manager = InfoboxManager(self)
        self.updater = self.manager.updater
        
    
