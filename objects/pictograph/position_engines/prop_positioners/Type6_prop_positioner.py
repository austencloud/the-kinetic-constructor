from Enums import (
    non_strictly_placed_props,
    strictly_placed_props,
    Direction,
)
from constants import (
    RADIAL,
    ANTIRADIAL,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    RED,
    BLUE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from objects.pictograph.position_engines.base_prop_positioner import BasePropPositioner
from objects.prop.prop import Prop


class Type6PropPositioner(BasePropPositioner):
    def reposition_β(self) -> None:
        moved_props = set()

        for color, motion in self.scene.motions.items():
            prop = next((p for p in self.props if p.color == color), None)
            if not prop or prop in moved_props:
                continue

            other_prop = next(
                (
                    other
                    for other in self.props
                    if other != prop and other.location == prop.location
                ),
                None,
            )

            if other_prop and (
                (other_prop.is_radial() and prop.is_radial())
                or (other_prop.is_antiradial() and prop.is_antiradial())
            ):
                if prop.prop_type in non_strictly_placed_props:
                    direction = self._get_translation_dir_for_static_beta(prop)
                    if direction:
                        self._move_prop(prop, direction)
                        moved_props.add(prop)  # Mark this prop as moved
                elif prop.prop_type in strictly_placed_props:
                    self._set_strict_prop_location(other_prop)

    def _get_translation_dir_for_static_beta(self, prop: Prop) -> Direction | None:
        layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
                (EAST, BLUE): DOWN,
            },
            ANTIRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT,
                (WEST, BLUE): LEFT,
                (WEST, RED): RIGHT,
                (EAST, BLUE): LEFT,
            },
        }
        if prop.is_radial():
            return layer_reposition_map[RADIAL][(prop.location, prop.color)]
        elif prop.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.location, prop.color)]
