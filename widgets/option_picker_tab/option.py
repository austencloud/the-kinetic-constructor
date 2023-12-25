import os
from typing import TYPE_CHECKING, Literal
from PyQt6.QtCore import Qt, QEvent, QByteArray, QBuffer, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from Enums import *
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING
from objects.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker_tab.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )


class Option(Pictograph):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INIT ###

    def __init__(
        self, main_widget: "MainWidget", option_picker_scroll: "OptionPickerScrollArea"
    ) -> None:
        self.view: "OptionView" = None
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.option_picker_scroll = option_picker_scroll
        self.imageLoaded = False
        self.pixmapItem = None  # Store the pixmap item
        self.pd_row_data = None  # Store the row data from the pandas dataframe

    ### SETUP ###

    ### IMAGE LOADING ###

    def loadImage(self, image_path: str) -> None:
        """Load image from the path."""
        # Lazy loading: Only load the image if it's not already loaded and the view is visible
        if not self.imageLoaded and self.view.isVisible():
            # Caching: Check if the image is already cached
            cached_pixmap = self.option_picker_scroll.get_cached_pixmap(image_path)
            if cached_pixmap:
                pixmap = cached_pixmap
            else:
                pixmap = QPixmap(image_path)
                self.option_picker_scroll.cache_pixmap(image_path, pixmap)

            # Pixmap Item Reuse: Update existing pixmap item if it exists, otherwise create a new one
            if not self.pixmapItem:
                self.pixmapItem = QGraphicsPixmapItem(pixmap)
                self.addItem(self.pixmapItem)
            else:
                self.pixmapItem.setPixmap(pixmap)

            self.imageLoaded = True

    def render_and_cache_image(self) -> None:
        # Generate the image path
        image_path = self.option_picker_scroll.generate_image_path_for_option(self)

        # Check if the image already exists in the cache or on the disk
        if image_path in self.option_picker_scroll.image_cache or os.path.exists(
            image_path
        ):
            # If the image is already cached or exists, load it
            print(f"Image already exists, using cached image for {image_path}")
            pixmap = QPixmap(image_path)
        else:
            # If the image doesn't exist, render the scene to a pixmap
            print(f"Rendering and saving image for {image_path}")
            pixmap = self.render_scene_to_pixmap()

            # Cache the pixmap
            self.option_picker_scroll.cache_pixmap(image_path, pixmap)

            # Save the image if it's not already saved
            image = QImage(pixmap.toImage())
            if not os.path.exists(image_path):
                image.save(image_path, "PNG")

        # Use the pixmap for the QGraphicsPixmapItem
        if not self.pixmapItem:
            self.pixmapItem = QGraphicsPixmapItem(pixmap)
            self.addItem(self.pixmapItem)
        else:
            self.pixmapItem.setPixmap(pixmap)

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
        blue_turns = self.motions[BLUE].turns
        red_turns = self.motions[RED].turns
        blue_end_orientation = self.motions[BLUE].end_orientation
        red_end_orientation = self.motions[RED].end_orientation

        image_name = (
            f"{letter}_"
            f"({self.start_position}→{self.end_position})_"
            f"({self.motions[BLUE].start_location}→{self.motions[BLUE].end_location}_"
            f"{blue_turns}_"
            f"{self.motions[BLUE].start_orientation}_{blue_end_orientation})_"
            f"({self.motions[RED].start_location}→{self.motions[RED].end_location}_"
            f"{red_turns}_"
            f"{self.motions[RED].start_orientation}_{red_end_orientation})_"
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
        if not self.imageLoaded:
            self.render_and_cache_image()

    ### FLAGS ###

    ### CREATE ###

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
            self.option.option_picker_scroll.width() / 4
        ) - self.option.option_picker_scroll.spacing * (
            self.option.option_picker_scroll.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event):
        self.option.option_picker_scroll.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False

    def showEvent(self, event):
        super().showEvent(event)
        # Ensure this slot is called after the event loop starts
        QTimer.singleShot(0, self.option.load_image_if_needed)
