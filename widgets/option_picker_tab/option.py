from constants.string_constants import (
    ANTI,
    BLUE,
    COLOR,
    DASH,
    MOTION_TYPE,
    PRO,
    RED,
    STATIC,
    TURNS,
    END_LOCATION,
    IN,
    PROP_TYPE,
    LOCATION,
    ORIENTATION,
)
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING, Dict, Literal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

import os
from PyQt6.QtGui import QImage, QPainter

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker_tab.option_picker_scroll import OptionPickerScroll
from PyQt6.QtCore import pyqtSignal


class Option(Pictograph):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INIT ###

    def __init__(
        self, main_widget: "MainWidget", option_picker: "OptionPickerScroll"
    ) -> None:
        self.view: "OptionView" = None
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.option_picker = option_picker
        self.imageLoaded = False
        self.pixmapItem = None  # Store the pixmap item
        self.pd_row_data = None  # Store the row data from the pandas dataframe

    ### SETUP ###

    def _add_motion(self, motion_dict: Dict) -> None:
        arrow = self._create_arrow(motion_dict)
        prop = self._create_prop(motion_dict)
        self._setup_motion_relations(arrow, prop)

    def _setup_motion_relations(self, arrow: Arrow, prop: Prop) -> None:
        motion = self.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = self.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    def _finalize_setup(self, motion_dict) -> None:
        for motion in self.motions.values():
            if motion.color == motion_dict[COLOR]:
                motion.setup_attributes(motion_dict)
                motion.arrow = self.arrows[motion.color]
                motion.prop = self.props[motion.color]
                motion.assign_location_to_arrow()
                motion.update_prop_orientation()
                motion.arrow.set_is_svg_mirrored_from_attributes()
                motion.arrow.update_mirror()
                motion.arrow.update_appearance()
                motion.prop.update_appearance()
                motion.arrow.motion = motion
                motion.prop.motion = motion
                motion.arrow.ghost = self.ghost_arrows[motion.color]
                motion.arrow.ghost.motion = motion
                motion.arrow.ghost.set_is_svg_mirrored_from_attributes()
                motion.arrow.ghost.update_appearance()
                motion.arrow.ghost.update_mirror()

        if motion_dict[COLOR] == BLUE:
            self.motions[BLUE].setup_attributes(motion_dict)
        elif motion_dict[COLOR] == RED:
            self.motions[RED].setup_attributes(motion_dict)

        self.motions[BLUE].end_orientation = self.motions[BLUE].get_end_orientation()
        self.motions[RED].end_orientation = self.motions[RED].get_end_orientation()

        self.arrows[RED].motion = self.motions[RED]
        self.arrows[BLUE].motion = self.motions[BLUE]

    ### IMAGE LOADING ###

    def loadImage(self, image_path: str) -> None:
        """Load image from the path."""
        # Lazy loading: Only load the image if it's not already loaded and the view is visible
        if not self.imageLoaded and self.view.isVisible():
            # Caching: Check if the image is already cached
            cached_pixmap = self.option_picker.get_cached_pixmap(image_path)
            if cached_pixmap:
                pixmap = cached_pixmap
            else:
                pixmap = QPixmap(image_path)
                self.option_picker.cache_pixmap(image_path, pixmap)

            # Pixmap Item Reuse: Update existing pixmap item if it exists, otherwise create a new one
            if not self.pixmapItem:
                self.pixmapItem = QGraphicsPixmapItem(pixmap)
                self.addItem(self.pixmapItem)
            else:
                self.pixmapItem.setPixmap(pixmap)

            self.imageLoaded = True

    def render_and_cache_image(self) -> None:
        # Render the scene into an image and store it in the cache
        image_path = self.option_picker.generate_image_path_for_option(self)
        pixmap = self.render_scene_to_pixmap()
        self.option_picker.cache_pixmap(image_path, pixmap)
        self.pixmapItem = QGraphicsPixmapItem(pixmap)
        self.addItem(self.pixmapItem)
        self.imageLoaded = True

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
        turns_folder = f"({blue_motion_type_prefix}{self.motions[BLUE].turns},{red_motion_type_prefix}{self.motions[RED].turns})"

        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            letter,
            prop_type,
            turns_folder,
        )
        os.makedirs(image_dir, exist_ok=True)

        # Modify the filename to include motion types and turns
        image_name = (
            f"{letter}_{self.start_position}_{self.end_position}_"
            f"{self.motions[BLUE].motion_type[:1]}{self.motions[BLUE].turns}_"
            f"{self.motions[BLUE].start_orientation}_"
            f"{self.motions[BLUE].end_orientation}_"
            f"{self.motions[RED].motion_type[:1]}{self.motions[RED].turns}_"
            f"{self.motions[RED].start_orientation}_"
            f"{self.motions[RED].end_orientation}_"
            f"{prop_type}.png"
        )

        image_path = os.path.join(image_dir, image_name)
        image = QImage(
            int(self.width()),
            int(self.height()),
            QImage.Format.Format_ARGB32,
        )
        painter = QPainter(image)
        self.render(painter)
        painter.end()

        # Save the image
        try:
            image.save(image_path)
            self.imageGenerated.emit(image_path)
        except Exception as e:
            print(f"Failed to save image: {e}")

    ### CREATE ###

    def _create_motion_dict(self, row_data, color: str) -> Dict:
        return {
            "color": color,
            "motion_type": row_data[f"{color}_motion_type"],
            "rotation_direction": row_data[f"{color}_rotation_direction"],
            "start_location": row_data[f"{color}_start_location"],
            "end_location": row_data[f"{color}_end_location"],
            "turns": row_data[f"{color}_turns"],
            "start_orientation": row_data[f"{color}_start_orientation"],
        }

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

    ### EVENTS ###

    def wheelEvent(self, event) -> None:
        return super().wheelEvent(event)


class OptionView(QGraphicsView):
    def __init__(self, option: "Option") -> None:
        super().__init__(option)
        self.option = option

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.option)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_option_view(self) -> None:
        view_width = int(
            self.option.option_picker.width() / 4
        ) - self.option.option_picker.spacing * (
            self.option.option_picker.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event):
        self.option.option_picker.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.option.option_picker.load_image_if_visible(self.option)

    def showEvent(self, event):
        super().showEvent(event)
        # Trigger image rendering and loading when the view becomes visible
        if not self.option.imageLoaded:
            self.option.render_and_cache_image()
