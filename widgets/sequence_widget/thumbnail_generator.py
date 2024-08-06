import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtGui import QImage
from PIL import Image, PngImagePlugin
import numpy as np
from datetime import datetime


if TYPE_CHECKING:
    from widgets.sequence_widget.add_to_dictionary_manager import AddToDictionaryManager


class ThumbnailGenerator:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.manager = add_to_dictionary_manager
        self.sequence_widget = add_to_dictionary_manager.sequence_widget
        self.beat_frame = self.sequence_widget.beat_frame
        self.export_manager = self.beat_frame.export_manager

    def generate_and_save_thumbnail(
        self, sequence, turn_pattern, structural_variation_number, directory
    ):
        beat_frame_image = self.export_manager.image_creator.create_sequence_image(
            sequence, include_start_pos=False
        )
        pil_image = self.qimage_to_pil(beat_frame_image)
        metadata = {
            "sequence": sequence,
            "date_added": datetime.now().isoformat()
        }
        metadata_str = json.dumps(metadata)
        info = self._create_png_info(metadata_str)
        image_filename = self._create_image_filename(
            sequence, structural_variation_number, turn_pattern
        )
        image_path = os.path.join(directory, image_filename)
        self._save_image(pil_image, image_path, info)
        return image_path

    def qimage_to_pil(self, qimage: QImage) -> Image.Image:
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, copy=False).reshape((height, width, 4))
        arr = arr[..., [2, 1, 0, 3]]  # Adjust for RGB
        return Image.fromarray(arr, "RGBA")

    def _create_png_info(self, metadata: str) -> PngImagePlugin.PngInfo:
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", metadata.encode("utf-8"))
        return info

    def _create_image_filename(
        self, sequence, structural_variation_number, turn_pattern
    ):
        base_word = self.manager.sequence_widget.beat_frame.get_current_word()
        return f"{base_word}_ver{structural_variation_number}_({turn_pattern}).png"

    def _save_image(
        self, pil_image: Image.Image, image_path: str, info: PngImagePlugin.PngInfo
    ):
        pil_image.save(image_path, "PNG", pnginfo=info)
