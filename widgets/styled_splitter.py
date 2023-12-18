from PyQt6.QtWidgets import QSplitter, QStyleOption, QStyle
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QLinearGradient, QBrush, QPen
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtWidgets import QSplitterHandle
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt


class StyledSplitter(QSplitter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHandleWidth(10)  # Set the handle width

    def createHandle(self):
        return StyledSplitterHandle(self.orientation(), self)  # Create a custom handle

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, option, painter, self
        )

        # Call the base class paintEvent to draw the splitter handle
        super().paintEvent(event)
        
class StyledSplitterHandle(QSplitterHandle):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Customize the appearance of the splitter handle
        handle_color = QColor(100, 100, 100)
        handle_pen = QPen(handle_color, 2, Qt.PenStyle.SolidLine)

        # Draw a rectangle representing the splitter handle
        painter.setPen(handle_pen)
        painter.drawRect(self.rect())

