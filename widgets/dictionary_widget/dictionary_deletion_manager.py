import os
import shutil
from typing import TYPE_CHECKING

from path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryDeletionManager:
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        self.dictionary_widget = dictionary_widget

    def delete_variation(self, thumbnail_box: "ThumbnailBox", index):
        file_path = thumbnail_box.thumbnails.pop(index)
        os.remove(file_path)
        if len(thumbnail_box.thumbnails) == 0:
            self.delete_word(thumbnail_box.base_word)
            self.dictionary_widget.preview_area.current_index = index
            self.dictionary_widget.preview_area.update_preview(None)
            self.dictionary_widget.preview_area.variation_number_label.setText(
                f"Variation {index + 1}"
            )
        else:
            self.dictionary_widget.browser.scroll_widget.load_base_words()
        # update the preview area's labels

    def delete_word(self, base_word):
        base_path = os.path.join(get_images_and_data_path("dictionary"), base_word)
        shutil.rmtree(base_path)
        self.dictionary_widget.browser.scroll_widget.load_base_words()
