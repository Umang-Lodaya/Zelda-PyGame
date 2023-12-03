# GAME VARIABLES
WIDTH, HEIGHT = 1280, 720
FPS = 60
TILE_SIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = r"graphics\font\joystix.ttf"
UI_FONT_SIZE = 18

# GENERAL COLOR
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# UI COLOR
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# UPGRADE COLORS
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

INITIAL_STATS = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
MAX_STATS = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
UPGRADE_COST = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}

WEAPONS_DATA = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": r"graphics\weapons\sword\full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": r"graphics\weapons\lance\full.png",
    },
    "axe": {
        "cooldown": 300, 
        "damage": 20, 
        "graphic": r"graphics\weapons\axe\full.png"},
    "rapier": {
        "cooldown": 50,
        "damage": 8,
        "graphic": r"graphics\weapons\rapier\full.png",
    },
    "sai": {
        "cooldown": 80, 
        "damage": 10, 
        "graphic": r"graphics\weapons\sai\full.png"},
}

MAGIC_DATA = {
    "flame": {
        "strength": 5,
        "cost": 20,
        "graphic": r"graphics\particles\flame\fire.png",
    },
    "heal": {
        "strength": 20,
        "cost": 10,
        "graphic": r"graphics\particles\heal\heal.png",
    },
}

ENEMY_DATA = {
    "squid": {
        "health": 100,
        "exp": 100,
        "damage": 20,
        "attack_type": "slash",
        "attack_sound": r"audio\attack\slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "raccoon": {
        "health": 300,
        "exp": 250,
        "damage": 40,
        "attack_type": "claw",
        "attack_sound": r"audio\attack\claw.wav",
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "spirit": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": r"audio\attack\fireball.wav",
        "speed": 4,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 350,
    },
    "bamboo": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": r"audio\attack\slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}

