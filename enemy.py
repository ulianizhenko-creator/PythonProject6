# enemy.py
import arcade
import random
import math
from constants import *


class BasicEnemy(arcade.Sprite):
    """Простой враг, двигающийся вниз."""

    def __init__(self, y_position=SCREEN_HEIGHT):
        super().__init__(ENEMY_BASIC_IMAGE, 0.7)
        self.center_x = random.randint(self.width, SCREEN_WIDTH - self.width)
        self.center_y = y_position
        self.change_y = -ENEMY_SPEED_BASE
        self.bullet_list = arcade.SpriteList()
        self.health = 2

    def on_update(self, delta_time: float):
        self.center_y += self.change_y
        if self.bottom < 0:
            self.remove_from_sprite_lists()

        # Простая логика стрельбы: стреляет с небольшой вероятностью
        if random.random() < ENEMY_SHOOT_PROBABILITY:
            self.fire()

    def fire(self, player):
        """Выстрел в сторону игрока."""
        if not player: return

        # Расчет угла для стрельбы в направлении игрока
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        angle = math.degrees(math.atan2(dy, dx))

        bullet = Bullet(self.center_x, self.center_y - 15, angle, 4, friendly=False)
        self.bullet_list.append(bullet)
        # arcade.play_sound(arcade.sound.load(LASER_SOUND)) # Можно добавить свой звук для врагов

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.remove_from_sprite_lists()
            return True  # Враг уничтожен
        return False

