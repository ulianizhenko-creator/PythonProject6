# game_objects.py
import arcade
import random
import math
from constants import *

# ------------------------------------------------------------------
# Вспомогательная функция – безопасно выбирает X‑координату,
# гарантируя, что левый и правый пределы не «пересекаются».
# ------------------------------------------------------------------
def safe_random_x(sprite: arcade.Sprite) -> int:
    """
    Возвращает случайную X‑позицию, позволяя спрайту полностью помещаться
    на экране. Если спрайт шире экрана, возвращаем центр экрана.
    """
    half = sprite.width / 2
    min_x = int(half)
    max_x = int(SCREEN_WIDTH - half)

    # Если ширина спрайта > ширина экрана, min_x будет > max_x
    if min_x > max_x:
        return SCREEN_WIDTH // 2
    return random.randint(min_x, max_x)


# ------------------------------------------------------------------
# ПУЛИ
# ------------------------------------------------------------------
class Bullet(arcade.Sprite):
    """Пуля, используемая как игроком, так и врагами."""
    def __init__(self, x, y, angle, speed, friendly=True):
        super().__init__(BULLET_IMAGE, 0.8)
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.speed = speed
        self.friendly = friendly
        self.change_x = math.cos(math.radians(angle)) * speed
        self.change_y = math.sin(math.radians(angle)) * speed
        if not self.friendly:
            self.color = arcade.color.RED

    def update(self, delta_time: float = 0):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Удаляем пулю, если она ушла за пределы экрана
        if (self.bottom > SCREEN_HEIGHT or self.top < 0 or
                self.right < 0 or self.left > SCREEN_WIDTH):
            self.remove_from_sprite_lists()


# ------------------------------------------------------------------
# АСТЕРОИДЫ
# ------------------------------------------------------------------
class Asteroid(arcade.Sprite):
    """Астероид, падающий сверху вниз."""
    def __init__(self):
        super().__init__(ASTEROID_IMAGE,
                         random.uniform(0.5, 1.5))

        # Безопасно ставим X‑координату
        self.center_x = safe_random_x(self)

        self.center_y = SCREEN_HEIGHT + self.height
        self.change_y = -random.uniform(ASTEROID_SPEED_MIN,
                                        ASTEROID_SPEED_MAX)
        self.change_angle = random.uniform(-3, 3)

    def update(self, delta_time: float = 0):
        self.center_y += self.change_y
        self.angle += self.change_angle
        if self.bottom < 0:
            self.remove_from_sprite_lists()


# ------------------------------------------------------------------
# УСИЛЕНИЯ (POWER‑UPS)
# ------------------------------------------------------------------
class PowerUp(arcade.Sprite):
    """Базовый класс усовершенствований."""
    def __init__(self, image_path: str, power_type: str):
        super().__init__(image_path, 0.8)
        self.center_x = safe_random_x(self)
        self.center_y = SCREEN_HEIGHT + self.height
        self.change_y = -2
        self.power_type = power_type   # "shield" | "rapid_fire"

    def update(self, delta_time: float = 0):
        self.center_y += self.change_y
        self.angle += 1
        if self.bottom < 0:
            self.remove_from_sprite_lists()


class ShieldPowerUp(PowerUp):
    """Щитовый power‑up."""
    def __init__(self):
        super().__init__(POWERUP_SHIELD_IMAGE, "shield")


class RapidFirePowerUp(PowerUp):
    """Ускоряющий fire‑rate power‑up."""
    def __init__(self):
        super().__init__(POWERUP_RAPID_FIRE_IMAGE, "rapid_fire")


# ------------------------------------------------------------------
# ФОН (звёздное небо)
# ------------------------------------------------------------------
class Star(arcade.Sprite):
    """Один паттерн звезды для фонового эффекта."""
    def __init__(self):
        super().__init__(STAR_BG_IMAGE)
        # Звёзды маленькие, но всё равно используем safe_random_x
        self.center_x = safe_random_x(self)
        self.center_y = random.randint(0, SCREEN_HEIGHT)
        self.alpha = random.randint(50, 200)
        self.speed = random.uniform(0.2, 1.5)

    def update(self, delta_time: float = 0):
        self.center_y -= self.speed
        if self.bottom < 0:
            self.center_y = SCREEN_HEIGHT
            self.center_x = safe_random_x(self)
