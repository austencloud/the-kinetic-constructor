import queue
import threading
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea
    from widgets.pictograph_scroll_area.scroll_area_pictograph_factory import (
        PictographFactory,
    )


class PictographLoader(QObject):
    pictograph_ready = pyqtSignal(str)  # Signal to notify when a pictograph is ready

    def __init__(self, scroll_area: "ScrollArea") -> None:
        super().__init__()
        self.pictograph_factory = scroll_area.pictograph_factory
        # Use PriorityQueue for loading pictographs, priority is given by the order number

    def start_loading(self) -> None:
        self.pictograph_queue = queue.PriorityQueue()
        self.load_thread = threading.Thread(target=self.load_pictographs)
        self.load_thread.daemon = True  # Ensure thread closes with the program
        self.stopped = False
        self.order_number = 0  # To keep track of the order of pictographs added

        # Call this method after the main event loop has started
        self.load_thread.start()

    def load_pictographs(self) -> None:
        while not self.stopped:
            try:
                # Get the next pictograph to load, with priority
                _, pictograph_key = self.pictograph_queue.get(
                    timeout=3
                )  # 3 seconds timeout
                ig_pictograph = self.pictograph_factory.get_or_create_pictograph(
                    pictograph_key
                )
                self.pictograph_ready.emit(pictograph_key)  # Emit signal to main thread
            except queue.Empty:
                # No pictographs to load, continue the loop
                # You can also check for a shutdown signal here and break the loop if needed
                pass

    def stop(self) -> None:
        self.stopped = True
        self.load_thread.join()

    def queue_pictograph(self, pictograph_key) -> None:
        # All pictographs get added with increasing order numbers, ensuring FIFO without priority
        self.pictograph_queue.put((self.order_number, pictograph_key))
        self.order_number += 1

    def prioritize_pictograph(self, pictograph_key) -> None:
        # Whenever a pictograph needs to be prioritized, it is added with the highest priority (lowest number)
        self.pictograph_queue.put((0, pictograph_key))

    def reset_priority(self) -> None:
        # In case you need to reset priority when a user action dictates so
        self.order_number = 0
