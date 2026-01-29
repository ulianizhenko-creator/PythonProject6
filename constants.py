# constants.py
import arcade

# --- Настройки экрана ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Star Defender"

# --- Настройки игрока ---
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = 100
PLAYER_SPEED = 5
PLAYER_LIVES = 3

# --- Настройки игры ---
ENEMY_SPAWN_RATE = 0.8  # Секунды между спавном врагов
ASTEROID_SPAWN_RATE = 2.0
POWERUP_SPAWN_RATE = 8.0
GAME_DIFFICULTY_INCREASE_INTERVAL = 10 # Каждые N секунд игра усложняется

# --- Настройки врагов ---
ENEMY_SPEED_BASE = 2
ENEMY_SHOOT_PROBABILITY = 0.01 # Вероятность выстрела в каждом кадре

# --- Настройки астероидов ---
ASTEROID_COUNT_MIN = 3
ASTEROID_COUNT_MAX = 6
ASTEROID_SPEED_MIN = 1
ASTEROID_SPEED_MAX = 3

# --- Пути к ресурсам ---
ASSET_PATH = "assets/"
IMAGE_PATH = ASSET_PATH + "images/"
SOUND_PATH = ASSET_PATH + "sounds/"

PLAYER_IMAGE = IMAGE_PATH + "player_ship.jpg"
ENEMY_BASIC_IMAGE = IMAGE_PATH + "enemy_basic.jpg"
ASTEROID_IMAGE = IMAGE_PATH + "asteroid.jpg"
BULLET_IMAGE = IMAGE_PATH + "bullet.jpg"
POWERUP_SHIELD_IMAGE = IMAGE_PATH + "powerup_shield.jpg"
POWERUP_RAPID_FIRE_IMAGE = IMAGE_PATH + "powerup_rapid_fire.jpg"
STAR_BG_IMAGE = IMAGE_PATH + "star.jpg" # Для фона

# Звуковые файлы
LASER_SOUND = SOUND_PATH + "laser.wav"
EXPLOSION_SOUND = SOUND_PATH + "explosion.wav"
POWERUP_SOUND = SOUND_PATH + "powerup.wav"

# constants.py
...
# Время, в течение которого игрок неуязвим после появления (в кадрах)
PLAYER_START_INVULNERABLE_TIME = 120      # 2 секунды при 60 FPS
...


# --- Цвета ---
COLOR_BACKGROUND = arcade.color.BLACK
COLOR_TEXT = arcade.color.WHITE
COLOR_PLAYER_HIT = (255, 100, 100) # Красный оттенок при получении урона

