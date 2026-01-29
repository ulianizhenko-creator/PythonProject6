# player.py
import arcade
import math
from constants import *


class Player(arcade.Sprite):
    """Класс корабля игрока."""

    def __init__(self):
        super().__init__(PLAYER_IMAGE, 0.8)
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.lives = PLAYER_LIVES
        self.max_lives = PLAYER_LIVES
        self.shield_active = False
        self.shield_timer = 0
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.fire_cooldown = 0
        self.base_fire_rate = 10  # Кадры между выстрелами
        self.current_fire_rate = self.base_fire_rate

    def update(self):
        # Обновляем таймеры усилений
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.rapid_fire_active:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False
                self.current_fire_rate = self.base_fire_rate
        else:
            self.current_fire_rate = self.base_fire_rate

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Ограничение движения в пределах экрана
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT

    def can_fire(self):
        return self.fire_cooldown <= 0

    def fire(self, bullet_list):
        if self.can_fire():
            bullet = Bullet(self.center_x, self.center_y + 20, 90, 10, friendly=True)
            bullet_list.append(bullet)
            arcade.play_sound(arcade.sound.load(LASER_SOUND))
            self.fire_cooldown = self.current_fire_rate

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 300  # ~5 секунд при 60 FPS

    def activate_rapid_fire(self):
        self.rapid_fire_active = True
        self.rapid_fire_timer = 450  # ~7.5 секунд
        self.current_fire_rate = 3  # Увеличиваем скорострельность

    def take_damage(self):
        if not self.shield_active:
            self.lives -= 1
            # Эффект получения урона (мерцание)
            self.alpha = 128
            return True
        return False

