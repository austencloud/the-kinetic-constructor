from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QColor, QLinearGradient
from PyQt6.QtWidgets import QWidget

from .snowflake_worker import SnowflakeWorker

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from PyQt6.QtGui import QPaintEvent


class SnowfallBackground(QWidget):
    snowflake_count = 100
    update_required = pyqtSignal()  # Signal for requesting an update

    def __init__(self, main_widget: "MainWidget" = None):
        super().__init__(main_widget)
        self.main_widget = main_widget
        # Dimensions and properties

        self.widget_width = self.main_widget.width()
        self.widget_height = self.main_widget.height()
        self.setFixedSize(self.widget_width, self.widget_height)
        self.setAutoFillBackground(True)

        # Snowflake properties
        self.snowflake_images = [
            QPixmap(f"images/snowflakes/snowflake{i}.png") for i in range(1, 21)
        ]  # Preload 20 snowflake images
        self.snowflakes = []
        # Worker thread setup
        self.worker_thread = QThread()
        self.worker = SnowflakeWorker(
            self.snowflake_count,
            self.widget_width,
            self.widget_height,
            len(self.snowflake_images),
        )
        self.worker.moveToThread(self.worker_thread)
        self.worker.update_snowflakes.connect(self._update_snowflakes_from_worker)
        self.worker_thread.started.connect(self.worker.process)

        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update)

    def start_animation(self):
        """Start the background animation."""
        self.worker.running = True
        self.worker_thread.start()
        self.animation_timer.start(16)  # Approximately 60 FPS

    def stop_animation(self):
        """Stop the background animation."""
        self.worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.animation_timer.stop()

    def closeEvent(self, event):
        """Stop the worker thread and timer when the widget is closed."""
        self.stop_animation()
        super().closeEvent(event)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    #     for snowflake in self.snowflakes:
    #         x, y, image_index = snowflake["x"], snowflake["y"], snowflake["image_index"]
    #         pixmap = self.snowflake_images[image_index]
    #         painter.drawPixmap(int(x), int(y), pixmap)  # Use coordinates directly

    @pyqtSlot(list)
    def _update_snowflakes_from_worker(self, snowflakes):
        """Slot to receive updated snowflake positions from the worker."""
        self.snowflakes = snowflakes
        self.update_required.emit()

    def resizeEvent(self, event):
        """Handle resizing of the widget and update worker bounds."""

        def update_bounds():
            self.widget_width = self.main_widget.width()
            self.widget_height = self.main_widget.height()
            print(
                f"Updated bounds: width={self.widget_width}, height={self.widget_height}"
            )
            self.worker.update_bounds(self.widget_width, self.widget_height)

        QTimer.singleShot(0, update_bounds)
        super().resizeEvent(event)

    def paint_background(self, parent_widget: QWidget, painter: QPainter):
        """Paint the gradient background and snowflakes using the parent widget."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gradient Background
        gradient = QLinearGradient(0, 0, 0, self.widget_height)
        gradient.setColorAt(0, QColor(20, 30, 48))  # Dark blue
        gradient.setColorAt(1, QColor(50, 80, 120))  # Light blue
        painter.fillRect(self.main_widget.rect(), gradient)

        # Draw Snowflakes
        for snowflake in self.snowflakes:
            x, y, image_index = snowflake["x"], snowflake["y"], snowflake["image_index"]
            pixmap = self.snowflake_images[image_index]
            painter.drawPixmap(int(x), int(y), pixmap)

    def paintEvent(self, event: Optional["QPaintEvent"]):
        """Handle painting of the background and snowflakes."""
        painter = QPainter(self)
        self.paint_background(self, painter)
        painter.end()
