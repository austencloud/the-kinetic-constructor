from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple, Union
from PyQt6.QtCore import Qt, QPointF, QByteArray, QBuffer
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from Enums import LetterNumberType

from constants import *

from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
    MainArrowPlacementManager,
)
from utilities.TypeChecking.prop_types import (
    strictly_placed_props,
    non_strictly_placed_props,
)
from utilities.TypeChecking.Letters import Letters
from utilities.TypeChecking.TypeChecking import Colors, Locations, SpecificPositions

from utilities.letter_item import LetterItem
from ..motion.motion import Motion
from ..prop.prop import Prop
from ..arrow.arrow import Arrow
from ..arrow.ghost_arrow import GhostArrow
from ..prop.ghost_prop import GhostProp
from ..grid import Grid

from objects.pictograph.pictograph_event_handler import PictographEventHandler
from objects.pictograph.pictograph_init import PictographInit
from objects.pictograph.pictograph_menu_handler import PictographMenuHandler
from objects.pictograph.position_engines.prop_positioners.main_prop_positioner import (
    MainPropPlacementManager,
)
from utilities.letter_engine import LetterEngine
from data.rules import beta_ending_letters, alpha_ending_letters, gamma_ending_letters

if TYPE_CHECKING:
    from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
    from widgets.option_picker_tab.option import Option
    from widgets.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    def __init__(
        self,
        main_widget: "MainWidget",
        graph_type: Literal[
            "main",
            "option",
            "beat",
            "start_pos_beat",
            "ig_pictograph",
        ],
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graph_type = graph_type

        self.setup_scene()
        self.setup_components(main_widget)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 950, 950)
        self.setBackgroundBrush(Qt.GlobalColor.white)

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.arrows: Dict[Colors, Arrow] = {}
        self.props: Dict[Colors, Prop] = {}
        self.ghost_arrows: Dict[Colors, GhostArrow] = {}
        self.ghost_props: Dict[Colors, GhostProp] = {}
        self.motions: Dict[Colors, Motion] = {}
        self.letter: Letters = None
        self.pictograph_dict: Dict = {}
        self.motion_dict_list: List[Dict] = []
        self.start_pos: SpecificPositions = None
        self.end_pos: SpecificPositions = None
        self.image_loaded: bool = False
        self.pixmap = None
        self.pictograph_dict = None
        self.view_scale = 1
        self.event_handler = PictographEventHandler(self)

        self.dragged_arrow: Arrow = None
        self.dragged_prop: Prop = None
        self.initializer = PictographInit(self)

        self.arrow_turns = 0

        self.grid: Grid = self.initializer.init_grid()
        self.locations: Dict[
            Locations, Tuple[int, int, int, int]
        ] = self.initializer.init_quadrant_boundaries(self.grid)

        self.motions: Dict[Colors, Motion] = self.initializer.init_motions()
        self.arrows, self.ghost_arrows = self.initializer.init_arrows()
        self.props, self.ghost_props = self.initializer.init_props(
            self.main_widget.prop_type
        )

        self.view = self._init_view(self.graph_type)
        self.letter_item: LetterItem = self.initializer.init_letter_item()

        self.red_motion = self.motions[RED]
        self.blue_motion = self.motions[BLUE]
        self.red_arrow = self.arrows[RED]
        self.blue_arrow = self.arrows[BLUE]

        self._setup_managers(main_widget)

    def _init_view(self, graph_type) -> QGraphicsView:
        from widgets.graph_editor_tab.graph_editor_pictograph_view import (
            GraphEditorPictographView,
        )
        from widgets.option_picker_tab.option import OptionView
        from widgets.sequence_widget.beat_frame.start_pos_beat import (
            StartPositionBeatView,
        )
        from widgets.sequence_widget.beat_frame.beat import BeatView
        from widgets.ig_tab.ig_scroll.ig_pictograph import IG_Pictograph_View

        if graph_type == MAIN:
            view = GraphEditorPictographView(self)
        elif graph_type == OPTION:
            view = OptionView(self)
        elif graph_type == BEAT:
            view = BeatView(self)
        elif graph_type == START_POS_BEAT:
            view = StartPositionBeatView(self)
        elif graph_type == IG_PICTOGRAPH:
            view = IG_Pictograph_View(self)
        return view

    def _set_letter_renderer(self, letter: str) -> None:
        letter_type = self._get_letter_type(letter)
        svg_path = f"resources/images/letters_trimmed/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    def _setup_managers(self, main_widget: "MainWidget") -> None:
        self.pictograph_menu_handler = PictographMenuHandler(main_widget, self)
        self.arrow_placement_manager = MainArrowPlacementManager(self)
        self.prop_placement_manager = MainPropPlacementManager(self)
        self.letter_engine = LetterEngine(self)

    def _create_motion_dict(
        self: Union["Option", "IGPictograph"], pictograph_dict: Dict, color: Colors
    ) -> Dict:
        motion_dict = {
            COLOR: color,
            MOTION_TYPE: pictograph_dict.get(f"{color}_motion_type"),
            PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
            START_LOC: pictograph_dict.get(f"{color}_start_loc"),
            END_LOC: pictograph_dict.get(f"{color}_end_loc"),
            TURNS: pictograph_dict.get(f"{color}_turns"),
            START_ORI: pictograph_dict.get(f"{color}_start_ori"),
        }
        return {k: v for k, v in motion_dict.items() if v != None}

    ### EVENT HANDLERS ###

    def mousePressEvent(self, event) -> None:
        self.main_widget.deselect_all_except(self)
        self.event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event) -> None:
        self.event_handler.handle_context_menu(event)

    ### GETTERS ###

    def _get_letter_type(self, letter: Letters) -> Optional[str]:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return letter_type.description
        return None

    def get_closest_hand_point(
        self, pos: QPointF
    ) -> Tuple[Optional[str], Optional[QPointF]]:
        min_distance = float("inf")
        nearest_point_name = None
        nearest_point_coords = None
        if self.main_widget.prop_type in strictly_placed_props:
            strict = True
        elif self.main_widget.prop_type in non_strictly_placed_props:
            strict = False
        if self.grid.grid_mode == DIAMOND:
            if strict is True:
                for name, point in self.grid.circle_coordinates_cache["hand_points"][
                    self.grid.grid_mode
                ]["strict"].items():
                    distance = (pos - point).manhattanLength()
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point_name = name
                        nearest_point_coords = point
            elif strict is False:
                for name, point in self.grid.circle_coordinates_cache["hand_points"][
                    self.grid.grid_mode
                ]["normal"].items():
                    distance = (pos - point).manhattanLength()
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point_name = name
                        nearest_point_coords = point

        elif self.grid.grid_mode == BOX:
            for name, point in self.grid.box_hand_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        return nearest_point_name, nearest_point_coords

    def get_closest_layer2_point(
        self, pos: QPointF
    ) -> Tuple[Optional[str], Optional[QPointF]]:
        min_distance = float("inf")
        nearest_point_name = None
        nearest_point_coords = None

        if self.grid.grid_mode == DIAMOND:
            for name, point in self.grid.diamond_layer2_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        elif self.grid.grid_mode == BOX:
            for name, point in self.grid.box_layer2_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        return nearest_point_name, nearest_point_coords

    def get_motions_by_type(self, motion_type: str) -> List[Motion]:
        return [
            motion
            for motion in self.motions.values()
            if motion.motion_type == motion_type
        ]

    def get_leading_motion(self) -> Motion:
        if self.red_motion.start_loc == self.blue_motion.end_loc:
            return self.red_motion
        elif self.blue_motion.start_loc == self.red_motion.end_loc:
            return self.blue_motion

    ### HELPERS ###

    def select_arrow(self, arrow):
        self.selected_arrow: Arrow = arrow

    def add_to_sequence_callback(self) -> None:
        new_beat = self.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for motion in self.motions.values():
            motion.manipulator.rotate_motion(direction)

    def clear_pictograph(self) -> None:
        for motion in self.motions.values():
            motion.clear_attributes()
        for arrow in self.arrows.values():
            arrow.clear_attributes()
        for prop in self.props.values():
            prop.clear_attributes()
        for ghost_arrow in self.ghost_arrows.values():
            ghost_arrow.clear_attributes()
        for ghost_prop in self.ghost_props.values():
            ghost_prop.clear_attributes()
        for item in self.items():
            if isinstance(item, Arrow) or isinstance(item, Prop):
                self.removeItem(item)
        self._update_letter()

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    ### UPDATERS ###

    def update_attributes(self, pictograph_dict: Dict) -> None:
        for attr_name, attr_value in pictograph_dict.items():
            setattr(self, attr_name, attr_value)

    def is_complete(self, pictograph_dict: Dict) -> bool:
        required_keys = [
            "letter",
            "start_pos",
            "end_pos",
            "blue_motion_type",
            "blue_prop_rot_dir",
            "blue_start_loc",
            "blue_end_loc",
            "blue_start_ori",
            "blue_turns",
            "red_motion_type",
            "red_prop_rot_dir",
            "red_start_loc",
            "red_end_loc",
            "red_start_ori",
            "red_turns",
        ]
        return all(key in pictograph_dict for key in required_keys)

    def update_pictograph(self, pictograph_dict: Dict = None) -> None:
        self._update_letter()
        if pictograph_dict:
            if self.is_complete(pictograph_dict):
                self.pictograph_dict = pictograph_dict
            self._update_from_pictograph_dict(pictograph_dict)
        self._position_objects()

        if self.graph_type == MAIN:
            self._update_attr_panel()

    def _update_from_pictograph_dict(self, pictograph_dict):
        self.update_attributes(pictograph_dict)
        motion_dicts = []
        for color in [BLUE, RED]:
            motion_dict = self._create_motion_dict(pictograph_dict, color)
            motion_dicts.append(motion_dict)
            if MOTION_TYPE in motion_dict:
                self.motions[color].motion_type = motion_dict[MOTION_TYPE]
            if PROP_ROT_DIR in motion_dict:
                self.motions[color].prop_rot_dir = motion_dict[PROP_ROT_DIR]
            if START_ORI in motion_dict:
                self.motions[color].start_ori = motion_dict[START_ORI]
            if START_LOC in motion_dict and END_LOC in motion_dict:
                if motion_dict[COLOR] == BLUE:
                    self.blue_motion.start_loc = motion_dict[START_LOC]
                    self.blue_motion.end_loc = motion_dict[END_LOC]
                elif motion_dict[COLOR] == RED:
                    self.red_motion.start_loc = motion_dict[START_LOC]
                    self.red_motion.end_loc = motion_dict[END_LOC]
            if pictograph_dict.get(f"{color}_motion_type"):
                arrow_dict = {
                    MOTION_TYPE: pictograph_dict.get(f"{color}_motion_type"),
                    TURNS: pictograph_dict.get(f"{color}_turns"),
                }

                self.motions[color].arrow.setup_arrow(arrow_dict)
                self.ghost_arrows[color].setup_arrow(arrow_dict)
                self.motions[color].arrow.show()
                prop_dict = {
                    PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
                    ORI: self.motions[color].get_end_ori(),
                }
                self.motions[color].prop.update_attributes(prop_dict)
                self.ghost_props[color].update_attributes(prop_dict)
                self.motions[color].prop.show()
                self.motions[color].prop.update_prop()

        self._update_motions()

    def _update_attr_panel(self) -> None:
        for motion in self.motions.values():
            self.main_widget.graph_editor_tab.graph_editor.attr_panel.update_attr_panel(
                motion
            )

    def _position_objects(self) -> None:
        self.prop_placement_manager.position_props()
        self.arrow_placement_manager.update_arrow_placement()

    def _update_motions(self) -> None:
        for motion in self.motions.values():
            motion.update_motion()

    def _update_letter(self) -> None:
        if all(motion.motion_type for motion in self.motions.values()):
            self.letter = self.letter_engine.get_current_letter()
            self.letter_item.letter = self.letter
            self._set_letter_renderer(self.letter)
            self.letter_item.position_letter_item(self.letter_item)
        else:
            self.letter = None
            svg_path = f"resources/images/letter_button_icons/blank.svg"
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.letter_item.setSharedRenderer(renderer)

    def create_new_beat(self) -> QGraphicsScene:
        from widgets.sequence_widget.beat_frame.beat import Beat

        new_beat = Beat(self.main_widget)
        new_beat.setSceneRect(self.sceneRect())
        for motion in self.motions.values():
            new_beat.motions[motion.color] = Motion(new_beat, motion.get_attributes())
            new_arrow = Arrow(
                new_beat, motion.arrow.get_attributes(), new_beat.motions[motion.color]
            )

            new_prop = Prop(
                new_beat, motion.prop.get_attributes(), new_beat.motions[motion.color]
            )

            new_ghost_arrow = GhostArrow(
                new_beat, motion.arrow.get_attributes(), new_beat.motions[motion.color]
            )

            new_ghost_prop = GhostProp(
                new_beat, motion.prop.get_attributes(), new_beat.motions[motion.color]
            )

            new_beat.arrows[new_arrow.color] = new_arrow
            new_beat.props[new_prop.color] = new_prop

            new_beat.motions[motion.color].arrow = new_arrow
            new_beat.motions[motion.color].prop = new_prop
            new_beat.motions[motion.color].arrow.ghost = new_ghost_arrow
            new_beat.motions[motion.color].prop.ghost = new_ghost_prop

            new_beat.arrows[motion.color] = new_arrow
            new_beat.props[motion.color] = new_prop
            new_beat.ghost_arrows[motion.color] = new_ghost_arrow
            new_beat.ghost_props[motion.color] = new_ghost_prop

            if new_arrow.loc:
                new_arrow.update_arrow()
                new_ghost_arrow.update_arrow()

            if new_prop.loc:
                new_prop.update_prop()
                new_ghost_prop.update_prop()

            new_arrow.ghost = new_ghost_arrow
            new_prop.ghost = new_ghost_prop

            new_arrow.motion = new_beat.motions[motion.color]
            new_prop.motion = new_beat.motions[motion.color]
            new_ghost_arrow.motion = new_beat.motions[motion.color]
            new_ghost_prop.motion = new_beat.motions[motion.color]

            new_ghost_arrow.hide()
            new_ghost_prop.hide()

            motion_dict = self.motions[motion.color].get_attributes()
            motion_dict[ARROW] = new_arrow
            motion_dict[PROP] = new_prop
            motion_dict[MOTION_TYPE] = new_arrow.motion_type
            new_arrow.turns = motion_dict[TURNS]
            new_arrow.motion.update_motion(motion_dict)

            new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())
            new_arrow.ghost.setTransformOriginPoint(
                new_arrow.ghost.boundingRect().center()
            )
            new_arrow.update_arrow()
        new_beat.update_pictograph()

        return new_beat

    def _meets_criteria(self, filters):
        blue_turns = str(self.motions[BLUE].turns)
        red_turns = str(self.motions[RED].turns)
        return blue_turns in filters[BLUE_TURNS] and red_turns in filters[RED_TURNS]

    def render_and_cache_image(self) -> None:
        image_path = self.main_widget.generate_image_path(self)
        if os.path.isfile(image_path):
            # If the image is already cached, use it
            pixmap = self.main_widget.get_cached_pixmap(image_path)
            if pixmap is None:
                # If the pixmap is not loaded yet, load it
                pixmap = QPixmap(image_path)
                self.main_widget.cache_image(image_path, pixmap)
            print(f"Using cached image for {image_path}")
        else:
            pixmap = self._render_scene_to_pixmap()
            self.main_widget.cache_image(image_path, pixmap)
            if not os.path.exists(image_path):
                pixmap.save(image_path, "PNG")

        self._update_thumbnail(pixmap)

    def _update_thumbnail(self, pixmap: QPixmap) -> None:
        if not self.pixmap:
            self.pixmap = QGraphicsPixmapItem(pixmap)
            self.addItem(self.pixmap)
        else:
            self.pixmap.setPixmap(pixmap)
        self.image_loaded = True

    def _render_scene_to_pixmap(self) -> None:
        self.update_pictograph(self.pictograph_dict)

        prop_type = self.main_widget.prop_type
        letter = self.letter
        letter_type = self._get_letter_type(letter)

        blue_motion_type_prefix = self.motions[BLUE].motion_type[0]
        red_motion_type_prefix = self.motions[RED].motion_type[0]
        turns_string = f"{blue_motion_type_prefix}{self.motions[BLUE].turns},{red_motion_type_prefix}{self.motions[RED].turns}"

        # Construct the folder name based on turns and motion types
        basic_turns_string = f"{self.motions[BLUE].turns},{self.motions[RED].turns}"
        start_to_end_string = f"{self.start_pos}→{self.end_pos}"
        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            prop_type,
            basic_turns_string,
            letter_type,
            letter,
            start_to_end_string,
        )
        os.makedirs(image_dir, exist_ok=True)

        # Modify the filename to include motion types and turns
        blue_turns = self.motions[BLUE].turns
        red_turns = self.motions[RED].turns
        blue_end_ori = self.motions[BLUE].end_ori
        red_end_ori = self.motions[RED].end_ori

        image_name = (
            f"{letter}_"
            f"({start_to_end_string})_"
            f"({self.motions[BLUE].motion_type}_{self.motions[BLUE].start_loc}→{self.motions[BLUE].end_loc}_"
            f"{blue_turns}_"
            f"{self.motions[BLUE].start_ori}→{blue_end_ori})_"
            f"({self.motions[RED].motion_type}_{self.motions[RED].start_loc}→{self.motions[RED].end_loc}_"
            f"{red_turns}_"
            f"{self.motions[RED].start_ori}→{red_end_ori})_"
            f"{prop_type}.png"
        )

        image_path = os.path.join(image_dir, image_name).replace("\\", "/")
        image = QImage(
            int(self.width()), int(self.height()), QImage.Format.Format_ARGB32
        )
        painter = QPainter(image)
        self.render(painter)
        painter.end()

        if not image.isNull():
            buffer = QByteArray()
            buf = QBuffer(buffer)
            buf.open(QBuffer.OpenModeFlag.WriteOnly)
            success = image.save(buf, "PNG")
            buf.close()

            if success:
                with open(image_path, "w", encoding="utf-8") as file:
                    file.write(buffer.decode("utf-8"))
                print(f"Image saved successfully to {image_path}")
            else:
                print(f"Failed to save the image to {image_path}")
        else:
            print("QImage is null. Nothing to save.")

        return QPixmap.fromImage(image)

    def load_image_if_needed(self) -> None:
        if not self.image_loaded:
            self.render_and_cache_image()

    ### FLAGS ###

    def has_props_in_beta(self) -> bool | None:
        return self.letter in beta_ending_letters

    def has_props_in_alpha(self) -> bool | None:
        return self.letter in alpha_ending_letters

    def has_props_in_gamma(self) -> bool | None:
        return self.letter in gamma_ending_letters

    def has_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.props[RED], self.props[BLUE]
        return red_prop.is_radial() != blue_prop.is_radial()

    def has_non_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.props[RED], self.props[BLUE]
        return (red_prop.is_radial() == blue_prop.is_radial()) or (
            red_prop.is_antiradial() and blue_prop.is_antiradial()
        )

    def has_all_radial_props(self) -> bool:
        return all(prop.is_radial() for prop in self.props.values())

    def has_all_antiradial_props(self) -> bool:
        return all(prop.is_antiradial() for prop in self.props.values())
