from typing import TYPE_CHECKING
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtCore import QByteArray, QBuffer
import os

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsPixmapItem


class PictographImageRenderer:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def render_and_cache_image(self) -> None:
        image_path = self.pictograph.main_widget.generate_image_path(self.pictograph)
        if os.path.isfile(image_path):
            pixmap = self.pictograph.main_widget.get_cached_pixmap(image_path)
            if pixmap is None:
                pixmap = QPixmap(image_path)
                self.pictograph.main_widget.cache_image(image_path, pixmap)
            print(f"Using cached image for {image_path}")
        else:
            pixmap = self._render_scene_to_pixmap()
            self.pictograph.main_widget.cache_image(image_path, pixmap)
            if not os.path.exists(image_path):
                pixmap.save(image_path, "PNG")
        self._update_thumbnail(pixmap)

    def _update_thumbnail(self, pixmap: QPixmap) -> None:
        if not self.pictograph.pixmap:
            self.pictograph.pixmap = QGraphicsPixmapItem(pixmap)
            self.pictograph.addItem(self.pictograph.pixmap)
        else:
            self.pictograph.pixmap.setPixmap(pixmap)
        self.pictograph.image_loaded = True

    def _render_scene_to_pixmap(self) -> QPixmap:
        self.pictograph.updater.update_pictograph(self.pictograph.pictograph_dict)

        prop_type = self.pictograph.main_widget.prop_type
        letter = self.pictograph.letter
        letter_type = self.pictograph.get.letter_type(letter)

        basic_turns_string = (
            f"{self.pictograph.blue_motion.turns},"
            f"{self.pictograph.red_motion.turns}"
        )
        start_to_end_string = f"{self.pictograph.start_pos}→{self.pictograph.end_pos}"
        image_dir = os.path.join(
            "images",
            "pictographs",
            prop_type,
            basic_turns_string,
            letter_type,
            letter,
            start_to_end_string,
        )
        os.makedirs(image_dir, exist_ok=True)

        blue_turns = self.pictograph.blue_motion.turns
        red_turns = self.pictograph.red_motion.turns
        blue_end_ori = self.pictograph.blue_motion.end_ori
        red_end_ori = self.pictograph.red_motion.end_ori

        image_name = (
            f"{letter}_"
            f"({start_to_end_string})_"
            f"({self.pictograph.blue_motion.motion_type}_{self.pictograph.blue_motion.start_loc}"
            f"→{self.pictograph.blue_motion.end_loc}_{blue_turns}_"
            f"{self.pictograph.blue_motion.start_ori}→{blue_end_ori})_"
            f"({self.pictograph.red_motion.motion_type}_{self.pictograph.red_motion.start_loc}"
            f"→{self.pictograph.red_motion.end_loc}_{red_turns}_"
            f"{self.pictograph.red_motion.start_ori}→{red_end_ori})_"
            f"{prop_type}.png"
        )

        image_path = os.path.join(image_dir, image_name).replace("\\", "/")
        image = QImage(
            int(self.pictograph.width()),
            int(self.pictograph.height()),
            QImage.Format.Format_ARGB32,
        )
        painter = QPainter(image)
        self.pictograph.render(painter)
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
        if not self.pictograph.image_loaded:
            self.render_and_cache_image()
