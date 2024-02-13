from constants import (
    BLUE_END_LOC,
    BLUE_END_ORI,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    END_POS,
    LETTER,
    RED_END_LOC,
    RED_END_ORI,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    START_POS,
)


class PictographKeyGenerator:
    @staticmethod
    def generate_pictograph_key(pictograph_dict: dict) -> str:
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[BLUE_START_ORI]}→{pictograph_dict[BLUE_END_ORI]}_"
            f"{pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
            f"_{pictograph_dict[RED_START_ORI]}→{pictograph_dict[RED_END_ORI]}"
        )
