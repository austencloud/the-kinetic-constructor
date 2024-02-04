from PyQt6.QtGui import QIcon


class IconCache:
    _cache = {}

    @staticmethod
    def get_icon(icon_path: str) -> QIcon:
        if icon_path not in IconCache._cache:
            IconCache._cache[icon_path] = QIcon(icon_path)
        return IconCache._cache[icon_path]
