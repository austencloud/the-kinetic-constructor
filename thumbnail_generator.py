import json
import os
from PyQt6.QtGui import QImage, QPainter
from PIL import Image, PngImagePlugin
import numpy as np
from path_helpers import get_app_data_path, get_images_and_data_path, get_my_photos_path
from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_Beat_Frame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.add_to_dictionary_manager import AddToDictionaryManager


class ThumbnailGenerator:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.manager = add_to_dictionary_manager
        self.sequence_widget = add_to_dictionary_manager.sequence_widget
        self.beat_frame = self.sequence_widget.beat_frame

    def generate_and_save_thumbnail(self, sequence, turn_pattern, structural_variation_number=None):
        offscreen_frame = self._get_offscreen_frame(turn_pattern)
        qimage = self._render_offscreen_frame(offscreen_frame, sequence)
        pil_image = self._qimage_to_pil(qimage)
        metadata = json.dumps(sequence)
        info = self._create_png_info(metadata)
        master_dir = self._construct_master_directory(sequence, structural_variation_number)
        image_filename = self._create_image_filename(sequence, structural_variation_number, turn_pattern)
        image_path = os.path.join(master_dir, image_filename)
        self._save_image(pil_image, image_path, info)
        return image_path

    def _get_offscreen_frame(self, turn_pattern):
        if turn_pattern == "current":
            return self.beat_frame
        else:
            return SW_Beat_Frame(self.sequence_widget)

    def _render_offscreen_frame(self, offscreen_frame: "SW_Beat_Frame", sequence):
        offscreen_frame.set_sequence(sequence)
        offscreen_frame.resize(self.sequence_widget.size())
        qimage = QImage(offscreen_frame.size(), QImage.Format.Format_ARGB32)
        painter = QPainter(qimage)
        offscreen_frame.render(painter)
        painter.end()
        return qimage

    def _qimage_to_pil(self, qimage: "QImage"):
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, copy=False).reshape((height, width, 4))
        arr = arr[..., [2, 1, 0, 3]]  # Adjust for RGB
        return Image.fromarray(arr, "RGBA")

    def _create_png_info(self, metadata:  str):
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", metadata.encode("utf-8"))
        return info

    def _construct_master_directory(self, sequence, structural_variation_number):
        base_pattern = self.manager.get_base_word(sequence)
        base_dir = get_images_and_data_path(f"thumbnails/{base_pattern}")
        if structural_variation_number is None:
            structural_variation_number = 1
            master_dir = os.path.join(base_dir, f"{base_pattern}_v{structural_variation_number}")
            while os.path.exists(master_dir):
                structural_variation_number += 1
                master_dir = os.path.join(base_dir, f"{base_pattern}_v{structural_variation_number}")
        else:
            master_dir = os.path.join(base_dir, f"{base_pattern}_v{structural_variation_number}")

        os.makedirs(master_dir, exist_ok=True)
        return master_dir

    def _create_image_filename(self, sequence, structural_variation_number, turn_pattern):
        base_pattern = self.manager.get_base_word(sequence)
        return f"{base_pattern}_v{structural_variation_number}_{turn_pattern}.png"

    def _save_image(self, pil_image, image_path, info):
        pil_image.save(image_path, "PNG", pnginfo=info)

    def qimage_to_pil(self, qimage: "QImage") -> Image.Image:
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, copy=False).reshape((height, width, 4))
        arr = arr[..., [2, 1, 0, 3]]  # Adjust for RGB
        return Image.fromarray(arr, "RGBA")

    def construct_master_directory(self, base_pattern, master_version):
        base_dir = get_images_and_data_path(f"thumbnails/{base_pattern}")
        if master_version is None:
            master_version = 1
            master_dir = os.path.join(base_dir, f"{base_pattern}_v{master_version}")
            while os.path.exists(master_dir):
                master_version += 1
                master_dir = os.path.join(base_dir, f"{base_pattern}_v{master_version}")
        else:
            master_dir = os.path.join(base_dir, f"{base_pattern}_v{master_version}")

        os.makedirs(master_dir, exist_ok=True)
        return master_dir

    def get_base_word(self, sequence):
        return "".join([beat.get("letter", "") for beat in sequence])
