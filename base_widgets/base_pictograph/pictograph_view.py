# pictograph_view.py
import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame, QMenu, QToolTip, QApplication
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import (
    QPainter,
    QCursor,
    QKeyEvent,
    QMouseEvent,
    QClipboard,
    QAction,
    QContextMenuEvent,
)


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

        # Basic setup without border logic
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        # Gestures and other initializations if necessary
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        self.setSceneRect(self.scene().itemsBoundingRect())
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def enterEvent(self, event: QEvent) -> None:
        """Handle mouse entering the widget area."""
        # No border logic
        pass

    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leaving the widget area."""
        # No border logic
        pass

    def contextMenuEvent(self, event: QEvent) -> None:
        """
        Override the context menu event to provide custom options.
        Allows users to copy the pictograph_dict to the clipboard.
        """
        if isinstance(event, QContextMenuEvent):
            # Create a QMenu instance
            context_menu = QMenu(self)

            # Create the "Copy Dictionary" action
            copy_action = QAction("Copy Dictionary", self)
            copy_action.triggered.connect(self.copy_pictograph_dict)

            # Add the action to the menu
            context_menu.addAction(copy_action)

            # Optionally, add more actions here

            # Execute the menu at the cursor's position
            context_menu.exec(QCursor.pos())

    def copy_pictograph_dict(self) -> None:
        """
        Serialize the pictograph_dict and copy it to the clipboard.
        """
        # Ensure pictograph_dict exists
        if (
            hasattr(self.pictograph, "pictograph_dict")
            and self.pictograph.pictograph_dict
        ):
            try:
                # Serialize the dictionary to a JSON-formatted string
                pictograph_json = json.dumps(
                    self.pictograph.pictograph_dict, indent=4, ensure_ascii=False
                )

                # Access the clipboard and set the text
                clipboard: QClipboard = QApplication.clipboard()
                clipboard.setText(pictograph_json)
                indicator_label = (
                    self.pictograph.main_widget.sequence_widget.indicator_label
                )
                indicator_label.show_message("Dictionary copied to clipboard!")
                # Optionally, show a tooltip notification
                QToolTip.showText(
                    QCursor.pos(), "Pictograph dictionary copied to clipboard.", self
                )

            except Exception as e:
                # Handle any exceptions that occur during serialization or clipboard access
                print(f"Error copying pictograph_dict to clipboard: {e}")
                QToolTip.showText(QCursor.pos(), "Failed to copy dictionary.", self)
        else:
            print("No pictograph_dict available to copy.")
            QToolTip.showText(QCursor.pos(), "No dictionary to copy.", self)
