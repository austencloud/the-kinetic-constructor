from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from PyQt6.QtCore import QPointF
from objects.arrow import Arrow, BlankArrow
from objects.staff import Staff
from widgets.graphboard.graphboard_init import GraphBoardInit
from widgets.graphboard.graphboard_menu_handler import GraphBoardMenuHandler
from widgets.graphboard.position_engines.staff_positioner import StaffPositioner
from widgets.graphboard.position_engines.arrow_positioner import ArrowPositioner
from utilities.letter_engine import LetterEngine
from settings.string_constants import (
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    RED,
    BLUE,
    LETTER_SVG_DIR,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHEAST,
    STATIC,
)
from data.letter_engine_data import letter_types
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    TYPE_CHECKING,
    List,
    Optional,
    Tuple,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.infobox.infobox import InfoBox
    from utilities.pictograph_generator import PictographGenerator


class GraphBoard(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.setup_scene()
        self.setup_components(main_widget)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 750, 900)
        self.arrows: List[Arrow] = []
        self.staffs: List[Staff] = []
        self.current_letter: str = None
        self.infobox: InfoBox = None

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.letters = main_widget.letters
        self.generator: PictographGenerator = None

        self.dragged_arrow: Arrow = None
        self.dragged_staff: Staff = None
        self.initializer = GraphBoardInit(self)

        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.ghost_staffs = self.initializer.init_ghost_staffs()
        self.grid = self.initializer.init_grid()
        self.view = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.letter_item = self.initializer.init_letter_item()
        self.quadrants = self.initializer.init_quadrants(self.grid)

        self.setup_managers(main_widget)

    def setup_managers(self, main_widget: "MainWidget") -> None:
        self.graphboard_menu_handler = GraphBoardMenuHandler(main_widget, self)
        self.arrow_positioner = ArrowPositioner(self)
        self.staff_positioner = StaffPositioner(self)
        self.letter_engine = LetterEngine(self)

    ### EVENTS ###

    def contextMenuEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene_pos = self.view.mapToScene(event.pos().toPoint())
        items_at_pos = self.items(scene_pos)

        clicked_item = None
        for item in items_at_pos:
            if isinstance(item, Arrow) or isinstance(item, Staff):
                clicked_item = item
                break

        if not clicked_item and items_at_pos:
            clicked_item = items_at_pos[0]

        event_pos = event.screenPos()
        self.graphboard_menu_handler.create_master_menu(event_pos, clicked_item)

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

    def get_current_arrow_coordinates(
        self,
    ) -> Tuple[Optional[QPointF], Optional[QPointF]]:
        red_position = None
        blue_position = None

        for arrow in self.arrows:
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position

    def get_state(self) -> List[ArrowAttributesDicts]:
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

    def get_staff_by_color(self, color: str) -> Optional[Staff]:
        for staff in self.staff_set.values():
            if staff.color == color:
                return staff

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


    ### HELPERS ###

    @staticmethod
    def point_in_quadrant(
        x: float, y: float, boundary: Tuple[float, float, float, float]
    ) -> bool:
        return boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]

    def create_blank_arrow(self, deleted_arrow: Arrow) -> None:
        blank_attributes_dict = {
            COLOR: deleted_arrow.color,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow.end_location,
            END_LOCATION: deleted_arrow.end_location,
            TURNS: deleted_arrow.turns
        }
        blank_arrow = BlankArrow(self, blank_attributes_dict)
        self.addItem(blank_arrow)
        self.arrows.append(blank_arrow)
        blank_arrow.staff = deleted_arrow.staff
        blank_arrow.staff.arrow = blank_arrow

    def position_letter_item(self, letter_item: "QGraphicsSvgItem") -> None:
        x = (
            self.grid.boundingRect().width() / 2
            - letter_item.boundingRect().width() / 2
        )
        y = self.grid.boundingRect().height()
        letter_item.setPos(x, y)

    def add_to_sequence(self) -> None:
        pass

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
            self.letter_item.setSharedRenderer(
                QSvgRenderer(f"{LETTER_SVG_DIR}/blank.svg")
            )

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)
