from settings.string_constants import *


class Manipulators:
    def __init__(self, graphboard):
        self.graphboard = graphboard

    def swap_colors(self):
        if self.graphboard.current_letter != "G" and self.graphboard.current_letter != "H":
            if len(self.graphboard.arrows) >= 1:
                for arrow in self.graphboard.arrows:
                    if arrow.color == RED:
                        new_color = BLUE
                    elif arrow.color == BLUE:
                        new_color = RED
                    else:
                        continue
                    arrow.color = new_color
                    arrow.staff.color = new_color
                    arrow.update_appearance()
                    arrow.staff.update_appearance()
                    
                self.graphboard.update()
