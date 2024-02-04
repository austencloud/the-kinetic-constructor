from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from widgets.scroll_area.components.section_manager.section_widget.components.type_label import (
    SectionTypeLabel,
)

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )


class SectionHeader(QWidget):
    clicked = pyqtSignal()
    EXPAND_ARROW_PATH = "images/icons/dropdown/expand.png"
    COLLAPSE_ARROW_PATH = "images/icons/dropdown/collapse.png"

    def __init__(self, section_widget: "SectionWidget") -> None:
        super().__init__()
        self.section = section_widget
        self.type_label = SectionTypeLabel(section_widget)
        self.arrow_label = QLabel()
        self.arrow_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.expand_arrow_pixmap = self.load_and_resize_pixmap(self.EXPAND_ARROW_PATH)
        self.collapse_arrow_pixmap = self.load_and_resize_pixmap(
            self.COLLAPSE_ARROW_PATH
        )
        self.toggle_dropdown_arrow(False)

        self.left_frame = QWidget()
        self.middle_frame = QWidget()
        self.right_frame = QWidget()

        self._setup_frames()
        self._set_contents_margins()

    def _setup_frames(self) -> None:
        self._setup_left_frame()
        self._setup_middle_frame()
        self._setup_right_frame()

        main_frame = QFrame()
        main_frame.layout = QHBoxLayout(main_frame)
        main_frame.layout.addStretch(10)
        main_frame.layout.addWidget(self.left_frame)
        main_frame.layout.addStretch(1)
        main_frame.layout.addWidget(self.middle_frame)
        main_frame.layout.addStretch(1)
        main_frame.layout.addWidget(self.right_frame)
        main_frame.layout.addStretch(10)
        main_frame.setContentsMargins(0, 0, 0, 0)
        main_frame.layout.setContentsMargins(0, 0, 0, 0)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(main_frame)
        self.layout.setContentsMargins(0, 0, 0, 0)
        button_size = self.section.scroll_area.width() // 20
        self.left_frame.setFixedWidth(button_size)
        self.left_frame.setFixedHeight(button_size)
        self.right_frame.setFixedWidth(button_size)
        self.right_frame.setFixedHeight(button_size)
        self.setMaximumHeight(button_size)

    def _setup_left_frame(self) -> None:
        left_layout = QHBoxLayout(self.left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.section.vtg_dir_button_manager.opp_button)

    def _setup_middle_frame(self) -> None:
        middle_layout = QHBoxLayout(self.middle_frame)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.addWidget(self.type_label)
        middle_layout.addStretch(2)
        middle_layout.addWidget(self.arrow_label)

    def _setup_right_frame(self) -> None:
        right_layout = QHBoxLayout(self.right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.section.vtg_dir_button_manager.same_button)

    def _set_contents_margins(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

    def load_and_resize_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        height = self.section.scroll_area.width() // 40
        return pixmap.scaledToHeight(height, Qt.TransformationMode.SmoothTransformation)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.clicked.emit()

    def toggle_dropdown_arrow(self, is_expanded) -> None:
        arrow_pixmap = (
            self.expand_arrow_pixmap if is_expanded else self.collapse_arrow_pixmap
        )
        self.arrow_label.setPixmap(arrow_pixmap)
