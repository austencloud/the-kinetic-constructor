from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QMouseEvent

from Enums.letters import LetterType
from main_window.main_widget.generate_tab.freeform.letter_type_picker_widget.letter_type_widget_animator import (
    LetterTypeButtonAnimator,
)
from main_window.main_widget.generate_tab.freeform.letter_type_picker_widget.letter_type_widget_updater import (
    LetterTypeButtonUpdater,
)
from .styled_border_overlay_for_button import StyledBorderOverlayForButton

if TYPE_CHECKING:
    from .letter_type_picker import LetterTypePicker


class LetterTypeButton(QWidget):
    clicked = pyqtSignal(LetterType, bool)

    def __init__(
        self,
        letter_type_picker: "LetterTypePicker",
        letter_type: LetterType,
        index: int,
    ):
        super().__init__()
        self.letter_type = letter_type
        self.letter_type_picker = letter_type_picker
        self.index = index

        self.is_selected = True
        self._hovered = False

        self.primary_color, self.secondary_color = self._get_border_colors(letter_type)

        self.label = QLabel(str(self.index), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.overlay = StyledBorderOverlayForButton(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._baseColor = QColor("white")
        self.animator = LetterTypeButtonAnimator(self)
        self.updater = LetterTypeButtonUpdater(self)

        self.updater.update_colors()
        self.setFixedSize(60, 60)

    def enterEvent(self, event):
        self._hovered = True
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        self.animator.animate_hover(True, self._baseColor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        QApplication.restoreOverrideCursor()
        self.animator.animate_hover(False, self._baseColor)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_selected = not self.is_selected
            self.updater.update_colors()
            self.clicked.emit(self.letter_type, self.is_selected)
            self.animator.animate_press()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.animator.animate_release()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setFixedSize(self.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self.animator.clickScale, self.animator.clickScale)
        painter.translate(-self.width() / 2, -self.height() / 2)

        super().paintEvent(event)

    def _get_border_colors(self, letter_type: LetterType):
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),
            LetterType.Type3: ("#26e600", "#6F2DA8"),
            LetterType.Type4: ("#26e600", "#26e600"),
            LetterType.Type5: ("#00b3ff", "#26e600"),
            LetterType.Type6: ("#eb7d00", "#eb7d00"),
        }
        return border_colors_map.get(letter_type, ("black", "black"))
