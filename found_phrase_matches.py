# GENERATED FILE: Matching classes for phrase: 'setGraphicsEffect(None)'
# Search directory: C:\the-kinetic-constructor\main_window

# -------------------------------------------------------
# File: C:\the-kinetic-constructor\main_window\main_widget\base_indicator_label.py
# -------------------------------------------------------
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSlot
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget



# [Line 13]
class BaseIndicatorLabel(QLabel):
    def __init__(
        self, parent_widget: Union["BaseLessonWidget", "SequenceWidget"]
    ) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.font_size = parent_widget.width() // 40
        font = self.font()
        font.setPointSize(self.font_size)
        font.setWeight(QFont.Weight.DemiBold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()
        self.setContentsMargins(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)


    def show_message(self, text) -> None:
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(None)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.clear)
        if self.timer.isActive():
            self.timer.stop()
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()

        self.setText(text)
        self.timer.start(1000)

    @pyqtSlot()
    def start_fade_out(self) -> None:
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def clear(self) -> None:
        self.setText(" ")
# -------------------------------------------------------
# File: C:\the-kinetic-constructor\main_window\main_widget\browse_tab\browse_tab_filter_manager.py
# -------------------------------------------------------
from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.browse_tab import BrowseTab



# [Line 13]
class BrowseTabFilterManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.main_widget = self.browse_tab.main_widget
        self.fade_manager = self.main_widget.fade_manager

    def show_favorites(self):
        """Show only favorite sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("favorite sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        favorites = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if any(
                self.browse_tab.main_widget.metadata_extractor.get_favorite_status(
                    thumbnail
                )
                for thumbnail in thumbnails
            )
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = favorites
        self.browse_tab.ui_updater.update_and_display_ui(len(favorites))

    def show_all_sequences(self):
        """Show all sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("all sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        sequences = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = sequences
        self.browse_tab.ui_updater.update_and_display_ui(len(sequences))

    def show_most_recent_sequences(self, date: datetime):
        """Show most recent sequences based on date."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("most recent sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        most_recent = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if self.browse_tab.sequence_picker.section_manager.get_date_added(
                thumbnails
            )
            >= date
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = most_recent
        self.browse_tab.ui_updater.update_and_display_ui(len(most_recent))

    def show_browser_with_filters_from_settings(self):
        """Show browser with filters from settings."""
        current_filter = (
            self.browse_tab.main_widget.main_window.settings_manager.browse_settings.get_current_filter()
        )

        self.apply_filter(current_filter)

    def apply_filter(self, current_filter):
        self.browse_tab.settings.set_current_section("sequence_picker")
        self.current_filter = current_filter

        widgets_to_fade = [
            self.browse_tab.sequence_picker.filter_stack,
            self.browse_tab.sequence_picker,
        ]
        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self._apply_filter_logic,
        )

    def _apply_filter_logic(self):
        self.browse_tab.filter_manager.sort_and_display_thumbnail_boxes_by_current_filter(
            self.browse_tab.filter_manager.current_filter
        )
        # QApplication.processEvents()
        self.browse_tab.main_widget.left_stack.setCurrentIndex(
            self.browse_tab.main_widget.left_sequence_picker_index
        )
        # self.browse_tab.main_widget.left_stack.setGraphicsEffect(None)
        # self.browse_tab.sequence_picker.setGraphicsEffect(None)
        # self.main_widget.fade_manager.graphics_effect_remover.clear_graphics_effects()

    def sort_and_display_thumbnail_boxes_by_current_filter(
        self, initial_selection: dict
    ) -> None:

        filter_selector = self.browse_tab.sequence_picker.filter_stack
        starting_position_section = filter_selector.starting_position_section
        contains_letter_section = filter_selector.contains_letter_section
        starting_letter_section = filter_selector.starting_letter_section
        level_section = filter_selector.level_section
        length_section = filter_selector.length_section
        author_section = filter_selector.author_section
        grid_mode_section = filter_selector.grid_mode_section
        display_functions = {
            "starting_letter": starting_letter_section.display_only_thumbnails_starting_with_letter,
            "sequence_length": length_section.display_only_thumbnails_with_sequence_length,
            "level": level_section.display_only_thumbnails_with_level,
            "contains_letters": contains_letter_section.display_only_thumbnails_containing_letters,
            "starting_position": starting_position_section.display_only_thumbnails_with_starting_position,
            "author": author_section.display_only_thumbnails_by_author,
            "favorites": self.browse_tab.filter_manager.show_favorites,
            "most_recent": self.browse_tab.filter_manager.show_most_recent_sequences,
            "grid_mode": grid_mode_section.display_only_thumbnails_with_grid_mode,
            "show_all": self.browse_tab.filter_manager.show_all_sequences,
        }
        if initial_selection:
            for key, value in initial_selection.items():
                if key in display_functions:
                    if key in ["favorites", "show_all"]:
                        display_functions[key]()
                    else:
                        display_functions[key](value)

    def prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.setText(
            ""
        )
        # QApplication.processEvents()
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.show_message(
            description
        )
        self.browse_tab.sequence_picker.control_panel.count_label.setText("")
        self.browse_tab.sequence_picker.scroll_widget.clear_layout()
        self.browse_tab.sequence_picker.scroll_widget.grid_layout.addWidget(
            self.browse_tab.sequence_picker.progress_bar,
            0,
            0,
            1,
            self.browse_tab.sequence_picker.sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.browse_tab.sequence_picker.progress_bar.setVisible(True)
        self.browse_tab.sequence_picker.progress_bar.resize_progress_bar()

        # QApplication.processEvents()
# -------------------------------------------------------
# File: C:\the-kinetic-constructor\main_window\main_widget\fade_manager\graphics_effect_remover.py
# -------------------------------------------------------
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel
from main_window.main_widget.fade_manager.fadeable_opacity_effect import FadableOpacityEffect

if TYPE_CHECKING:
    from .fade_manager import FadeManager



# [Line 11]
class GraphicsEffectRemover:
    def __init__(self, fade_manager: "FadeManager"):
        self.manager = fade_manager

    def clear_graphics_effects(self, widgets: list[QWidget] = None) -> None:
        """Remove all graphics effects from specified widgets and their children."""
        if not widgets:  # Handle None or empty list
            widgets = [
                self.manager.main_widget.right_stack.currentWidget(),
                self.manager.main_widget.left_stack.currentWidget(),
            ]
        for widget in widgets:
            if widget:
                self._remove_all_graphics_effects(widget)


    def _remove_all_graphics_effects(self, widget):
        # If widget is a QWidget, process its graphics effect and its children.
        if isinstance(widget, QWidget):
            if widget.graphicsEffect():
                widget.setGraphicsEffect(None)
            for child in widget.findChildren(QWidget):
                if child.graphicsEffect():
                    # Optionally, check for a specific base class as you already do.
                    if child.__class__.__base__ != BaseIndicatorLabel:
                        child.setGraphicsEffect(None)
        else:
            # For non-QWidget items (e.g. QGraphicsItemGroup), you might choose to do nothing,
            # or handle them in a custom way.
            pass
# -------------------------------------------------------
# File: C:\the-kinetic-constructor\main_window\main_widget\fade_manager\widget_fader.py
# -------------------------------------------------------
import os
from typing import TYPE_CHECKING, Optional, Union
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QGraphicsItem
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from Enums.Enums import Glyph
from base_widgets.base_pictograph.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from main_window.main_widget.fade_manager.fade_when_ready_helper import (
    FadeWhenReadyHelper,
)
from main_window.main_widget.fade_manager.fadeable_opacity_effect import FadableOpacityEffect

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


def safe_remove_effect(widget: QWidget, effect: QGraphicsOpacityEffect):
    if widget.graphicsEffect() is effect:
        widget.setGraphicsEffect(None)



# [Line 28]
class WidgetFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager
        self.profiler = manager.main_widget.main_window.profiler

    def fade_widgets(
        self,
        widgets: list[QWidget],
        fade_in: bool,
        duration: int,
        callback: Optional[callable] = None,
    ) -> None:
        if not widgets:
            if callback:
                callback()
            return

        ready_widgets: list[QWidget] = []
        for widget in widgets:
            if widget.isVisible() and widget.window().winId():
                ready_widgets.append(widget)
            else:
                from main_window.main_widget.fade_manager.fade_when_ready_helper import FadeWhenReadyHelper
                helper = FadeWhenReadyHelper(widget, fade_in, duration, callback, self)
                widget.installEventFilter(helper)
        
        if not ready_widgets:
            return

        animation_group = QParallelAnimationGroup(self.manager)
        for widget in ready_widgets:
            effect = self._ensure_opacity_effect(widget)
            # Mark the effect as in use.
            effect.in_animation = True

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0 if fade_in else 1.0)
            animation.setEndValue(1.0 if fade_in else 0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(animation)

            # When the animation finishes, mark the effect as no longer in use and then remove it safely.
            animation.finished.connect(lambda w=widget, eff=effect: self._animation_finished(w, eff))

        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def _animation_finished(self, widget: QWidget, effect: FadableOpacityEffect):
        effect.in_animation = False
        # Only remove if the widget’s current effect is still ours.
        if widget.graphicsEffect() is effect:
            widget.setGraphicsEffect(None)


    def _ensure_opacity_effect(self, widget: QWidget) -> FadableOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, FadableOpacityEffect):
            effect = FadableOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect


    def fade_and_update(
        self,
        widget: list[QWidget],
        callback: Union[callable, tuple[callable, callable]] = None,
        duration: int = 250,
    ) -> None:

        # self.profiler.enable()

        def on_fade_out_finished():
            self.manager.graphics_effect_remover.clear_graphics_effects(widget)

            if callback:
                if isinstance(callback, tuple):
                    callback[0]()
                    self.fade_widgets(
                        widget,
                        True,
                        duration,
                        lambda: QTimer.singleShot(0, callback[1]),
                    )
                else:
                    callback()
                    self.fade_widgets(widget, True, duration)

        self.fade_widgets(widget, False, duration, on_fade_out_finished)

        # self.profiler.disable()
        # self.profiler.write_profiling_stats_to_file(
        #     "option_updater_profile.txt", os.getcwd()
        # )

    def fade_visibility_items_to_opacity(
        self,
        visibility_element: Union[Glyph, NonRadialPointsGroup],
        opacity: float,
        duration: int = 300,
        callback: Optional[callable] = None,
    ) -> None:
        if not visibility_element:
            if callback:
                callback()
            return
        items = self._get_corresponding_items(visibility_element)

        self.manager.graphics_effect_remover.clear_graphics_effects(
            [visibility_element]
        )
        animation_group = QParallelAnimationGroup(self.manager)
        for item in items:
            self.manager.graphics_effect_remover.clear_graphics_effects([item])
            if isinstance(item, QGraphicsItem):
                item.setOpacity(opacity)
            elif isinstance(item, QWidget):
                effect = self._ensure_opacity_effect(item)
                if effect:
                    start_opacity = effect.opacity() if effect else 1.0
                    animation = QPropertyAnimation(effect, b"opacity")
                    animation.setDuration(duration)
                    animation.setStartValue(start_opacity)
                    animation.setEndValue(opacity)
                    animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                    animation_group.addAnimation(animation)
        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def _get_corresponding_items(
        self, element: Union[Glyph, NonRadialPointsGroup]
    ) -> list[Union[Glyph, NonRadialPointsGroup]]:
        if element.name == "TKA":
            items = element.get_all_items()
        elif element.name == "VTG":
            items = [element]
        elif element.name == "Elemental":
            items = [element]
        elif element.name == "Positions":
            items = element.get_all_items()
        elif element.name == "Reversals":
            items = list(element.reversal_items.values())
        elif element.name == "non_radial_points":
            items = element.child_points
        return items
# -------------------------------------------------------
# File: C:\the-kinetic-constructor\main_window\main_widget\sequence_widget\graph_editor\graph_editor_animator.py
# -------------------------------------------------------
from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QRect, QPoint, QEasingCurve, QObject
if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import GraphEditor


# [Line 6]
class GraphEditorAnimator(QObject):
    def __init__(self, graph_editor: "GraphEditor"):
        super().__init__(graph_editor)
        self.sequence_widget = graph_editor.sequence_widget
        self.graph_editor = graph_editor
        self.toggle_tab = graph_editor.toggle_tab
        self.graph_editor_placeholder = self.graph_editor.placeholder
        self.button_panel_bottom_placeholder = (
            self.sequence_widget.button_panel.bottom_placeholder
        )
        self.current_animations = []

    def toggle(self):
        if self.graph_editor.is_toggled:
            self.graph_editor.is_toggled = False
            self.animate_graph_editor(show=False)
        else:
            self.sequence_widget.layout_manager.main_layout.addWidget(
                self.graph_editor_placeholder
            )
            self.graph_editor.show()
            self.graph_editor.is_toggled = True
            self.animate_graph_editor(show=True)

    def clear_previous_animations(self):
        """Stop all currently running animations and clear effects."""
        for animation in self.current_animations:
            animation.stop()
        self.current_animations.clear()

        # Clear any lingering graphics effects (if used)
        self.graph_editor.setGraphicsEffect(None)
        self.graph_editor_placeholder.setGraphicsEffect(None)
        self.toggle_tab.setGraphicsEffect(None)

    def animate_graph_editor(self, show):
        self.clear_previous_animations()

        parent_height = self.sequence_widget.height()
        parent_width = self.sequence_widget.width()
        desired_height = self.sequence_widget.graph_editor.get_graph_editor_height()

        if show:
            editor_start_rect = QRect(0, parent_height, parent_width, 0)
            editor_end_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            toggle_start_pos = QPoint(0, parent_height - self.toggle_tab.height())
            toggle_end_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            placeholder_start_height = 0
            placeholder_end_height = desired_height
        else:
            editor_start_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            editor_end_rect = QRect(0, parent_height, parent_width, 0)
            toggle_start_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            toggle_end_pos = QPoint(0, parent_height - self.toggle_tab.height())
            placeholder_start_height = desired_height
            placeholder_end_height = 0

        # Animate GraphEditor geometry
        graph_editor_animation = QPropertyAnimation(self.graph_editor, b"geometry")
        graph_editor_animation.setStartValue(editor_start_rect)
        graph_editor_animation.setEndValue(editor_end_rect)
        graph_editor_animation.setDuration(300)
        graph_editor_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(graph_editor_animation)

        # Animate graph editor placeholder height
        placeholder_animation = QPropertyAnimation(
            self.graph_editor_placeholder, b"minimumHeight"
        )
        placeholder_animation.setStartValue(placeholder_start_height)
        placeholder_animation.setEndValue(placeholder_end_height)
        placeholder_animation.setDuration(300)
        placeholder_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(placeholder_animation)

        # Animate toggle tab position
        toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        toggle_tab_animation.setStartValue(toggle_start_pos)
        toggle_tab_animation.setEndValue(toggle_end_pos)
        toggle_tab_animation.setDuration(300)
        toggle_tab_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(toggle_tab_animation)

        # Handle cleanup on collapse
        if not show:
            graph_editor_animation.finished.connect(
                lambda: self.sequence_widget.layout_manager.main_layout.removeWidget(
                    self.graph_editor_placeholder
                )
            )
            graph_editor_animation.finished.connect(self.graph_editor.hide)

        # Start all animations
        for animation in self.current_animations:
            animation.start()
