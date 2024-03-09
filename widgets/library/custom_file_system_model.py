from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDateTime, Qt

class CustomFileSystemModel(QFileSystemModel):
    def columnCount(self, parent=None):
        # Only show 2 columns: name and date modified
        return 2

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Custom Name"
            elif section == 1:
                return "Custom Date Modified"
        return super().headerData(section, orientation, role)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 1:
                # Only change the display for the "Custom Date Modified" column
                # Assuming that the date modified is in the original 3rd column (index 2)
                date_time = super().data(index.siblingAtColumn(2), role)
                # Convert the QDateTime to just a date string in the desired format
                if isinstance(date_time, QDateTime):
                    return date_time.toString("d/M/yy")
            elif index.column() == 0:
                # For the "Custom Name" column, return the filename as usual
                return super().data(index, role)
        elif role == Qt.ItemDataRole.DecorationRole and index.column() == 0:
            # Provide an icon for the first column if needed
            return super().data(index, role)
        return None  # Don't return any data for size and type columns
