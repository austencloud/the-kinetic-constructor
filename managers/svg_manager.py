
import xml.etree.ElementTree as ET
from PyQt6.QtSvg import QSvgRenderer
import re
from xml.dom import minidom

class SvgManager():
    def set_svg_color(self, svg_file, new_color):
        color_map = {
            "red": "#ED1C24",
            "blue": "#2E3192"
        }
        new_hex_color = color_map.get(new_color)

        with open(svg_file, 'r') as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(r'\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}', re.DOTALL)
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode('utf-8')



