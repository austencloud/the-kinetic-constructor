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

from widgets.sequence_widget.sequence_widget_beat_frame.custom_print_dialog import (
    CustomPrintDialog,
)

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFramePrintManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.scene = QGraphicsScene()
        self._setup_printer()

    def _setup_printer(self):
        self.printer = QPrinter()
        self.printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        self.printer.setPageOrientation(QPageLayout.Orientation.Portrait)
        self.printer.setPageMargins(
            QMarginsF(15, 15, 15, 15), QPageLayout.Unit.Millimeter
        )

    def setup_scene(self) -> None:
        # Assuming you have a method to get the pixmaps and positions for each beat
        for beat_view in self.beat_frame.beat_views:
            if beat_view.is_filled:
                pixmap = beat_view.grab()  # Grab the pixmap of the beat view
                # Calculate the position where it should be placed in the scene
                pos = self.calculate_position(beat_view)
                item = QGraphicsPixmapItem(pixmap)
                item.setPos(pos)
                self.scene.addItem(item)

    def calculate_position(self, beat_view) -> QPointF:
        filled_beats = [beat for beat in self.beat_frame.beat_views if beat.is_filled]
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

    def _calculate_layout(self, filled_beat_count) -> tuple[int, int]:
        """
        Determines the layout for the beats in the printing preview.
        """
        export_manager = self.beat_frame.export_manager
        layout_options = export_manager.get_layout_options()

        if filled_beat_count in layout_options:
            return layout_options[filled_beat_count]
        else:
            column_count = min(filled_beat_count, self.beat_frame.COLUMN_COUNT)
            row_count = (filled_beat_count + column_count - 1) // column_count
            return column_count, row_count

    def show_preview(self) -> None:
        view = QGraphicsView(self.scene)
        view.show()

    def print_sequence(self):
        self.setup_scene()

        # Debug print to check the size of the scene rect
        print("Scene rect:", self.scene.sceneRect())

        self.pixmap = QPixmap(self.scene.sceneRect().size().toSize())

        # Fill the pixmap with a transparent color to check if it's being painted
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
            self.scene.setSceneRect(rect)

            # Debug print to check the size of the page rect
            print("Page rect:", rect)

            # Render the scene onto the printer, ensure to pass the page rect
            self.scene.render(painter, rect, self.scene.sceneRect())

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
