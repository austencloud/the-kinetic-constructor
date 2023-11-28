import re
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QPointF, QSize
from objects.arrow import Arrow
from objects.props.props import Prop
from objects.grid import Grid
import xml.etree.ElementTree as ET
from copy import deepcopy
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from utilities.TypeChecking.TypeChecking import ColorHex


class ExportHandler:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.pictograph = main_widget.graph_editor.pictograph
        self.grid = self.pictograph.grid
        self.get_fill_color(self.grid.svg_file)
        self.export_to_png()

    ### EXPORTERS ###

    def export_to_png(self) -> None:
        selectedItems = self.pictograph.selectedItems()
        image = QImage(
            QSize(int(self.pictograph.width()), int(self.pictograph.height())),
            QImage.Format.Format_ARGB32,
        )
        painter = QPainter(image)

        for item in selectedItems:
            item.setSelected(False)

        self.pictograph.render(painter)
        painter.end()
        image.save("export.png")

        for item in selectedItems:
            item.setSelected(True)

    def export_to_svg(self, output_file_path: str) -> None:
        nsmap = {"svg": "SVG_NS"}
        ET.register_namespace("", nsmap["svg"])

        # Create the root element for the SVG
        svg_data = ET.Element("{SVG_NS}svg")
        svg_data.set("width", "750")
        svg_data.set("height", "900")
        svg_data.set("viewBox", "0 0 750 900")

        # Create groups for staffs, arrows, and the grid
        staffs_group = ET.SubElement(svg_data, "{SVG_NS}g", id="staffs")
        arrows_group = ET.SubElement(svg_data, "{SVG_NS}g", id="arrows")
        grid_group = ET.SubElement(svg_data, "{SVG_NS}g", id="grid")

        for item in self.pictograph.items():
            if isinstance(item, Grid):
                circle_elements = self.get_circle_elements(item)
                grid_group.append(circle_elements)

            elif isinstance(item, Arrow):
                arrow_path_element = self.get_arrow_path_element(item)
                arrows_group.append(arrow_path_element)

            elif isinstance(item, Prop):
                staff_rect_element = self.get_staff_rect_element(item)
                staffs_group.append(staff_rect_element)

        svg_data.append(ET.Comment(" staffs "))
        svg_data.append(staffs_group)
        svg_data.append(ET.Comment(" ARROWS "))
        svg_data.append(arrows_group)
        svg_data.append(ET.Comment(" GRID "))
        svg_data.append(grid_group)
        svg_string = ET.tostring(svg_data, encoding="unicode", method="xml")

        svg_string = svg_string.replace(">\n<", ">\n\n<")
        with open(output_file_path, "w") as file:
            file.write(svg_string)

    ### GETTERS ###

    def get_circle_elements(self, item: Grid) -> List[ET.Element]:
        grid_svg_data = ET.parse(item.svg_file)
        circle_elements: List[ET.Element] = grid_svg_data.getroot().findall(
            ".//{SVG_NS}circle"
        )
        for circle_element in circle_elements:
            cx = float(circle_element.get("cx")) + 50
            cy = float(circle_element.get("cy")) + 50
            circle_element.set("cx", str(cx))
            circle_element.set("cy", str(cy))

        return circle_elements

    def get_arrow_path_element(self, arrow: "Arrow") -> ET.Element:
        arrow_svg_data = ET.parse(arrow.svg_file)
        path_elements = arrow_svg_data.getroot().findall(".//{SVG_NS}path")
        fill_color = self.get_fill_color(arrow.svg_file)
        transform = arrow.transform()

        for path_element in path_elements:
            path_element.set(
                "transform",
                f"matrix({transform.m11()}, {transform.m12()}, {transform.m21()}, {transform.m22()}, {arrow.x()}, {arrow.y()})",
            )
            if fill_color is not None:
                path_element.set("fill", fill_color)

        return path_elements[0]

    def get_staff_rect_element(self, staff: "Prop") -> ET.Element:
        staff_svg_data = ET.parse(staff.svg_file)
        rect_elements = staff_svg_data.getroot().findall(".//{SVG_NS}rect")
        fill_color = self.get_fill_color(staff.svg_file)
        position = staff.pos()

        for rect_element in rect_elements:
            rect_element_copy = deepcopy(rect_element)
            rect_element_copy.set("x", str(position.x()))
            rect_element_copy.set("y", str(position.y()))
            rect_element_copy.set("transform", f"matrix(1.0, 0.0, 0.0, 1.0, 0, 0)")
            if fill_color is not None:
                rect_element_copy.set("fill", fill_color)

        return rect_elements[0]

    def get_staff_position(self, staff: "Prop") -> QPointF:
        staff_svg = ET.parse(staff.svg_file)
        rect_elements = staff_svg.getroot().findall(".//{SVG_NS}rect")
        position = None

        for rect_element in rect_elements:
            if "x" in rect_element.attrib and "y" in rect_element.attrib:
                position = QPointF(
                    float(rect_element.attrib["x"]), float(rect_element.attrib["y"])
                )
                break

        return position

    def get_fill_color(self, svg_file) -> ColorHex | None:
        svg_data = ET.parse(svg_file)
        fill_color: ColorHex | None = None

        # Try to get fill color from style element
        style_element = svg_data.getroot().find(".//{SVG_NS}style")
        if style_element is not None:
            style_text = style_element.text
            color_match: re.Match | None = re.search(
                r"fill:\s*(#[0-9a-fA-F]+)", style_text
            )
            if color_match:
                fill_color = color_match.group(1)

        # If fill color was not found in style element, try to get it from path or rect elements
        if fill_color is None:
            for element in svg_data.getroot().iterfind(".//{SVG_NS}*"):
                if "fill" in element.attrib:
                    fill_color = element.attrib["fill"]
                    break

        return fill_color
