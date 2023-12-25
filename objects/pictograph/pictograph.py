from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple, Union
from PyQt6.QtCore import Qt, QPointF, QByteArray, QBuffer
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
import pandas as pd
from Enums import Color, Letter, LetterNumberType, Location, SpecificPosition
from constants.string_constants import *
from data.positions_map import get_specific_start_end_positions
from objects.letter_item import LetterItem
from objects.motion import Motion
from objects.prop.prop import Prop
from objects.arrow.arrow import Arrow
from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.pictograph.pictograph_event_handler import PictographEventHandler
from objects.pictograph.pictograph_init import PictographInit
from objects.pictograph.pictograph_menu_handler import PictographMenuHandler
from objects.pictograph.position_engines.arrow_positioners.arrow_positioner import (
    ArrowPositioner,
)
from objects.pictograph.position_engines.prop_positioner import PropPositioner
from utilities.letter_engine import LetterEngine

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_pictograph import IGPictograph
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
            "start_position_beat",
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
        self.arrows: Dict[Color, Arrow] = {}
        self.props: Dict[Color, Prop] = {}
        self.ghost_arrows: Dict[Color, GhostArrow] = {}
        self.ghost_props: Dict[Color, GhostProp] = {}
        self.motions: Dict[Color, Motion] = {}
        self.current_letter: Letter = None
        self.pictograph_dict: Dict = {}
        self.motion_dict_list: List[Dict] = []
        self.start_position: SpecificPosition = None
        self.end_position: SpecificPosition = None
        self.image_loaded: bool = False
        self.pixmap = None  # Store the pixmap item
        self.pd_row_data = None  # Store the row data from the pandas dataframe
        self.view_scale = 1
        self.event_handler = PictographEventHandler(self)

        self.dragged_arrow: Arrow = None
        self.dragged_prop: Prop = None
        self.initializer = PictographInit(self)

        self.arrow_turns = 0

        self.grid: Grid = self.initializer.init_grid()
        self.locations: Dict[
            Location, Tuple[int, int, int, int]
        ] = self.initializer.init_locations(self.grid)

        self.motions: Dict[Color, Motion] = self.initializer.init_motions()
        self.arrows, self.ghost_arrows = self.initializer.init_arrows()
        self.props, self.ghost_props = self.initializer.init_props(
            self.main_widget.prop_type
        )

        self.view = self.init_view(self.graph_type)
        self.letter_item: LetterItem = self.initializer.init_letter_item()

        self.setup_managers(main_widget)

    def init_view(self, graph_type) -> QGraphicsView:
        from widgets.graph_editor_tab.main_pictograph_view import MainPictographView
        from widgets.option_picker_tab.option import OptionView
        from widgets.sequence_widget.beat_frame.start_position import (
            StartPositionBeatView,
        )
        from widgets.sequence_widget.beat_frame.beat import BeatView
        from widgets.image_generator_tab.ig_pictograph import IG_Pictograph_View

        if graph_type == MAIN:
            view = MainPictographView(self)
        elif graph_type == OPTION:
            view = OptionView(self)
        elif graph_type == BEAT:
            view = BeatView(self)
        elif graph_type == START_POSITION_BEAT:
            view = StartPositionBeatView(self)
        elif graph_type == IG_PICTOGRAPH:
            view = IG_Pictograph_View(self)
        return view

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_letter_type(letter)
        svg_path = f"resources/images/letters_trimmed/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    def setup_managers(self, main_widget: "MainWidget") -> None:
        self.pictograph_menu_handler = PictographMenuHandler(main_widget, self)
        self.arrow_positioner = ArrowPositioner(self)
        self.prop_positioner = PropPositioner(self)
        self.letter_engine = LetterEngine(self)

    def _finalize_motion_setup(self, pd_row_data, filters) -> None:
        self.pd_row_data = pd_row_data

        red_motion_dict = self._create_motion_dict_from_pd_row_data(
            pd_row_data, BLUE, filters
        )

        blue_motion_dict = self._create_motion_dict_from_pd_row_data(
            pd_row_data, RED, filters
        )

        self._add_motion(red_motion_dict)
        self._add_motion(blue_motion_dict)

    def _add_motion(self, motion_dict: Dict) -> None:
        arrow = self._create_arrow(motion_dict)
        prop = self._create_prop(motion_dict)
        motion = self.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = self.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    def _create_prop(self, motion_dict: Dict) -> Prop:
        prop_dict = {
            COLOR: motion_dict[COLOR],
            PROP_TYPE: self.main_widget.prop_type,
            LOCATION: motion_dict[END_LOCATION],
            ORIENTATION: IN,
        }
        prop = Prop(self, prop_dict, self.motions[motion_dict[COLOR]])
        self.props[prop.color] = prop
        prop.motion = self.motions[prop.color]
        self.addItem(prop)
        return prop

    def _create_arrow(self, motion_dict: Dict) -> Arrow:
        arrow_dict = {
            COLOR: motion_dict[COLOR],
            MOTION_TYPE: motion_dict[MOTION_TYPE],
            TURNS: motion_dict[TURNS],
        }
        arrow = Arrow(self, arrow_dict, self.motions[motion_dict[COLOR]])
        self.arrows[arrow.color] = arrow
        arrow.motion = self.motions[arrow.color]
        self.addItem(arrow)
        return arrow

    def _create_motion_dict_from_pd_row_data(
        self: Union["Option", "IGPictograph"],
        pd_row_data: pd.Series,
        color: str,
        filters,
    ) -> Dict:
        return {
            COLOR: color,
            MOTION_TYPE: pd_row_data[f"{color}_motion_type"],
            ROTATION_DIRECTION: pd_row_data[f"{color}_rotation_direction"],
            START_LOCATION: pd_row_data[f"{color}_start_location"],
            END_LOCATION: pd_row_data[f"{color}_end_location"],
            TURNS: filters[f"{color}_turns"],
            START_ORIENTATION: pd_row_data[f"{color}_start_orientation"],
        }

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

    def get_current_arrow_coordinates(
        self,
    ) -> Tuple[Optional[QPointF], Optional[QPointF]]:
        red_position = None
        blue_position = None

        for arrow in self.arrows.values():
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position

    def get_start_end_positions(self) -> Optional[SpecificPosition]:
        specific_positions = get_specific_start_end_positions(
            self.motions[RED], self.motions[BLUE]
        )
        if specific_positions:
            start_position = specific_positions[START_POSITION]
            end_position = specific_positions[END_POSITION]
        return start_position, end_position

    def get_state(self) -> Dict:
        start_position, end_position = self.get_start_end_positions()
        state_data = {
            LETTER: self.current_letter,
            START_POSITION: start_position,
            END_POSITION: end_position,
        }

        for color, motion in self.motions.items():
            prefix = f"{color}_"
            state_data.update(
                {
                    prefix + MOTION_TYPE: motion.motion_type,
                    prefix + ROTATION_DIRECTION: motion.rotation_direction,
                    prefix + START_LOCATION: motion.start_location,
                    prefix + END_LOCATION: motion.end_location,
                    prefix + TURNS: motion.turns,
                    prefix + START_ORIENTATION: motion.start_orientation,
                    prefix + END_ORIENTATION: motion.end_orientation,
                }
            )

        return state_data

    def get_letter_type(self, letter: Letter) -> Optional[str]:
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

        if self.grid.grid_mode == DIAMOND:
            for name, point in self.grid.diamond_hand_points.items():
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

    ### HELPERS ###

    def add_to_sequence_callback(self) -> None:
        new_beat = self.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for arrow in self.arrows.values():
            arrow.manipulator.rotate_arrow(direction)

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
        self.update_letter()

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    ### UPDATERS ###

    def update_attr_panel(self) -> None:
        for motion in self.motions.values():
            self.main_widget.graph_editor_tab.graph_editor.attr_panel.update_attr_panel(
                motion
            )

    def update_pictograph(self) -> None:
        self.update_letter()
        self.update_arrows()
        self.update_props()
        if self.graph_type == MAIN:
            self.update_attr_panel()

    def update_arrows(self) -> None:
        self.arrow_positioner.update_arrow_positions()

    def update_props(self) -> None:
        self.prop_positioner.update_prop_positions()

    def update_letter(self) -> None:
        if all(motion.motion_type for motion in self.motions.values()):
            self.current_letter = self.letter_engine.get_current_letter()
            self.set_letter_renderer(self.current_letter)
            self.letter_item.position_letter_item(self.letter_item)
        else:
            self.current_letter = None
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

            if new_arrow.location:
                new_arrow.update_appearance()
                new_ghost_arrow.update_appearance()

            if new_prop.location:
                new_prop.update_appearance()
                new_ghost_prop.update_appearance()

            new_arrow.ghost = new_ghost_arrow
            new_prop.ghost = new_ghost_prop

            new_arrow.motion = new_beat.motions[motion.color]
            new_prop.motion = new_beat.motions[motion.color]
            new_ghost_arrow.motion = new_beat.motions[motion.color]
            new_ghost_prop.motion = new_beat.motions[motion.color]

            new_beat.addItem(new_arrow)
            new_beat.addItem(new_prop)
            new_beat.addItem(new_ghost_arrow)
            new_beat.addItem(new_ghost_prop)

            new_ghost_arrow.hide()
            new_ghost_prop.hide()

            motion_dict = self.motions[motion.color].get_attributes()
            motion_dict[ARROW] = new_arrow
            motion_dict[PROP] = new_prop
            motion_dict[MOTION_TYPE] = new_arrow.motion_type
            new_arrow.turns = motion_dict[TURNS]
            new_arrow.motion.setup_attributes(motion_dict)

            new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())
            new_arrow.ghost.setTransformOriginPoint(
                new_arrow.ghost.boundingRect().center()
            )
            svg_file = new_arrow.get_svg_file(new_arrow.motion_type, new_arrow.turns)
            new_arrow.update_svg(svg_file)
            new_arrow.ghost.update_svg(svg_file)
            new_arrow.update_appearance()
            new_arrow.ghost.update_appearance()
        new_beat.update_pictograph()

        return new_beat

    def meets_turn_criteria(self, filters):
        blue_turns = self.motions[BLUE].turns
        red_turns = self.motions[RED].turns
        return blue_turns in filters[BLUE_TURNS] and red_turns in filters[RED_TURNS]

    def render_and_cache_image(self) -> None:
        # Generate the image path
        image_path = self.main_widget.generate_image_path(self)

        # Check if the image already exists in the cache
        if image_path in self.main_widget.image_cache:
            # If the image is already cached, use it
            pixmap = self.main_widget.get_cached_pixmap(image_path)
            if pixmap is None:
                # If the pixmap is not loaded yet, load it
                pixmap = QPixmap(image_path)
                self.main_widget.cache_image(image_path, pixmap)
            print(f"Using cached image for {image_path}")
        else:
            # If the image doesn't exist, render the scene to a pixmap
            print(f"Rendering and saving image for {image_path}")
            pixmap = self.render_scene_to_pixmap()
            
            # Cache the pixmap
            self.main_widget.cache_image(image_path, pixmap)

            # Save the image if it's not already saved
            if not os.path.exists(image_path):
                pixmap.save(image_path, "PNG")

        # Use the pixmap for the QGraphicsPixmapItem
        self.update_pixmap_item(pixmap)



    def update_pixmap_item(self, pixmap: QPixmap) -> None:
        if not self.pixmap:
            self.pixmap = QGraphicsPixmapItem(pixmap)
            self.addItem(self.pixmap)
        else:
            self.pixmap.setPixmap(pixmap)
        self.image_loaded = True

    def render_scene_to_pixmap(self) -> None:
        self.update_pictograph()

        prop_type = self.main_widget.prop_type
        letter = self.current_letter

        if self.motions[BLUE].motion_type == PRO:
            blue_motion_type_prefix = "p"
        elif self.motions[BLUE].motion_type == ANTI:
            blue_motion_type_prefix = "a"
        elif self.motions[BLUE].motion_type == STATIC:
            blue_motion_type_prefix = "s"
        elif self.motions[BLUE].motion_type == DASH:
            blue_motion_type_prefix = "d"

        if self.motions[RED].motion_type == PRO:
            red_motion_type_prefix = "p"
        elif self.motions[RED].motion_type == ANTI:
            red_motion_type_prefix = "a"
        elif self.motions[RED].motion_type == STATIC:
            red_motion_type_prefix = "s"
        elif self.motions[RED].motion_type == DASH:
            red_motion_type_prefix = "d"

        # Construct the folder name based on turns and motion types
        turns_string = f"({blue_motion_type_prefix}{self.motions[BLUE].turns},{red_motion_type_prefix}{self.motions[RED].turns})"
        start_to_end_string = f"({self.start_position}→{self.end_position})"
        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            prop_type,
            letter,
            start_to_end_string,
            turns_string,
            
        )
        os.makedirs(image_dir, exist_ok=True)

        # Modify the filename to include motion types and turns
        blue_turns = self.motions[BLUE].turns
        red_turns = self.motions[RED].turns
        blue_end_orientation = self.motions[BLUE].end_orientation
        red_end_orientation = self.motions[RED].end_orientation

        image_name = (
            f"{letter}_"
            f"{start_to_end_string}_"
            f"({self.motions[BLUE].start_location}→{self.motions[BLUE].end_location}_"
            f"{blue_turns}_"
            f"{self.motions[BLUE].start_orientation}→{blue_end_orientation})_"
            f"({self.motions[RED].start_location}→{self.motions[RED].end_location}_"
            f"{red_turns}_"
            f"{self.motions[RED].start_orientation}→{red_end_orientation})_"
            f"{prop_type}.png "
        )

        image_path = os.path.join(image_dir, image_name)
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
                with open(image_path, "wb") as file:
                    file.write(buffer)
                print(f"Image saved successfully to {image_path}")
            else:
                print(f"Failed to save the image to {image_path}")
        else:
            print("QImage is null. Nothing to save.")

        return QPixmap.fromImage(image)

    # New method to handle conditional image loading
    def load_image_if_needed(self) -> None:
        if not self.image_loaded:
            self.render_and_cache_image()
