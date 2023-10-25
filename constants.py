
GRAPHBOARD_SCALE = .4
PICTOGRAPH_SCALE = .2

MAIN_WINDOW_WIDTH = int(2600 * GRAPHBOARD_SCALE)
MAIN_WINDOW_HEIGHT = int(3000 * GRAPHBOARD_SCALE)

STAFF_WIDTH = 25
STAFF_LENGTH = 250

DEFAULT_GRAPHBOARD_HEIGHT = 900
DEFAULT_GRAPHBOARD_WIDTH = 750
DEFAULT_GRID_WIDTH = 650
DEFAULT_GRID_PADDING = ((DEFAULT_GRAPHBOARD_HEIGHT - DEFAULT_GRID_WIDTH) / 2)

GRAPHBOARD_HEIGHT = DEFAULT_GRAPHBOARD_HEIGHT * GRAPHBOARD_SCALE
GRAPHBOARD_WIDTH = DEFAULT_GRAPHBOARD_WIDTH * GRAPHBOARD_SCALE
GRAPHBOARD_GRID_WIDTH = 650 * GRAPHBOARD_SCALE
GRAPHBOARD_GRID_PADDING = ((GRAPHBOARD_WIDTH - GRAPHBOARD_GRID_WIDTH) / 2)

VERTICAL_OFFSET = (GRAPHBOARD_HEIGHT - GRAPHBOARD_WIDTH) / 2


ARROW_DIR = 'images/arrows'

ARROW_ADJUSTMENT_DISTANCE = 40 * GRAPHBOARD_SCALE

PICTOGRAPH_GRID_WIDTH = DEFAULT_GRID_WIDTH * PICTOGRAPH_SCALE
PICTOGRAPH_WIDTH = int(DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE)
PICTOGRAPH_HEIGHT = int(DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE)
PICTOGRAPH_GRID_PADDING = ((PICTOGRAPH_WIDTH - PICTOGRAPH_GRID_WIDTH) / 2)

BETA_STAFF_REPOSITION_OFFSET = 20

RED = '#ed1c24'
BLUE = '#2e3192'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

COLOR_MAP = {
    "red": "#ed1c24",
    "blue": "#2E3192"
}