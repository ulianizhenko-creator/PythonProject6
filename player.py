# player.py
import arcade
import math
from constants import *
from game_objects import Bullet

class Player(arcade.Sprite):
    """Корабль игрока."""

    # ←‑‑ ИЗМЕНЕНИЕ: хранение звука в классе (загружается один раз)
    laser_sound = None

    def __init__(self):
        super().__init__(PLAYER_IMAGE, 0.8)

        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y

        self.lives = PLAYER_LIVES
        self.max_lives = PLAYER_LIVES

        # ←‑‑ ИЗМЕНЕНИЕ: таймер «неуязвим» сразу после появления
        self.invulnerable_timer = PLAYER_START_INVULNERABLE_TIME

        self.shield_active = False
        self.shield_timer = 0

        self.rapid_fire_active = False
        self.rapid_fire_timer = 0

        self.fire_cooldown = 0
        self.base_fire_rate = 10          # кадры между выстрелами
        self.current_fire_rate = self.base_fire_rate

    # -------------------------------------------------------------
    # Вариант update, совместимый с новыми версиями arcade
    # -------------------------------------------------------------
    def update(self, delta_time: float = 0):
        # Таймеры усилений
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.rapid_fire_active:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False
                self.current_fire_rate = self.base_fire_rate

        # Таймер неуязвимости
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            # Делать корабль слегка полупрозрачным – визуальная подсказка
            self.alpha = max(100, self.alpha - 2)

        # Охлаждение оружия
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Ограничиваем границы экрана
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT

        # После перемещения возвращаем полную непрозрачность,
        # если уже не в таймере неуязвимости
        if self.invulnerable_timer == 0:
            self.alpha = 255

    # -------------------------------------------------------------
    # Стрельба (загружаем звук только один раз)
    # -------------------------------------------------------------
    def fire(self, bullet_list: arcade.SpriteList):
        if self.can_fire():
            bullet = Bullet(self.center_x, self.center_y + 20, 90, 10, friendly=True)
            bullet_list.append(bullet)

            # Загружаем звук, если ещё не загружен
            if Player.laser_sound is None:
                Player.laser_sound = arcade.load_sound(LASER_SOUND)

            arcade.play_sound(Player.laser_sound)
            self.fire_cooldown = self.current_fire_rate

    # -------------------------------------------------------------
    def can_fire(self) -> bool:
        return self.fire_cooldown <= 0

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 300          # ≈ 5 сек

    def activate_rapid_fire(self):
        self.rapid_fire_active = True
        self.rapid_fire_timer = 450      # ≈ 7.5 сек
        self.current_fire_rate = 3

    # -------------------------------------------------------------
    # При получении урона
    # -------------------------------------------------------------
    def take_damage(self) -> bool:
        """Возвращает True, если жизнь действительно уменьшилась."""
        # Если игрок имеет активный щит – урон игнорируется
        if self.shield_active:
            return False

        # Если игрок в состоянии неуязвимости – тоже игнорируем урон
        if self.invulnerable_timer > 0:
            return False

        self.lives -= 1
        # Коротко «мигаем», показывая повреждение
        self.alpha = 128
        return True
