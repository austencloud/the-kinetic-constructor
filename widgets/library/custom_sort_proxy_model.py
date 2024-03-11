from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex


class CustomSortProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lengthSortingEnabled = False

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        if self.lengthSortingEnabled:
            leftData = self.sourceModel().fileName(left)
            rightData = self.sourceModel().fileName(right)
            leftLength = self.compute_display_length(leftData)
            rightLength = self.compute_display_length(rightData)
            return leftLength < rightLength
        else:
            return super().lessThan(left, right)

    @staticmethod
    def compute_display_length(name: str) -> int:
        count = 0
        skip_next = False
        for i, char in enumerate(name):
            if skip_next:
                skip_next = False
                continue
            if char == "-" and i + 1 < len(name):
                count += 1
                skip_next = True
            else:
                count += 1
        return count
