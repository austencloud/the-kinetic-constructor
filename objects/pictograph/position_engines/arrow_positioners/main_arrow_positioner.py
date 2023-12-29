from objects.pictograph.pictograph import Pictograph
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type1_arrow_positioner import (
    Type1ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type2_arrow_positioner import (
    Type2ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type3_arrow_positioner import (
    Type3ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type4_arrow_positioner import (
    Type4ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type5_arrow_positioner import (
    Type5ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type6_arrow_positioner import (
    Type6ArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.base_arrow_positioner import (
    BaseArrowPositioner,
)
from utilities.TypeChecking.Letters import (
    Type1_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
)


class MainArrowPositioner:
    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.init_arrow_positioners(scene)

    def init_arrow_positioners(self, scene) -> None:
        letter_to_positioner = {
            **{letter: Type1ArrowPositioner for letter in Type1_letters},
            **{letter: Type2ArrowPositioner for letter in Type2_letters},
            **{letter: Type3ArrowPositioner for letter in Type3_letters},
            **{letter: Type4ArrowPositioner for letter in Type4_letters},
            **{letter: Type5ArrowPositioner for letter in Type5_letters},
            **{letter: Type6ArrowPositioner for letter in Type6_letters},
        }

        self.positioners = {
            letter: pos_class(scene)
            for letter, pos_class in letter_to_positioner.items()
        }

    def position_arrows(self) -> None:
        positioner: BaseArrowPositioner = self.positioners[self.scene.current_letter]
        positioner.update_arrow_positions()
