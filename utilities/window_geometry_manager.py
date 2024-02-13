from typing import TYPE_CHECKING
from PyQt6.QtGui import QGuiApplication

if TYPE_CHECKING:
    from main import MainWindow


class WindowGeometryManager:
    def __init__(self, window: "MainWindow") -> None:
        self.window = window

    def set_dimensions(self) -> None:
        screens = QGuiApplication.screens()
        # screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        screen = QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()
        device_pixel_ratio = screen.devicePixelRatio()

        # add the device pixel ratio to the available geometry
        # available_geometry.setWidth(
        #     int(available_geometry.width() // device_pixel_ratio)
        # )
        # available_geometry.setHeight(
        #     int(available_geometry.height() // device_pixel_ratio)
        # )

        # Adjusting dimensions based on the device pixel ratio
        window_width = int((available_geometry.width() * 0.9))
        window_height = int((available_geometry.height() * 0.9))
        x = available_geometry.x() + int(
            ((available_geometry.width() - window_width) / 2)
        )
        y = available_geometry.y() + int(
            ((available_geometry.height() - window_height) / 2)
        )

        self.window.setGeometry(x, y, window_width, window_height)
