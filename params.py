import random

#Screen parameters
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 850

#Colours
BROWN = (139, 69, 19)
BLACK = (100, 100, 100)
LIGHT_BLUE = (100, 200, 230)
GROUND_COLOR = (0, 128, 0)

#Ground parameters
GROUND_HEIGHT = SCREEN_HEIGHT // 10
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

#Block parameters
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 70
BLOCK_HITPOINTS = 300
BLOCK_STRUCTURE = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
STRUCTURE_START_X = 100
STRUCTURE_START_Y = GROUND_Y - BLOCK_HEIGHT * 6 - 6
HORIZONTAL_SPACING = 1
VERTICAL_SPACING = 1
COLOR_DISTRIBUTION = [BROWN] * 6 + [BLACK] * 6 + [LIGHT_BLUE] * 6

#Catapult
CATAPULT_SCALE = 0.6

#Birds
BIRD_TYPES = ["Red", "Yellow", "Blue", "Black"]
BIRD_QUEUE = random.choices(BIRD_TYPES, k=10000)
current_bird_index = 0
BIRD_SCALES = {
    "Red": 0.2,
    "Yellow": 0.2,
    "Blue": 0.2,
    "Black": 0.2
}

BIRD_DAMAGE = {
    "Red": {"brown": 100, "black": 100, "light_blue": 100},
    "Yellow": {"brown": 200, "black": 50, "light_blue": 50},
    "Blue": {"brown": 50, "black": 50, "light_blue": 200},
    "Black": {"brown": 50, "black": 200, "light_blue": 50}
}

LAUNCH_POWER = 0.2
GRAVITY = 0.5
BOUNCE_DAMPENING = 0.5
MIN_VELOCITY = 1.0
MAX_PULL_DISTANCE = 200
PULL_BACK_COLOR = (255,0,0)

#Winner
WINNER_BG = "resources/images/Winner.png"