from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceValidationOriCalculator:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def calculate_end_orientation(self, entry, color):
        """Calculate the end orientation based on the JSON entry data."""
        motion_type = entry[f"{color}_motion_type"]
        turns = float(entry[f"{color}_turns"])
        start_ori = entry[f"{color}_start_ori"]
        prop_rot_dir = entry.get(
            f"{color}_prop_rot_dir", "cw"
        )  # Assuming 'cw' as default

        if motion_type in ["pro", "static"]:
            return self.calculate_pro_static_orientation(start_ori, turns, prop_rot_dir)
        elif motion_type in ["anti", "dash"]:
            return self.calculate_anti_dash_orientation(start_ori, turns, prop_rot_dir)

        return start_ori  # Default return if no specific logic matches

    def calculate_pro_static_orientation(self, start_ori, turns, prop_rot_dir):
        """Calculates the end orientation for 'pro' and 'static' motions."""
        # This logic needs to be refined based on specific rules for how 'pro' and 'static' affect orientation
        if turns % 2 == 0:
            return start_ori  # No change for an even number of full turns
        else:
            # For half turns, the orientation changes based on the prop rotation direction
            if prop_rot_dir == "cw":
                return {
                    "in": "clock",
                    "out": "counter",
                    "clock": "out",
                    "counter": "in",
                }.get(start_ori, start_ori)
            else:  # "ccw"
                return {
                    "in": "counter",
                    "out": "clock",
                    "clock": "in",
                    "counter": "out",
                }.get(start_ori, start_ori)

    def calculate_anti_dash_orientation(self, start_ori, turns, prop_rot_dir):
        """Calculates the end orientation for 'anti' and 'dash' motions."""
        if turns == 0:
            return self.switch_orientation(start_ori)
        elif turns % 2 == 0:
            return self.switch_orientation(start_ori)
        else:
            # For half turns, adjust based on rotation direction, this is a placeholder
            return start_ori  # Placeholder logic

    def switch_orientation(self, ori):
        """Switches orientation between 'in'/'out' and 'clock'/'counter'."""
        return {"in": "out", "out": "in", "clock": "counter", "counter": "clock"}.get(
            ori, ori
        )
