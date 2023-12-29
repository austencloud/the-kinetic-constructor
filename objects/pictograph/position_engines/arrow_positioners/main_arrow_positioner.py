from objects.pictograph.pictograph import Pictograph
from typing import Dict, List
from Enums import Letter
from objects.pictograph.pictograph import (
    Type1_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
)
from .base_arrow_positioner import BaseArrowPositioner

class MainArrowPositioner:
    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.letters: Dict[Letter, List[Dict[str, str]]] = scene.main_widget.letters
        self.init_arrow_positioners(scene)

    def init_arrow_positioners(self, scene) -> None:
        pass

    def position_props(self) -> None:
        positioner: BaseArrowPositioner = self.positioners.get(
            self.scene.current_letter
        )
        if positioner:
            positioner.update_prop_positions()
