from typing import TYPE_CHECKING
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtGui import QPainter, QPixmap, QPageSize, QPageLayout
from PyQt6.QtCore import QTemporaryFile, QIODevice, Qt, QPointF, QMarginsF
import tempfile
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsView,
    QDialog,
    QVBoxLayout,
)

from widgets.sequence_widget.SW_beat_frame.custom_print_dialog import (
    CustomPrintDialog,
)

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFramePrintManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.beat_frame_scene = QGraphicsScene()  # Using the custom scene class
        self.printer = None

    def _setup_printer(self):
        self.printer = QPrinter()
        self.printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        self.printer.setPageOrientation(QPageLayout.Orientation.Portrait)
        self.printer.setPageMargins(
            QMarginsF(15, 15, 15, 15), QPageLayout.Unit.Millimeter
        )

    def setup_scene(self):
        filled_beats = [beat for beat in self.beat_frame.beats if beat.is_filled]
        column_count, row_count = self._calculate_layout(len(filled_beats))

        max_x, max_y = 0, 0  # Track the furthest extents of items added to the scene
        for beat_index, beat_view in enumerate(filled_beats):
            pixmap: QPixmap = beat_view.grab()
            col = beat_index % column_count
            row = beat_index // column_count
            beat_size = int(self.beat_frame.start_pos_view.beat.width())
            x = col * beat_size
            y = row * beat_size

            item = QGraphicsPixmapItem(pixmap)
            item.setPos(x, y)
            self.beat_frame_scene.addItem(item)

            max_x = max(max_x, x + pixmap.width())
            max_y = max(max_y, y + pixmap.height())

        # Adjust the scene size to ensure it encompasses all items
        self.beat_frame_scene.setSceneRect(0, 0, max_x, max_y)

    def calculate_position(self, beat_view) -> QPointF:
        filled_beats = [beat for beat in self.beat_frame.beats if beat.is_filled]
        beat_index = filled_beats.index(
            beat_view
        )  # Ensure this is the index in filled_beats

        column_count, row_count = self._calculate_layout(len(filled_beats))
        beat_size = int(self.beat_frame.start_pos_view.beat.width())

        col = beat_index % column_count
        row = beat_index // column_count

        # Calculate x, y based on col and row position
        x = col * beat_size
        y = row * beat_size

        return QPointF(x, y)

    def _calculate_layout(self, filled_beat_count):
        # Use the layout logic from BeatFrameImageExportManager
        # Here, you could directly access the get_layout_options method or replicate its logic
        # For simplicity, I'm assuming you have access to that method here
        return self.beat_frame.export_manager._calculate_layout(filled_beat_count)

    def show_preview(self) -> None:
        view = QGraphicsView(self.beat_frame_scene)
        view.show()

    def print_sequence(self):

        self._setup_printer()

        self.setup_scene()

        print("Scene rect:", self.beat_frame_scene.sceneRect())
        self.pixmap = QPixmap(self.beat_frame_scene.sceneRect().size().toSize())
        self.pixmap.fill(Qt.GlobalColor.transparent)
        print_dialog = CustomPrintDialog(self.pixmap, self.beat_frame)

        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter(self.printer)
            painter.setRenderHints(
                QPainter.RenderHint.Antialiasing
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.SmoothPixmapTransform,
                on=True,
            )

            # Fit the scene rect to the printer page rect to make sure items are within the bounds
            rect = self.printer.pageRect(QPrinter.Unit.Point)
            self.beat_frame_scene.setSceneRect(rect)

            # Debug print to check the size of the page rect
            print("Page rect:", rect)

            # Render the scene onto the printer, ensure to pass the page rect
            self.beat_frame_scene.render(
                painter, rect, self.beat_frame_scene.sceneRect()
            )

            painter.end()

    def perform_print(self, pixmap: QPixmap, printer: QPrinter) -> None:
        # Set up the painter and print
        painter = QPainter(printer)

        # Start a new page and print contents
        printer.newPage()
        rect = printer.pageRect(QPrinter.Unit.Point)
        scale_factor = min(
            rect.width() / pixmap.width(), rect.height() / pixmap.height()
        )
        scaled_pixmap = pixmap.scaled(
            pixmap.size() * scale_factor, Qt.AspectRatioMode.KeepAspectRatio
        )
        x = (rect.width() - scaled_pixmap.width()) / 2
        y = (rect.height() - scaled_pixmap.height()) / 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()
