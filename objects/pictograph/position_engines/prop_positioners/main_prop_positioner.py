from Enums import Letter
from typing import TYPE_CHECKING, Dict, List

from objects.pictograph.position_engines.prop_positioners.base_prop_positioner import (
    BasePropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type1_prop_positioner import (
    Type1PropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type2_prop_positioner import (
    Type2PropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type3_prop_positioner import (
    Type3PropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type4_prop_positioner import (
    Type4PropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type5_prop_positioner import (
    Type5PropPositioner,
)
from objects.pictograph.position_engines.prop_positioners.by_letter_type.Type6_prop_positioner import (
    Type6PropPositioner,
)

from utilities.TypeChecking.Letters import (
    Type1_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
)


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class MainPropPositioner:
    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.init_prop_positioners(scene)

    def init_prop_positioners(self, scene) -> None:
        letter_to_positioner = {
            **{letter: Type1PropPositioner for letter in Type1_letters},
            **{letter: Type2PropPositioner for letter in Type2_letters},
            **{letter: Type3PropPositioner for letter in Type3_letters},
            **{letter: Type4PropPositioner for letter in Type4_letters},
            **{letter: Type5PropPositioner for letter in Type5_letters},
            **{letter: Type6PropPositioner for letter in Type6_letters},
            **{None: BasePropPositioner},
        }

        self.positioners = {
            letter: pos_class(scene)
            for letter, pos_class in letter_to_positioner.items()
        }

    def position_props(self) -> None:
        positioner: BasePropPositioner = self.positioners[self.scene.current_letter]
        positioner.update_prop_positions()
