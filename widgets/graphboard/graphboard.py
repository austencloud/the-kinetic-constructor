from typing import List, Optional, Dict, Any, Tuple, Set
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView, QWidget
from PyQt6.QtGui import QTransform
from objects.arrow import Arrow, BlankArrow
from objects.staff import Staff
from objects.grid import Grid
from settings.string_constants import ARROWS, COLOR, MOTION_TYPE, ROTATION_DIRECTION, QUADRANT, START_LOCATION, END_LOCATION, TURNS, RED, BLUE, LETTER_SVG_DIR, NORTHWEST, SOUTHEAST, SOUTHWEST, NORTHEAST, STATIC
from data.letter_types import letter_types
from .graphboard_init import GraphboardInit
from .graphboard_menu_handler import GraphboardMenuHandler
from .position_engines.staff_positioner import StaffPositioner
from .position_engines.arrow_positioner import ArrowPositioner
from utilities.export_handler import ExportHandler
from utilities.letter_engine import LetterEngine
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from PyQt6.QtCore import QPointF

class Graphboard(QGraphicsScene):
    arrows: List[Arrow]
    staffs: List[Staff]
    letter_renderers: Dict[str, QSvgRenderer]
    current_letter: Optional[str]
    infobox: Optional[QGraphicsItem]
    dragged_arrow: Optional[Arrow]
    dragged_staff: Optional[Staff]
    ghost_arrows: Dict[str, Arrow]
    ghost_staffs: Dict[str, Staff]
    grid: Optional[Grid]  
    view: QGraphicsView 
    staff_set: Set[Staff]
    letter_item: QGraphicsSvgItem
    quadrants: Dict[str, Tuple[float, float, float, float]]
    export_handler: ExportHandler
    context_menu_manager: GraphboardMenuHandler
    arrow_positioner: ArrowPositioner
    staff_positioner: StaffPositioner
    letter_engine: LetterEngine
    graph_editor: QWidget 
    
    def __init__(self, main_widget: Any, graph_editor: Any) -> None:
        super().__init__()
        self.setup_scene()
        self.setup_components(main_widget, graph_editor)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 750, 900)
        self.arrows = []
        self.staffs = []
        self.letter_renderers = {}
        self.current_letter = None
        self.infobox = None

    def setup_components(self, main_widget: Any, graph_editor: Any) -> None:
        self.graph_editor = graph_editor
        self.letters = main_widget.letters

        self.dragged_arrow = None
        self.dragged_staff = None

        self.initializer = GraphboardInit(self)

        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.ghost_staffs = self.initializer.init_ghost_staffs()
        self.grid = self.initializer.init_grid()
        self.view = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.letter_item = self.initializer.init_letter_item()
        self.quadrants = self.initializer.init_quadrants(self.grid)
        self.setup_managers(main_widget, graph_editor)

    def setup_managers(self, main_widget: Any, graph_editor: Any) -> None:
        self.export_handler = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardMenuHandler(
            main_widget, graph_editor, self
        )
        self.arrow_positioner = ArrowPositioner(self)
        self.staff_positioner = StaffPositioner(self)
        self.letter_engine = LetterEngine(self)

    ### DELETION ###

    def delete_arrow(self, arrow: Arrow, keep_staff: bool = False) -> None:
        self.removeItem(arrow)
        if arrow in self.arrows:
            self.arrows.remove(arrow)
        if keep_staff:
            self.create_blank_arrow(arrow)
        else:
            self.delete_staff(arrow.staff)

        self.update()

    def delete_staff(self, staff: Staff) -> None:
        self.removeItem(staff)
        self.staffs.remove(staff)
        self.update()

    ### EVENTS ###

    def contextMenuEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        clicked_item = self.itemAt(
            self.view.mapToScene(event.pos().toPoint().x(), event.pos().toPoint().y()),
            QTransform(),
        )
        selected_items = self.selectedItems()
        event_pos = event.screenPos()

        if isinstance(clicked_item, Arrow):
            self.context_menu_manager.create_arrow_menu(selected_items, event_pos)
        elif isinstance(clicked_item, Staff):
            self.context_menu_manager.create_staff_menu(selected_items, event_pos)
        else:
            self.context_menu_manager.create_graphboard_menu(event_pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        clicked_item = self.itemAt(event.scenePos(), QTransform())
        if isinstance(clicked_item, Staff):
            self.dragged_staff = clicked_item
            self.dragged_staff.mousePressEvent(event)  
        elif isinstance(clicked_item, Arrow):
            self.dragged_arrow = clicked_item
            self.dragged_arrow.mousePressEvent()
        else:
            self.dragged_staff = None
            self.dragged_arrow = None

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.dragged_staff:
            self.dragged_staff.mouseMoveEvent(event) 
        elif self.dragged_arrow:
            self.dragged_arrow.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.dragged_staff:
            self.dragged_staff.mouseReleaseEvent(event) 
            self.dragged_staff = None
        elif self.dragged_arrow:
            self.dragged_arrow.mouseReleaseEvent()
            self.dragged_arrow = None

    ### GETTERS ###

    def get_current_arrow_coordinates(self) -> Tuple[Optional[QPointF], Optional[QPointF]]:
        """Returns the coordinates for setting optimal positions"""
        red_position = None
        blue_position = None

        for arrow in self.arrows:
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position


    def get_state(self) -> List[Dict[str, Any]]:
        state = []
        for arrow in self.arrows:
            state.append(
                {
                    COLOR: arrow.color,
                    MOTION_TYPE: arrow.motion_type,
                    ROTATION_DIRECTION: arrow.rotation_direction,
                    QUADRANT: arrow.quadrant,
                    START_LOCATION: arrow.start_location,
                    END_LOCATION: arrow.end_location,
                    TURNS: arrow.turns,
                }
            )
        return state

    def get_current_letter_type(self) -> Optional[str]:
        if self.current_letter is not None:
            for letter_type, letters in letter_types.items():
                if self.current_letter in letters:
                    return letter_type
        else:
            return None

    def get_arrow_by_color(self, color: str) -> Optional[Arrow]:
        for arrow in self.arrows:
            if arrow.color == color:
                return arrow

    def get_quadrant(self, x: float, y: float) -> Optional[str]:
        if self.point_in_quadrant(x, y, self.quadrants[NORTHEAST]):
            return NORTHEAST
        elif self.point_in_quadrant(x, y, self.quadrants[SOUTHEAST]):
            return SOUTHEAST
        elif self.point_in_quadrant(x, y, self.quadrants[SOUTHWEST]):
            return SOUTHWEST
        elif self.point_in_quadrant(x, y, self.quadrants[NORTHWEST]):
            return NORTHWEST
        else:
            return None

    ### MANIPULATORS ###

    def swap_colors(self) -> None:
        if self.current_letter != "G" and self.current_letter != "H":
            if len(self.arrows) >= 1:
                for arrow in self.arrows:
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

                self.update()

    ### HELPERS ###

    @staticmethod
    def point_in_quadrant(x: float, y: float, boundary: Tuple[float, float, float, float]) -> bool:
        return boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]

    def create_blank_arrow(self, arrow: Arrow) -> None:
        deleted_arrow_attributes = arrow.attributes
        blank_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow_attributes[END_LOCATION],
            END_LOCATION: deleted_arrow_attributes[END_LOCATION],
            TURNS: 0,
        }
        blank_arrow = BlankArrow(self, blank_attributes_dict)
        self.addItem(blank_arrow)
        self.arrows.append(blank_arrow)
        blank_arrow.staff = arrow.staff
        blank_arrow.staff.arrow = blank_arrow

    def position_letter_item(self, letter_item: 'QGraphicsSvgItem'):
        x = self.grid.boundingRect().width() / 2 - letter_item.boundingRect().width() / 2
        y = self.grid.boundingRect().height() 
        letter_item.setPos(x, y)

    ### UPDATERS ###

    def update(self) -> None:
        self.update_letter()
        self.update_arrows()
        self.update_staffs()
        self.update_infobox()

    def update_infobox(self) -> None:
        self.infobox.update()

    def update_arrows(self) -> None:
        self.arrow_positioner.update()

    def update_staffs(self) -> None:
        self.staff_positioner.update()

    def update_letter(self) -> None:
        if len(self.staffs) == 2:
            self.current_letter = self.letter_engine.get_current_letter()
        else:
            self.current_letter = None
        self.update_letter_item(self.current_letter)
        self.position_letter_item(self.letter_item)

    def update_letter_item(self, letter: str) -> None:
        if letter:
            self.set_letter_renderer(letter)
        else:
            self.letter_item.setSharedRenderer(QSvgRenderer(f"{LETTER_SVG_DIR}/blank.svg"))

    ### SETTERS ###

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)
    
