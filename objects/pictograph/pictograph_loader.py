import queue
import threading
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from constants import IG_PICTOGRAPH
from utilities.TypeChecking.letter_lists import all_letters

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class PictographLoader(QObject):
    pictograph_ready = pyqtSignal(str)

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

    def start_loading(self) -> None:
        self.pictograph_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.load_thread = QThread()
        self.load_thread.started.connect(self.load_pictographs)
        self.load_thread.finished.connect(self.load_thread.deleteLater)
        self.stopped = False
        self.order_number = 0

        # Queue initial pictographs before starting the thread
        self.main_widget.pictograph_factory.queue_initial_pictographs()

        # Now you can start the thread
        self.load_thread.start()

    def load_pictographs(self) -> None:
        for letter in all_letters:
            pictograph_dicts = self.main_widget.ig_tab.scroll_area.letters.get(
                letter, []
            )
            try:
                for pictograph_dict in pictograph_dicts:
                    pictograph_key = self.main_widget.pictograph_factory.generate_pictograph_key_from_dict(
                        pictograph_dict
                    )
                    if pictograph_key not in self.main_widget.all_pictographs:
                        self.main_widget.all_pictographs[pictograph_key.split("_")[0]][
                            pictograph_key
                        ] = self.main_widget.pictograph_factory.create_pictograph(
                            IG_PICTOGRAPH
                        )
                        self.main_widget.all_pictographs[pictograph_key.split("_")[0]][
                            pictograph_key
                        ].state_updater.update_pictograph(pictograph_dict)
                        print (f"Loaded {pictograph_key}")
            except queue.Empty:
                continue

    def stop(self) -> None:
        self.stopped = True
        self.load_thread.quit()
        self.load_thread.wait()

    def queue_pictograph(self, pictograph_key) -> None:
        self.pictograph_queue.put((self.order_number, pictograph_key))
        self.order_number += 1

    def prioritize_pictograph(self, pictograph_key) -> None:
        self.pictograph_queue.put((0, pictograph_key))

    def reset_priority(self) -> None:
        self.order_number = 0

    def bump_up_priority_for_specific_letter(self, letter) -> None:
        for i in range(self.pictograph_queue.qsize()):
            order_number, pictograph_key = self.pictograph_queue.get()
            if pictograph_key.split("_")[0] == letter:
                self.pictograph_queue.put((0, pictograph_key))
            else:
                self.pictograph_queue.put((order_number, pictograph_key))

    def generate_pictographs_for_specific_letter(
        self, letter
    ) -> None:
        print (f"Generating pictographs for {letter}")
        for i in range(self.pictograph_queue.qsize()):
            order_number, pictograph_key = self.pictograph_queue.get()
            if pictograph_key.split("_")[0] == letter:
                self.main_widget.pictograph_factory.get_or_create_pictograph(
                    pictograph_key
                )
            else:
                self.pictograph_queue.put((order_number, pictograph_key))