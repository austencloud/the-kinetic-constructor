from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDateTime, Qt

class CustomFileSystemModel(QFileSystemModel):
    def columnCount(self, parent=None) -> int:
        return 1

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole) -> str:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Word"

        return super().headerData(section, orientation, role)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 1:
                date_time = super().data(index.siblingAtColumn(2), role)
                if isinstance(date_time, QDateTime):
                    return date_time.toString("d/M/yy")
            elif index.column() == 0:
                return super().data(index, role)
        elif role == Qt.ItemDataRole.DecorationRole and index.column() == 0:
            return super().data(index, role)
        return None
