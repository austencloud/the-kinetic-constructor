from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtSlot
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from main_window.main_widget.tab_fade_manager import TabFadeManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabSwitcher(QObject):
    fade_duration = 350

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_stack = self.main_widget.main_stacked_widget
        self.opacity_effect = QGraphicsOpacityEffect(self.main_stack)
        self.main_stack.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)  # Fully visible initially
        self._is_animating = False

    def fade_to_tab(self, new_index: int, on_finished: Optional[Callable] = None):
        """Fades out the current tab and fades in the new tab."""
        if self._is_animating:
            return
        if new_index == self.main_stack.currentIndex():
            return

        self._is_animating = True
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(self.fade_duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(lambda: self._switch_tab(new_index, on_finished))
        self.fade_out.finished.connect(self._animation_finished)
        self.fade_out.start()

    def _switch_tab(self, new_index: int, on_finished: Optional[Callable]):
        """Switch to the new tab and initiate fade-in."""
        self.main_stack.setCurrentIndex(new_index)

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(self.fade_duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if on_finished:
            self.fade_in.finished.connect(on_finished)

        self.fade_in.finished.connect(self._animation_finished)
        self.fade_in.start()

    @pyqtSlot()
    def _animation_finished(self):
        """Resets the animation flag after completion."""
        self._is_animating = False

    @pyqtSlot(int)
    def on_tab_selected(self, tab_index: int):
        tab_mapping = {
            0: ("construct", 0),
            1: ("generate", 0),
            2: ("browse", 1),
            3: ("learn", 2),
            4: ("write", 3),
        }

        if tab_index not in tab_mapping:
            return

        tab_name, main_stack_index = tab_mapping[tab_index]
        self.main_widget.settings_manager.global_settings.set_current_tab(tab_name)

        if tab_name in ["construct", "generate"]:
            self.fade_to_tab(main_stack_index)

            if tab_name == "construct":
                self.main_widget.build_tab.show_construct()
            elif tab_name == "generate":
                self.main_widget.build_tab.show_generate()
        else:
            self.fade_to_tab(main_stack_index)
