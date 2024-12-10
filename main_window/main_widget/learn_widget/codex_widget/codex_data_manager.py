# pictograph_data_manager.py

from typing import TYPE_CHECKING, Dict, Optional
from Enums.letters import Letter

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class CodexDataManager:
    """Manages the initialization and retrieval of pictograph data."""

    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.pictograph_data: Dict[str, Optional[dict]] = (
            self._initialize_pictograph_data()
        )

    def _find_pictograph_dict(
        self,
        letter_str: str,
        start_pos: str,
        end_pos: str,
        blue_motion_type: str,
        red_motion_type: str,
    ) -> Optional[dict]:
        """
        Search main_widget's preloaded pictograph_dicts for a given letter and conditions,
        including blue and red motion types. Assumes start_ori is always "in".
        """
        target_letter = None
        for l in Letter:
            if l.value == letter_str:
                target_letter = l
                break
        if not target_letter:
            print(f"Warning: Letter '{letter_str}' not found in Letter Enum.")
            return None

        letter_dicts = self.main_widget.pictograph_dicts.get(target_letter, [])
        for pdict in letter_dicts:
            if (
                pdict.get("start_pos") == start_pos
                and pdict.get("end_pos") == end_pos
                and pdict.get("blue_attributes", {}).get("motion_type")
                == blue_motion_type
                and pdict.get("red_attributes", {}).get("motion_type")
                == red_motion_type
            ):
                return pdict
        print(
            f"Warning: No matching pictograph found for letter '{letter_str}' with specified conditions."
        )
        return None

    def _initialize_pictograph_data(self) -> Dict[str, Optional[dict]]:
        """Initializes the pictograph data for all letters."""
        letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "Σ",
            "Δ",
            "θ",
            "Ω",
            "W-",
            "X-",
            "Y-",
            "Z-",
            "Σ-",
            "Δ-",
            "θ-",
            "Ω-",
            "Φ",
            "Ψ",
            "Λ",
            "Φ-",
            "Ψ-",
            "Λ-",
            "α",
            "β",
            "Γ",
        ]

        pictograph_data = {}
        for letter in letters:
            # Define the parameters based on your existing data
            # Since start_ori is always "in", we don't need to pass it
            # Adjust start_pos, end_pos, motion types as per your data
            # Here, we assume that these values are consistent with your initial code
            # You may need to adjust this based on actual data requirements

            # Example parameters (replace with actual values as needed)
            params = self._get_pictograph_params(letter)
            if params:
                pictograph_dict = self._find_pictograph_dict(
                    letter_str=letter,
                    start_pos=params["start_pos"],
                    end_pos=params["end_pos"],
                    blue_motion_type=params["blue_motion_type"],
                    red_motion_type=params["red_motion_type"],
                )
                pictograph_data[letter] = pictograph_dict
            else:
                pictograph_data[letter] = None  # Or handle as needed

        return pictograph_data

    def _get_pictograph_params(self, letter: str) -> Optional[dict]:
        """Returns the parameters for a given letter."""
        # Define the parameters based on your existing initial_pictograph_data
        # This can be refactored or loaded from a configuration file or database
        params_map = {
            "A": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "B": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "C": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "D": {
                "start_pos": "beta5",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "E": {
                "start_pos": "beta5",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "F": {
                "start_pos": "beta5",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "G": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "H": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "I": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "J": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "K": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "L": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "M": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "N": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "O": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "P": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "Q": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "R": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "S": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "T": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "U": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "V": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "anti",
            },
            "W": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "X": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Y": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Z": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Σ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Δ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "θ": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Ω": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "W-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "X-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Y-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Z-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Σ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Δ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "θ-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Ω-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Φ": {
                "start_pos": "beta7",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Ψ": {
                "start_pos": "alpha1",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Λ": {
                "start_pos": "gamma7",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Φ-": {
                "start_pos": "alpha3",
                "end_pos": "alpha7",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Ψ-": {
                "start_pos": "beta1",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Λ-": {
                "start_pos": "gamma15",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "α": {
                "start_pos": "alpha3",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "β": {
                "start_pos": "beta5",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "Γ": {
                "start_pos": "gamma11",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            # Add more letters and their parameters as needed
        }

        return params_map.get(letter)

    def get_pictograph_data(self) -> Dict[str, Optional[dict]]:
        """Returns the initialized pictograph data."""
        return self.pictograph_data
