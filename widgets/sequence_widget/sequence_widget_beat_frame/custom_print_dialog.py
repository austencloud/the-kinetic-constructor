from email.charset import QP
from typing import TYPE_CHECKING
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPixmap, QTransform, QPainter
from PyQt6.QtCore import Qt, QRectF

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsView,
    QSpinBox,
    QLabel,
    QGraphicsScene,
)


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from widgets.main_widget.main_widget import MainWidget


class CustomPrintDialog(QDialog):
    def __init__(self, pixmap: QPixmap, beat_frame: "SequenceWidgetBeatFrame") -> None:
        super().__init__(beat_frame)
        self.pixmap = pixmap
        self.beat_frame = beat_frame
        self.printer = QPrinter()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Print Preview")
        main_layout = QHBoxLayout(self)

        current_word = self.beat_frame.get_current_word()

        # Preview Column
        preview_column_layout = QVBoxLayout()
        self.label_current_word = QLabel(f"Current Word: {current_word}", self)
        self.preview_area = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.preview_area.setScene(self.scene)
        self.update_preview()
        preview_column_layout.addWidget(self.label_current_word)
        preview_column_layout.addWidget(self.preview_area)
        main_layout.addLayout(preview_column_layout)

        # Controls Column
        controls_column_layout = QVBoxLayout()
        copies_layout = QHBoxLayout()
        self.copies_label = QLabel("Copies:", self)
        self.copies_spinbox = QSpinBox(self)
        self.copies_spinbox.setMinimum(1)
        copies_layout.addWidget(self.copies_label)
        copies_layout.addWidget(self.copies_spinbox)
        controls_column_layout.addLayout(copies_layout)
        self.print_button = QPushButton("Print", self)
        self.print_button.clicked.connect(self.print)
        controls_column_layout.addWidget(self.print_button)
        main_layout.addLayout(controls_column_layout)

    def update_preview(self):
        self.scene.clear()
        self.preview_pixmap_item = self.scene.addPixmap(self.pixmap)
        self.preview_area.fitInView(
            self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.scene.setSceneRect(
            QRectF(self.preview_pixmap_item.pixmap().rect())
        )  # Fit the scene to the pixmap

    def print(self):
        # Set up the printer settings based on the dialog controls
        self.printer.setCopyCount(self.copies_spinbox.value())

        # Prepare to print
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.perform_print()

    def perform_print(self):
        painter = QPainter(self.printer)

        # Here, adjust the scaling of the pixmap based on the printer's page rect
        rect = self.printer.pageRect(QPrinter.Unit.Point)
        scale_factor = min(
            rect.width() / self.pixmap.width(), rect.height() / self.pixmap.height()
        )
        scaled_pixmap = self.pixmap.scaled(
            self.pixmap.size() * scale_factor, Qt.AspectRatioMode.KeepAspectRatio
        )
        x = int((rect.width() - scaled_pixmap.width()) / 2)
        y = int((rect.height() - scaled_pixmap.height()) / 2)

        # Draw the pixmap on the page
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()
