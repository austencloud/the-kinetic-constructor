# utils.py
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from utilities.TypeChecking.TypeChecking import VtgDirections

def load_svg_item(svg_path: str) -> QGraphicsSvgItem:
    renderer = QSvgRenderer(svg_path)
    if renderer.isValid():
        item = QGraphicsSvgItem()
        item.setSharedRenderer(renderer)
        return item
    return None


def parse_turns_tuple_string(turns_str: str) -> tuple:
    parts = turns_str.strip("()").split(",")
    turns_list = []

    for item in parts:
        item = item.strip()  # Strip extra spaces
        if item in ["0.5", "1.5", "2.5"]:
            item = float(item)
        elif item in ["0", "1", "2", "3"]:
            item = int(item)
        elif item == "s":
            item = VtgDirections.SAME
        elif item == "o":
            item = VtgDirections.OPP
        turns_list.append(item)
    if len(turns_list) == 3:
        return turns_list[0], turns_list[1], turns_list[2]
    else:
        return None, turns_list[0], turns_list[1]