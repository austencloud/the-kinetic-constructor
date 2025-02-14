from enum import IntEnum


class LeftStackIndex(IntEnum):
    WORKBENCH = 0
    LEARN_CODEX = 1
    WRITE_ACT_SHEET = 2
    FILTER_SELECTOR = 3
    SEQUENCE_PICKER = 4


class RightStackIndex(IntEnum):
    START_POS_PICKER = 0
    ADVANCED_START_POS_PICKER = 1
    OPTION_PICKER = 2
    GENERATE_TAB = 3
    LEARN_TAB = 4
    WRITE_TAB = 5
    SEQUENCE_VIEWER = 6
