from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from PyQt6.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve,
    QTimer,
)

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class ParallelStackFader:
    """Handles fading transitions between two stacks and then animates a resize event (via minimumWidth) after the fade."""

    left_old_widget: Optional[QWidget] = None
    left_new_widget: Optional[QWidget] = None
    right_old_widget: Optional[QWidget] = None
    right_new_widget: Optional[QWidget] = None

    def __init__(self, manager: "FadeManager"):
        self.manager = manager
        # Keep a reference to the current resize animation to prevent GC.
        self._current_resize_animation = None

    def fade_both_stacks(
        self,
        right_stack: QStackedWidget,
        right_new_index: int,
        left_stack: QStackedWidget,
        left_new_index: int,
        width_ratio: tuple[float, float],
        fade_duration: int = 300,
        resize_duration: int = 200,
        callback: Optional[callable] = None,
    ):
        """
        Fade out the current tab (e.g. generate), then switch to the new tab (e.g. browse) and fade it in.
        After the new tab is visible, animate the resizing of the left/right stacks.
        """
        # Cache current and target widgets.
        self.right_old_widget = right_stack.currentWidget()
        self.left_old_widget = left_stack.currentWidget()
        self.right_new_widget = right_stack.widget(right_new_index)
        self.left_new_widget = left_stack.widget(left_new_index)

        if not (
            self.right_old_widget
            and self.left_old_widget
            and self.right_new_widget
            and self.left_new_widget
        ):
            return

        # Step 1: Fade out the current widgets.
        def fade_out_finished():
            # Step 2: Switch the stacks to the new tab’s widgets.
            right_stack.setCurrentIndex(right_new_index)
            left_stack.setCurrentIndex(left_new_index)

            # Step 3: Fade in the new widgets and animate the resizing simultaneously.
            self.manager.widget_fader.fade_widgets(
                [self.right_new_widget, self.left_new_widget],
                fade_in=True,
                duration=fade_duration,
            )
            animate_resize()

        self.manager.widget_fader.fade_widgets(
            [self.right_old_widget, self.left_old_widget],
            fade_in=False,
            duration=fade_duration,
            callback=fade_out_finished,
        )

        # Step 4: Animate the resizing.
        def animate_resize():
            total_width = self.manager.main_widget.width()
            left_target = int(total_width * width_ratio[0])
            right_target = total_width - left_target

            # Animate minimumWidth so that the widget actually reflows its layout.
            left_anim = QPropertyAnimation(left_stack, b"minimumWidth")
            left_anim.setDuration(resize_duration)
            left_anim.setStartValue(left_stack.width())
            left_anim.setEndValue(left_target)
            left_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

            right_anim = QPropertyAnimation(right_stack, b"minimumWidth")
            right_anim.setDuration(resize_duration)
            right_anim.setStartValue(right_stack.width())
            right_anim.setEndValue(right_target)
            right_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

            group = QParallelAnimationGroup()
            group.addAnimation(left_anim)
            group.addAnimation(right_anim)

            def on_resize_finished():
                # Set the fixed width after the animation completes.
                left_stack.setFixedWidth(left_target)
                right_stack.setFixedWidth(right_target)
                if callback:
                    callback()

            group.finished.connect(on_resize_finished)
            group.start()
            self._current_resize_animation = group  # Keep a reference

        # End of fade_both_stacks()
