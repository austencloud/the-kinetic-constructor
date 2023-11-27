from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from objects.letter_item import LetterItem
from data.letter_engine_data import letter_types
from objects.arrow import Arrow, BlankArrow
from objects.grid import Grid
from objects.props.staff import Staff
from objects.motion import Motion
from settings.string_constants import (
    BLUE,
    COLOR,
    END_LOCATION,
    LETTER_SVG_DIR,
    MOTION_TYPE,
    NORTHEAST,
    NORTHWEST,
    QUADRANT,
    RED,
    ROTATION_DIRECTION,
    SOUTHEAST,
    SOUTHWEST,
    START_LOCATION,
    STATIC,
    TURNS,
    START_ORIENTATION,
    END_ORIENTATION,
    START_LAYER,
    END_LAYER,
)
from utilities.letter_engine import LetterEngine
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
    Layer,
    MotionAttributesDicts,
    List,
    Optional,
    Orientation,
    Tuple,
    Quadrant,
)
from widgets.graph_editor.pictograph.pictograph_view import PictographView
from widgets.graph_editor.pictograph.pictogaph_init import PictographInit
from widgets.graph_editor.pictograph.pictograph_menu_handler import (
    PictographMenuHandler,
)
from widgets.graph_editor.pictograph.position_engines.arrow_positioner import (
    ArrowPositioner,
)
from widgets.graph_editor.pictograph.position_engines.staff_positioner import (
    StaffPositioner,
)

if TYPE_CHECKING:
    from utilities.pictograph_generator import PictographGenerator
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


class Pictograph(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graph_editor = graph_editor
        self.setup_scene()
        self.setup_components(main_widget)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 750, 900)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.arrows: List[Arrow] = []
        self.staffs: List[Staff] = []
        self.motions: List[Motion] = []
        self.current_letter: str = None

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.letters = main_widget.letters
        self.generator: PictographGenerator = None

        self.dragged_arrow: Arrow = None
        self.dragged_staff: Staff = None
        self.initializer = PictographInit(self)

        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.ghost_staffs = self.initializer.init_ghost_staffs()
        self.grid = self.initializer.init_grid()
        self.view: PictographView = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.letter_item = self.initializer.init_letter_item()
        self.quadrants = self.initializer.init_quadrants(self.grid)

        # set the icons to 80% of the button size

        self.setup_managers(main_widget)

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    def setup_managers(self, main_widget: "MainWidget") -> None:
        self.pictograph_menu_handler = PictographMenuHandler(main_widget, self)
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
        self.pictograph_menu_handler.create_master_menu(event_pos, clicked_item)

    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        items_at_pos = self.items(scene_pos)

        # Collect all Arrow items at the click position
        arrows_at_pos = [item for item in items_at_pos if isinstance(item, Arrow)]

        # Find the closest arrow to the cursor position
        closest_arrow = None
        min_distance = float("inf")
        for arrow in arrows_at_pos:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance

        # If the closest item is an arrow, select it
        if closest_arrow:
            self.dragged_arrow = closest_arrow
            self.dragged_arrow.mousePressEvent(event)
        else:
            # Handle other items (Staff, LetterItem, Grid) or no item
            clicked_item = self.itemAt(scene_pos, QTransform())
            self.handle_non_arrow_click(clicked_item, event)

    def handle_non_arrow_click(self, clicked_item, event):
        if isinstance(clicked_item, Staff):
            self.dragged_staff = clicked_item
            self.dragged_staff.mousePressEvent(event)
        elif isinstance(clicked_item, LetterItem):
            clicked_item.setSelected(False)
            self.clear_selections()
        elif not clicked_item or isinstance(clicked_item, Grid):
            self.clear_selections()

    def mouseMoveEvent(self, event) -> None:
        if self.dragged_staff:
            self.dragged_staff.mouseMoveEvent(event)
        elif self.dragged_arrow:
            self.dragged_arrow.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.dragged_staff:
            self.dragged_staff.mouseReleaseEvent(event)
            self.dragged_staff = None
        elif self.dragged_arrow:
            self.dragged_arrow.mouseReleaseEvent(event)
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

    def get_state(self) -> List[MotionAttributesDicts]:
        state = []
        for motion in self.motions:
            state.append(
                {
                    COLOR: motion.color,
                    MOTION_TYPE: motion.motion_type,
                    ROTATION_DIRECTION: motion.rotation_direction,
                    QUADRANT: motion.quadrant,
                    START_LOCATION: motion.start_location,
                    END_LOCATION: motion.end_location,
                    TURNS: motion.turns,
                    START_LOCATION: motion.start_location,
                    END_LOCATION: motion.end_location,
                    START_ORIENTATION: motion.start_orientation,
                    END_ORIENTATION: motion.end_orientation,
                    START_LAYER: motion.start_layer,
                    END_LAYER: motion.end_layer,
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

    def get_motion_by_color(self, color: str) -> Optional[Motion]:
        for motion in self.motions:
            if motion.color == color:
                return motion

    def get_staff_by_color(self, color: str) -> Optional[Staff]:
        for staff in self.staff_set.values():
            if staff.color == color:
                return staff

    def get_quadrant(self, x: float, y: float) -> Quadrant:
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
            TURNS: deleted_arrow.turns,
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
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for arrow in self.arrows:
            arrow.rotate(direction)

    def clear_pictograph(self) -> None:
        for arrow in self.arrows:
            self.removeItem(arrow)
        for staff in self.staffs:
            self.removeItem(staff)
        self.arrows = []
        self.staffs = []
        self.update()

    def clear_selections(self):
        for arrow in self.arrows:
            arrow.setSelected(False)
        for staff in self.staffs:
            staff.setSelected(False)
        self.dragged_staff = None
        self.dragged_arrow = None


    def add_motion(
        self,
        arrow: Arrow,
        staff,
        start_orientation: Orientation,
        start_layer: Layer,
    ) -> None:
        motion_attributes: MotionAttributesDicts = {
            COLOR: arrow.color,
            MOTION_TYPE: arrow.motion_type,
            ROTATION_DIRECTION: arrow.rotation_direction,
            QUADRANT: arrow.quadrant,
            START_LOCATION: arrow.start_location,
            END_LOCATION: arrow.end_location,
            TURNS: arrow.turns,
            START_ORIENTATION: start_orientation,
            START_LAYER: start_layer,
        }

        motion = Motion(self, arrow, staff, motion_attributes)

        for m in self.motions:
            if m.color == motion.color:
                self.motions.remove(m)

        self.motions.append(motion)

    ### UPDATERS ###

    def update(self) -> None:
        self.update_letter()
        self.update_arrows()
        self.update_staffs()
        self.update_attr_panel()

    def update_attr_panel(self) -> None:
        self.graph_editor.attr_panel.update_attr_panel()

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
