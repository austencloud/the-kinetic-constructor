from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class BaseQuestionWidget(QWidget):
    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget

    def clear(self) -> None:
        raise NotImplementedError("This function should be implemented by the subclass.")

    def resize_question_widget(self) -> None:
        raise NotImplementedError("This function should be implemented by the subclass.")
    
    def load_pictograph(self, pictograph_dict) -> None:
        raise NotImplementedError("This function should be implemented by the subclass.")
    
    