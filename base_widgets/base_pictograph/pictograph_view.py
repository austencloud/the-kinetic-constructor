# pictograph_view.py
import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame, QMenu, QToolTip, QApplication
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QClipboard, QAction, QContextMenuEvent


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        self.setSceneRect(self.scene().itemsBoundingRect())
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def enterEvent(self, event: QEvent) -> None:
        pass

    def leaveEvent(self, event: QEvent) -> None:
        pass

    def contextMenuEvent(self, event: QEvent) -> None:
        if isinstance(event, QContextMenuEvent):
            context_menu = QMenu(self)
            copy_action = QAction("Copy Dictionary", self)
            copy_action.triggered.connect(self.copy_pictograph_dict)
            context_menu.addAction(copy_action)
            context_menu.exec(QCursor.pos())

    def copy_pictograph_dict(self) -> None:
        if (
            hasattr(self.pictograph, "pictograph_dict")
            and self.pictograph.pictograph_dict
        ):
            try:
                pictograph_json = json.dumps(
                    self.pictograph.pictograph_dict, indent=4, ensure_ascii=False
                )

                clipboard: QClipboard = QApplication.clipboard()
                clipboard.setText(pictograph_json)
                indicator_label = (
                    self.pictograph.main_widget.sequence_widget.indicator_label
                )
                indicator_label.show_message("Dictionary copied to clipboard!")
                QToolTip.showText(
                    QCursor.pos(), "Pictograph dictionary copied to clipboard.", self
                )

            except Exception as e:
                print(f"Error copying pictograph_dict to clipboard: {e}")
                QToolTip.showText(QCursor.pos(), "Failed to copy dictionary.", self)
        else:
            print("No pictograph_dict available to copy.")
            QToolTip.showText(QCursor.pos(), "No dictionary to copy.", self)
