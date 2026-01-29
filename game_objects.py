# game_objects.py
import arcade
import random
import math
from constants import *


class Bullet(arcade.Sprite):
    """Класс для пуль, выпускаемых как игроком, так и врагами."""

    def __init__(self, x, y, angle, speed, friendly=True):
        super().__init__(BULLET_IMAGE, 0.8)
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.speed = speed
        self.friendly = friendly

        # На самом деле arcade.Sprite использует angle в градусах, но change_x/y не зависит от angle
        # Поэтому вручную рассчитываем вектор скорости
        self.change_x = math.cos(math.radians(angle)) * speed
        self.change_y = math.sin(math.radians(angle)) * speed

        if not self.friendly:
            self.color = arcade.color.RED
            self.texture = arcade.load_texture(BULLET_IMAGE, tinted_color=arcade.color.RED)

    def on_update(self, delta_time: float):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Удаляем пулю, если она ушла за пределы экрана
        if self.bottom > SCREEN_HEIGHT or self.top < 0 or self.right < 0 or self.left > SCREEN_WIDTH:
            self.remove_from_sprite_lists()


class Asteroid(arcade.Sprite):
    """Класс для астероидов."""

    def __init__(self):
        super().__init__(ASTEROID_IMAGE, random.uniform(0.5, 1.5))
        # Появляется сверху экрана в случайной X позиции
        self.center_x = random.randint(self.width, SCREEN_WIDTH - self.width)
        self.center_y = SCREEN_HEIGHT + self.height
        self.change_y = -random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        # Случайная скорость и направление вращения
        self.change_angle = random.uniform(-3, 3)

    def on_update(self, delta_time: float):
        self.center_y += self.change_y
        self.angle += self.change_angle
        if self.bottom < 0:
            self.remove_from_sprite_lists()


class PowerUp(arcade.Sprite):
    """Базовый класс для усилений."""

    def __init__(self, image_path, power_type):
        super().__init__(image_path, 0.8)
        self.center_x = random.randint(self.width, SCREEN_WIDTH - self.width)
        self.center_y = SCREEN_HEIGHT + self.height
        self.change_y = -2
        self.power_type = power_type  # Например, "shield", "rapid_fire"

    def on_update(self, delta_time: float):
        self.center_y += self.change_y
        self.angle += 1
        if self.bottom < 0:
            self.remove_from_sprite_lists()


class ShieldPowerUp(PowerUp):
    """Усиление "Щит"."""

    def __init__(self):
        super().__init__(POWERUP_SHIELD_IMAGE, "shield")


class RapidFirePowerUp(PowerUp):
    """Усиление "Скорострельность"."""

    def __init__(self):
        super().__init__(POWERUP_RAPID_FIRE_IMAGE, "rapid_fire")


class Star(arcade.Sprite):
    """Звезда для фонового эффекта."""

    def __init__(self):
        super().__init__(STAR_BG_IMAGE)
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = random.randint(0, SCREEN_HEIGHT)
        self.alpha = random.randint(50, 200)
        self.speed = random.uniform(0.2, 1.5)

    def on_update(self, delta_time: float):
        self.center_y -= self.speed
        # Когда звезда уходит за нижний край экрана, перемещаем ее наверх
        if self.bottom < 0:
            self.center_y = SCREEN_HEIGHT
            self.center_x = random.randint(0, SCREEN_WIDTH)

