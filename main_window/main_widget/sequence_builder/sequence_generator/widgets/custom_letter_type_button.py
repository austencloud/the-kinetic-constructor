from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QColor
from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.letter_type_text_painter import (
    LetterTypeTextPainter,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.sequence_generator.freeform.letter_picker_dialog import (
        LetterPickerDialog,
    )


class CustomLetterTypeButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, dialog: "LetterPickerDialog", letter_type: LetterType):
        super().__init__(dialog)
        self.letter_type = letter_type
        self.dialog = dialog
        self.is_checked = True  # Default state
        self.is_hovered = False  # Track hover state

        # Set initial properties
        self.setText(self._get_colored_text())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Animation for background color transition
        self.bg_animation = QVariantAnimation(self)
        self.bg_animation.setDuration(300)
        self.bg_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.bg_animation.valueChanged.connect(self.animate_background)

        # Hover animation (not strictly necessary but kept for completeness)
        self.hover_animation = QVariantAnimation(self)
        self.hover_animation.setDuration(300)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.hover_animation.setStartValue(1)
        self.hover_animation.setEndValue(3)
        self.hover_animation.valueChanged.connect(self.animate_hover_border)

        # Set initial background state
        self.animate_background(QColor("#f0f0f0"))

        # Initial style update
        self.update_style()

    def _get_colored_text(self) -> str:
        """Use LetterTypeTextPainter to style the text, keeping it bold."""
        styled_description = LetterTypeTextPainter.get_colored_text(
            self.letter_type.description, bold=True
        )
        return f"<b>{self.letter_type.name}</b><br>{styled_description}"

    def mousePressEvent(self, event):
        """Toggle the check state on click and emit the clicked signal."""
        self.is_checked = not self.is_checked
        self.update_style()
        self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self.is_checked:
            self.is_hovered = True
            self.hover_animation.setDirection(QVariantAnimation.Direction.Forward)
            self.hover_animation.start()
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#e0e0e0"))
            self.bg_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_checked:
            self.is_hovered = False
            self.hover_animation.setDirection(QVariantAnimation.Direction.Backward)
            self.hover_animation.start()
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#f0f0f0"))
            self.bg_animation.start()
        super().leaveEvent(event)

    def animate_hover_border(self, border_width):
        border_thickness = f"{border_width}px"
        self.setStyleSheet(
            f"background-color: {self.palette().color(self.backgroundRole()).name()}; "
            f"color: black; "
            f"padding: 10px; "
            f"border-radius: {min(self.width(), self.height()) // 10}px; "
            f"border: {border_thickness} solid black; "
            f"font-size: {self.dialog.get_font_size()}px;"
        )

    def update_style(self):
        font_size = self.dialog.get_font_size()
        border_thickness = "3px" if self.is_checked else "1px"
        border_radius = min(self.width(), self.height()) // 10

        if self.is_checked:
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#999999"))  # Darker gray
            self.bg_animation.start()
        else:
            if self.is_hovered:
                self.bg_animation.setStartValue(
                    self.palette().color(self.backgroundRole())
                )
                self.bg_animation.setEndValue(QColor("#e0e0e0"))
            else:
                self.bg_animation.setStartValue(
                    self.palette().color(self.backgroundRole())
                )
                self.bg_animation.setEndValue(QColor("#f0f0f0"))
            self.bg_animation.start()

        self.setStyleSheet(
            f"background-color: {self.palette().color(self.backgroundRole()).name()}; "
            "color: black; "
            "padding: 10px; "
            f"border-radius: {border_radius}px; "
            f"border: {border_thickness} solid black; "
            f"font-size: {font_size}px;"
        )
        self.setText(self._get_colored_text())

    def animate_background(self, color: QColor):
        color_name = color.name()
        border_thickness = "3px" if self.is_checked else "1px"
        border_radius = min(self.width(), self.height()) // 10
        self.setStyleSheet(
            f"background-color: {color_name}; "
            "color: black; "
            "padding: 10px; "
            f"border-radius: {border_radius}px; "
            f"border: {border_thickness} solid black; "
            f"font-size: {self.dialog.get_font_size()}px;"
        )
        self.setText(self._get_colored_text())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_style()
