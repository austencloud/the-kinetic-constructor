from PyQt6.QtWidgets import QLayout, QLayoutItem
from PyQt6.QtCore import QRect, QSize, QPoint

class FlowLayout(QLayout):
    def __init__(self, parent=None, spacing=5):
        super().__init__(parent)
        self._item_list = []
        self.setSpacing(spacing)

    def addItem(self, item: QLayoutItem):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return 0

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._layout_items(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._layout_items(rect, False)

    def sizeHint(self):
        return QSize(200, 150)

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        return size

    def _layout_items(self, rect, test_only):
        x, y = rect.x(), rect.y()
        line_height = 0

        for item in self._item_list:
            widget_size = item.sizeHint()
            next_x = x + widget_size.width() + self.spacing()
            if next_x - self.spacing() > rect.right() and line_height > 0:
                x = rect.x()
                y += line_height + self.spacing()
                next_x = x + widget_size.width() + self.spacing()
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), widget_size))

            x = next_x
            line_height = max(line_height, widget_size.height())

        return y + line_height - rect.y()
