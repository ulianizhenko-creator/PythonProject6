# enemy.py
import arcade
import random
import math
from constants import *
from game_objects import Bullet

class BasicEnemy(arcade.Sprite):
    """Простой враг, двигающийся вниз и иногда стреляющий."""
    def __init__(self, y_position: float = SCREEN_HEIGHT):
        super().__init__(ENEMY_BASIC_IMAGE, 0.7)

        # Безопасная позиция X, аналогично Asteroid/PowerUp
        self.center_x = random.randint(
            int(self.width // 2),
            int(SCREEN_WIDTH - self.width // 2)
        ) if self.width < SCREEN_WIDTH else SCREEN_WIDTH // 2

        self.center_y = y_position
        self.change_y = -ENEMY_SPEED_BASE
        self.health = 2
        self.bullet_list = arcade.SpriteList()

    def update(self, delta_time: float = 0):
        """Перемещаем и иногда стреляем."""
        self.center_y += self.change_y
        if self.bottom < 0:
            self.remove_from_sprite_lists()
            return

        if random.random() < ENEMY_SHOOT_PROBABILITY:
            self.fire()

    def fire(self):
        """Создаёт пулю, летящую вниз."""
        bullet = Bullet(self.center_x,
                        self.center_y - 15,
                        -90,                # вниз
                        4,
                        friendly=False)
        self.bullet_list.append(bullet)

    def take_damage(self) -> bool:
        """Уменьшает здоровье, возвращает True, если враг уничтожен."""
        self.health -= 1
        if self.health <= 0:
            self.remove_from_sprite_lists()
            return True
        return False
