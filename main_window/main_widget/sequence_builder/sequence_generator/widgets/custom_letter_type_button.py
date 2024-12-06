from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QColor
from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.letter_type_text_painter import (
    LetterTypeTextPainter,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.sequence_generator.widgets.letter_type_picker import (
        LetterTypePicker,
    )


class CustomLetterTypeButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, letter_type_picker: "LetterTypePicker", letter_type: LetterType):
        super().__init__(letter_type_picker)
        self.letter_type = letter_type
        self.letter_type_picker = letter_type_picker
        self.is_checked = True  # Default state
        self.is_hovered = False  # Track hover state

        # Set initial properties
        self.setText(self._get_colored_text())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # StyledBorderOverlay for custom borders
        # self.border_overlay = StyledBorderOverlay(self)

        # Animation for background color transition
        self.bg_animation = QVariantAnimation(self)
        self.bg_animation.setDuration(300)
        self.bg_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.bg_animation.valueChanged.connect(self.animate_background)

        # Hover effect (border growth)
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
        """Toggle the check state and emit clicked signal."""
        self.is_checked = not self.is_checked
        self.update_style()
        self.clicked.emit()

    def enterEvent(self, event):
        """Animate the hover effect and update background color."""
        if not self.is_checked:
            self.is_hovered = True
            self.hover_animation.setDirection(QVariantAnimation.Direction.Forward)
            self.hover_animation.start()

            # Set the background to light gray when hovered
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#e0e0e0"))  # Light gray
            self.bg_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        """Shrink the border when the hover state ends and reset background."""
        if not self.is_checked:
            self.is_hovered = False
            self.hover_animation.setDirection(QVariantAnimation.Direction.Backward)
            self.hover_animation.start()

            # Reset the background to white when hover ends
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#f0f0f0"))  # White
            self.bg_animation.start()

        super().leaveEvent(event)

    def animate_hover_border(self, border_width):
        """Animate the border width during hover."""
        border_thickness = f"{border_width}px"
        self.setStyleSheet(
            f"background-color: {self.palette().color(self.backgroundRole()).name()}; "
            f"color: black; "
            f"padding: 10px; "
            f"border-radius: {min(self.width(), self.height()) // 10}px; "  # Dynamically set border radius
            f"border: {border_thickness} solid black; "
            f"font-size: {self.letter_type_picker.get_font_size()}px;"
        )

    def update_style(self):
        """Update the visual style based on the checked state and hover."""
        font_size = self.letter_type_picker.get_font_size()
        border_thickness = "3px" if self.is_checked else "1px"

        # Adjust border radius based on the button's size
        border_radius = min(self.width(), self.height()) // 10

        # Set the background to dark gray if pressed, otherwise check hover
        if self.is_checked:
            self.bg_animation.setStartValue(self.palette().color(self.backgroundRole()))
            self.bg_animation.setEndValue(QColor("#999999"))  # Darker gray for pressed
            self.bg_animation.start()

            # self.border_overlay.update_border_color_and_width(
            #     *self._get_border_colors()
            # )
        else:
            # self.border_overlay.update_border_color_and_width(
            #     "transparent", "transparent"
            # )
            if self.is_hovered:
                self.bg_animation.setStartValue(
                    self.palette().color(self.backgroundRole())
                )
                self.bg_animation.setEndValue(
                    QColor("#e0e0e0")
                )  # Light gray when hovered
            else:
                self.bg_animation.setStartValue(
                    self.palette().color(self.backgroundRole())
                )
                self.bg_animation.setEndValue(QColor("#f0f0f0"))  # White when idle
            self.bg_animation.start()

        # Apply the current style settings
        self.setStyleSheet(
            f"background-color: {self.palette().color(self.backgroundRole()).name()}; "
            "color: black; "
            "padding: 10px; "
            f"border-radius: {border_radius}px; "  # Dynamically set border radius
            f"border: {border_thickness} solid black; "
            f"font-size: {font_size}px;"
        )
        self.setText(self._get_colored_text())  # Ensure text stays bold

    def _get_border_colors(self) -> tuple[str, str]:
        """Determine the border colors based on the LetterType."""
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#00b3ff", "#26e600"),  # Cyan, Green
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        return border_colors_map.get(self.letter_type, ("black", "black"))

    def animate_background(self, color: QColor):
        """Animate the background color smoothly."""
        color_name = color.name()
        border_thickness = "3px" if self.is_checked else "1px"

        # Update dynamically calculated border radius
        border_radius = min(self.width(), self.height()) // 10

        self.setStyleSheet(
            f"background-color: {color_name}; "
            "color: black; "
            "padding: 10px; "
            f"border-radius: {border_radius}px; "
            f"border: {border_thickness} solid black; "
            f"font-size: {self.letter_type_picker.get_font_size()}px;"
        )
        self.setText(self._get_colored_text())  # Keep colored text bold

    def resizeEvent(self, event):
        """Ensure the border overlay and the button size adjust when resized."""
        super().resizeEvent(event)
        self.update_style()
        # self.border_overlay.resize_styled_border_overlay()
