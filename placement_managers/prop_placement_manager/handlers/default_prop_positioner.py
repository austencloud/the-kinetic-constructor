# default_prop_positioner.py

from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Dict
from objects.prop.prop import Prop
import logging

if TYPE_CHECKING:
    from objects.grid import GridPoint
    from ..prop_placement_manager import PropPlacementManager
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

logger = logging.getLogger(__name__)

class DefaultPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph: "BasePictograph" = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager
        self.location_points_cache = {}
    

    def set_prop_to_default_loc(self, prop: Prop) -> None:
        """
        Sets the prop to its default location based on its `loc` attribute.
        """
        # Determine whether to use strictly placed props
        strict = self.pictograph.check.has_strictly_placed_props()
        location_points = self.get_location_points(strict)

        # Construct the exact point name
        grid_mode = self.pictograph.grid.grid_mode
        point_suffix = "_strict" if strict else ""
        point_name = f"{prop.loc}_{grid_mode}_hand_point{point_suffix}"

        logger.debug(f"Attempting to place prop '{prop}' at point '{point_name}'.")

        # Retrieve the GridPoint
        grid_point = (
            self.pictograph.grid.grid_data.all_hand_points_strict.get(point_name)
            if strict
            else self.pictograph.grid.grid_data.all_hand_points_normal.get(point_name)
        )

        if grid_point and grid_point.coordinates:
            logger.debug(f"Found coordinates for '{point_name}': {grid_point.coordinates}.")
            self.place_prop_at_hand_point(prop, grid_point.coordinates)
        else:
            logger.warning(f"Hand point '{point_name}' not found or has no coordinates.")

        
    def place_prop_at_hand_point(self, prop: Prop, hand_point: QPointF) -> None:
        """
        Align the prop's center to the hand point using the 'centerPoint' defined in the SVG.
        """
        # Get the center point from the SVG by using the renderer and the centerPoint ID
        center_point_in_svg = self.get_svg_center_point(prop)
    
        # Map the SVG center point to scene coordinates
        center_point_in_scene = prop.mapToScene(center_point_in_svg)
    
        # Calculate the offset between the center point and the hand point
        offset = hand_point - center_point_in_scene
    
        # Apply the offset to the prop's current position
        new_position = prop.pos() + offset
        prop.setPos(new_position)
    
    def get_svg_center_point(self, prop: Prop) -> QPointF:
        """
        Retrieve the 'centerPoint' from the SVG.
        """
        # Use the QSvgRenderer to retrieve the coordinates of the 'centerPoint'
        element_bounding_box = prop.renderer.boundsOnElement("centerPoint")
        center_point_in_svg = element_bounding_box.center()
    
        return center_point_in_svg
    
    def get_location_points(self, strict: bool) -> Dict[str, "GridPoint"]:
        """
        Returns hand location points, depending on whether the props should be strictly placed.
        """
        location_points = (
            self.pictograph.grid.grid_data.all_hand_points_strict
            if strict
            else self.pictograph.grid.grid_data.all_hand_points_normal
        )
        return location_points  # Correct access without .points
