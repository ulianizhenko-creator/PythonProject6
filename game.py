# game.py
import arcade
import random
import time
from constants import *
from player import Player
from enemy import BasicEnemy
from game_objects import Bullet, Asteroid, ShieldPowerUp, RapidFirePowerUp, Star


class Game(arcade.View):
    """Основной класс, управляющий игровым процессом."""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(COLOR_BACKGROUND)

        # Спрайтлисты
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.asteroid_list = None
        self.powerup_list = None
        self.star_bg_list = None

        # Игровые переменные
        self.player_sprite = None
        self.score = 0
        self.game_time = 0
        self.difficulty_level = 1

        # Таймеры
        self.enemy_spawn_timer = 0
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0

    def setup(self):
        """Инициализация игры."""
        # Создаем спрайтлисты
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.star_bg_list = arcade.SpriteList()

        # Создаем игрока
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # Создаем фон из звезд
        for _ in range(100):
            star = Star()
            self.star_bg_list.append(star)

        # Сброс переменных
        self.score = 0
        self.game_time = 0
        self.difficulty_level = 1
        self.enemy_spawn_timer = 0
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0

        # Загружаем звуки
        self.explosion_sound = arcade.sound.load(EXPLOSION_SOUND)
        self.powerup_sound = arcade.sound.load(POWERUP_SOUND)

    def on_show_view(self):
        """Вызывается при переключении на этот вид."""
        self.setup()

    def on_draw(self):
        """Отрисовка."""
        self.clear()

        # Рисуем фон
        self.star_bg_list.draw()

        # Рисуем все спрайты
        self.asteroid_list.draw()
        self.powerup_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()

        # Рисуем UI
        score_text = f"Счет: {self.score}"
        lives_text = f"Жизни: {self.player_sprite.lives}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 30, COLOR_TEXT, 20)
        arcade.draw_text(lives_text, 10, SCREEN_HEIGHT - 60, COLOR_TEXT, 20)

        # Индикатор щита
        if self.player_sprite.shield_active:
            shield_text = f"Щит: {self.player_sprite.shield_timer / 60:.1f}s"
            arcade.draw_text(shield_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, arcade.color.CYAN, 18)

        if self.player_sprite.rapid_fire_active:
            rf_text = f"Скорострельность: {self.player_sprite.rapid_fire_timer / 60:.1f}s"
            arcade.draw_text(rf_text, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60, arcade.color.YELLOW, 18)

    def on_update(self, delta_time):
        """Обновление логики."""
        self.game_time += delta_time

        # Обновляем сложность игры
        if int(self.game_time) % GAME_DIFFICULTY_INCREASE_INTERVAL == 0 and int(self.game_time) > 0:
            self.difficulty_level += 1

        # Обновляем все спрайты
        self.star_bg_list.update()
        self.player_list.update()
        self.enemy_list.update()
        self.player_bullet_list.update()
        self.enemy_bullet_list.update()
        self.asteroid_list.update()
        self.powerup_list.update()

        # Спавн врагов
        self.enemy_spawn_timer -= delta_time
        if self.enemy_spawn_timer <= 0:
            enemy = BasicEnemy()
            enemy.change_y -= (self.difficulty_level * 0.2)  # Увеличиваем скорость со временем
            self.enemy_list.append(enemy)
            self.enemy_spawn_timer = ENEMY_SPAWN_RATE - (self.difficulty_level * 0.05)  # Увеличиваем частоту
            if self.enemy_spawn_timer < 0.2: self.enemy_spawn_timer = 0.2

        # Спавн астероидов
        self.asteroid_spawn_timer -= delta_time
        if self.asteroid_spawn_timer <= 0:
            for _ in range(random.randint(ASTEROID_COUNT_MIN, ASTEROID_COUNT_MAX)):
                asteroid = Asteroid()
                self.asteroid_list.append(asteroid)
            self.asteroid_spawn_timer = ASTEROID_SPAWN_RATE

        # Спавн усилений
        self.powerup_spawn_timer -= delta_time
        if self.powerup_spawn_timer <= 0:
            if random.random() < 0.5:
                self.powerup_list.append(ShieldPowerUp())
            else:
                self.powerup_list.append(RapidFirePowerUp())
            self.powerup_spawn_timer = POWERUP_SPAWN_RATE

        # --- Коллизии ---

        # 1. Пули игрока попадают во врагов
        for bullet in self.player_bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                for enemy in hit_list:
                    if enemy.take_damage():
                        self.score += 10
                        arcade.play_sound(self.explosion_sound)
                bullet.remove_from_sprite_lists()

        # 2. Пули игрока попадают в астероиды
        for bullet in self.player_bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            if hit_list:
                for asteroid in hit_list:
                    asteroid.remove_from_sprite_lists()
                    self.score += 5
                bullet.remove_from_sprite_lists()

        # 3. Игрок сталкивается с врагами
        enemy_hits = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if enemy_hits:
            if self.player_sprite.take_damage():
                arcade.play_sound(self.explosion_sound)
            for enemy in enemy_hits:
                enemy.remove_from_sprite_lists()

        # 4. Игрок сталкивается с пулями врагов
        bullet_hits = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
        if bullet_hits:
            if self.player_sprite.take_damage():
                arcade.play_sound(self.explosion_sound)
            for bullet in bullet_hits:
                bullet.remove_from_sprite_lists()

        # 5. Игрок сталкивается с астероидами
        asteroid_hits = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
        if asteroid_hits:
            if self.player_sprite.take_damage():
                arcade.play_sound(self.explosion_sound)
            for asteroid in asteroid_hits:
                asteroid.remove_from_sprite_lists()

        # 6. Игрок собирает усиления
        powerup_hits = arcade.check_for_collision_with_list(self.player_sprite, self.powerup_list)
        if powerup_hits:
            for powerup in powerup_hits:
                if powerup.power_type == "shield":
                    self.player_sprite.activate_shield()
                elif powerup.power_type == "rapid_fire":
                    self.player_sprite.activate_rapid_fire()
                arcade.play_sound(self.powerup_sound)
                powerup.remove_from_sprite_lists()

        # Враги стреляют в игрока
        for enemy in self.enemy_list:
            enemy.fire(self.player_sprite)  # В методе fire есть проверка на вероятность

        # Обновляем список пуль врагов
        self.enemy_bullet_list.extend(
            [b for b_list in [enemy.bullet_list for enemy in self.enemy_list] for b in b_list])
        for enemy in self.enemy_list:
            enemy.bullet_list.clear()

        # Проверка на окончание игры
        if self.player_sprite.lives <= 0:
            game_over_view = GameOverView(self, self.score)
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш."""
        if key == arcade.key.SPACE:
            self.player_sprite.fire(self.player_bullet_list)
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_SPEED
        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш."""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0

