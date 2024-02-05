# utils.py
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

def load_svg_item(svg_path: str) -> QGraphicsSvgItem:
    renderer = QSvgRenderer(svg_path)
    if renderer.isValid():
        item = QGraphicsSvgItem()
        item.setSharedRenderer(renderer)
        return item
    return None

def add_item_to_group(group, item, position=None):
    if item:
        group.addToGroup(item)
        if position:
            item.setPos(position)
