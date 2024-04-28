import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtGui import QImage
from PIL import Image, PngImagePlugin
import numpy as np

from path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from widgets.sequence_widget.add_to_dictionary_manager import AddToDictionaryManager


class ThumbnailGenerator:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.manager = add_to_dictionary_manager
        self.sequence_widget = add_to_dictionary_manager.sequence_widget
        self.beat_frame = self.sequence_widget.beat_frame
        self.export_manager = self.beat_frame.export_manager

    def generate_and_save_thumbnail(
        self, sequence, turn_pattern, structural_variation_number=None
    ):
        beat_frame_image = self.export_manager.create_beat_frame_image_for_printing()
        pil_image = self.qimage_to_pil(beat_frame_image)
        metadata = json.dumps(sequence)
        info = self._create_png_info(metadata)
        master_dir = self._construct_master_directory(
            sequence, structural_variation_number
        )
        image_filename = self._create_image_filename(
            sequence, structural_variation_number, turn_pattern
        )
        image_path = os.path.join(master_dir, image_filename)
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

    def _construct_master_directory(self, sequence, structural_variation_number) -> str:
        base_word = self.manager.get_base_word(sequence)
        base_dir = get_images_and_data_path(f"dictionary/{base_word}")
        master_dir = os.path.join(
            base_dir, f"{base_word}_v{structural_variation_number}"
        )
        os.makedirs(master_dir, exist_ok=True)
        return master_dir

    def _create_image_filename(
        self, sequence, structural_variation_number, turn_pattern
    ):
        base_word = self.manager.get_base_word(sequence)
        return f"{base_word}_v{structural_variation_number}_{turn_pattern}.png"

    def _save_image(
        self, pil_image: Image.Image, image_path: str, info: PngImagePlugin.PngInfo
    ):
        pil_image.save(image_path, "PNG", pnginfo=info)
