from typing import TYPE_CHECKING, Dict
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class AdjustmentMapper:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def apply_adjustment_to_arrow(self, arrow: Arrow):
        adjustment_key = self.positioner.turns_tuple_generator.generate_turns_tuple(arrow.scene.letter)
        special_rotation = self._check_for_special_rotation(arrow, adjustment_key)

        if special_rotation:
            self._apply_special_rotation(arrow, special_rotation)
        else:
            # Apply regular adjustment if no special rotation
            adjustment = self.positioner.adjustment_calculator.calculate_turns_tuple(arrow, adjustment_key)
            if adjustment:
                self._apply_adjustment(arrow, adjustment)

    def _check_for_special_rotation(self, arrow: Arrow, adjustment_key: str):
        placements = self.positioner.placement_manager.pictograph.main_widget.special_placements
        letter_data: Dict[str, Dict] = placements.get(self.positioner.pictograph.letter, {})
        prop_rot_dir = arrow.motion.prop_rot_dir
        special_rotation_key = f"{prop_rot_dir}_static"

        # Check if the special rotation key exists in the letter data
        return letter_data.get(adjustment_key, {}).get(special_rotation_key)

    def _apply_special_rotation(self, arrow: Arrow, special_rotation):
        # Apply the special rotation to the arrow
        # Assuming special_rotation is a dict with specific properties to apply
        # Example: {'x': 100, 'y': 100, 'rotation': 45}
        arrow.setPos(special_rotation.get('x', arrow.x()), special_rotation.get('y', arrow.y()))
        arrow.setRotation(special_rotation.get('rotation', arrow.rotation()))