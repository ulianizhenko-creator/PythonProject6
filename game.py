# game.py
import arcade
import random
import time
from constants import *
from player import Player
from enemy import BasicEnemy
from game_objects import Bullet, Asteroid, ShieldPowerUp, RapidFirePowerUp, Star

class Game(arcade.View):
    """Главный игровой процесс."""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(COLOR_BACKGROUND)

        # -----------------------------------------------------------------
        # Спрайт‑листы (будут созданы в setup())
        # -----------------------------------------------------------------
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.asteroid_list = None
        self.powerup_list = None
        self.star_bg_list = None

        self.player_sprite = None

        self.score = 0
        self.game_time = 0.0
        self.difficulty_level = 1

        self.enemy_spawn_timer = 0.0
        self.asteroid_spawn_timer = 0.0
        self.powerup_spawn_timer = 0.0

        # Звуки
        self.explosion_sound = None
        self.powerup_sound = None

    # -----------------------------------------------------------------
    # on_show_view вызывается каждый раз, когда этот View становится активным
    # -----------------------------------------------------------------
    def on_show_view(self):
        self.setup()

    # -----------------------------------------------------------------
    # Полная инициализация/перезапуск уровня
    # -----------------------------------------------------------------
    def setup(self):
        # ------------------ Списки ------------------
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.star_bg_list = arcade.SpriteList()

        # ------------------ Игрок ------------------
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # ------------------ Фон -------------------
        for _ in range(100):
            self.star_bg_list.append(Star())

        # ------------------ Статистика -------------
        self.score = 0
        self.game_time = 0.0
        self.difficulty_level = 1

        self.enemy_spawn_timer = 0.0
        self.asteroid_spawn_timer = 0.0
        self.powerup_spawn_timer = 0.0

        # ------------------ Звуки -------------------
        # Обратите внимание: теперь используется arcade.load_sound
        self.explosion_sound = arcade.load_sound(EXPLOSION_SOUND)
        self.powerup_sound = arcade.load_sound(POWERUP_SOUND)

    # -----------------------------------------------------------------
    # Отрисовка
    # -----------------------------------------------------------------
    def on_draw(self):
        self.clear()
        self.star_bg_list.draw()
        self.asteroid_list.draw()
        self.powerup_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()

        # ------------------ UI -----------------
        arcade.draw_text(f"Счёт: {self.score}",
                         10, SCREEN_HEIGHT - 30,
                         COLOR_TEXT, 20)

        arcade.draw_text(f"Жизни: {self.player_sprite.lives}",
                         10, SCREEN_HEIGHT - 60,
                         COLOR_TEXT, 20)

        if self.player_sprite.shield_active:
            txt = f"Щит: {self.player_sprite.shield_timer/60:.1f}s"
            arcade.draw_text(txt,
                             SCREEN_WIDTH - 150,
                             SCREEN_HEIGHT - 30,
                             arcade.color.CYAN, 18)

        if self.player_sprite.rapid_fire_active:
            txt = f"Скорострельность: {self.player_sprite.rapid_fire_timer/60:.1f}s"
            arcade.draw_text(txt,
                             SCREEN_WIDTH - 200,
                             SCREEN_HEIGHT - 60,
                             arcade.color.YELLOW, 18)

    # -----------------------------------------------------------------
    # Основная логика (вызывается каждый кадр)
    # -----------------------------------------------------------------
    def on_update(self, delta_time: float):
        # ------------------ Время и сложность ------------------
        self.game_time += delta_time
        if (int(self.game_time) %
            GAME_DIFFICULTY_INCREASE_INTERVAL) == 0 and int(self.game_time) > 0:
            self.difficulty_level += 1

        # ------------------ Обновляем спрайты ------------------
        self.star_bg_list.update(delta_time)
        self.player_list.update(delta_time)
        self.enemy_list.update(delta_time)
        self.player_bullet_list.update(delta_time)
        self.enemy_bullet_list.update(delta_time)
        self.asteroid_list.update(delta_time)
        self.powerup_list.update(delta_time)

        # ------------------ Спавн врагов ------------------
        self.enemy_spawn_timer -= delta_time
        if self.enemy_spawn_timer <= 0:
            enemy = BasicEnemy()
            enemy.change_y -= (self.difficulty_level * 0.2)
            self.enemy_list.append(enemy)

            # Уменьшаем интервал, но не допускаем отрицательного значения
            self.enemy_spawn_timer = max(0.2,
                                        ENEMY_SPAWN_RATE -
                                        (self.difficulty_level * 0.05))

        # ------------------ Спавн астероидов ------------------
        self.asteroid_spawn_timer -= delta_time
        if self.asteroid_spawn_timer <= 0:
            for _ in range(random.randint(ASTEROID_COUNT_MIN,
                                          ASTEROID_COUNT_MAX)):
                self.asteroid_list.append(Asteroid())
            self.asteroid_spawn_timer = ASTEROID_SPAWN_RATE

        # ------------------ Спавн power‑up'ов ------------------
        self.powerup_spawn_timer -= delta_time
        if self.powerup_spawn_timer <= 0:
            if random.random() < 0.5:
                self.powerup_list.append(ShieldPowerUp())
            else:
                self.powerup_list.append(RapidFirePowerUp())
            self.powerup_spawn_timer = POWERUP_SPAWN_RATE

        # ------------------ Коллизии ------------------
        # Пули игрока → враги
        for bullet in self.player_bullet_list:
            hit_enemies = arcade.check_for_collision_with_list(bullet,
                                                              self.enemy_list)
            if hit_enemies:
                for enemy in hit_enemies:
                    if enemy.take_damage():
                        self.score += 10
                        arcade.play_sound(self.explosion_sound)
                bullet.remove_from_sprite_lists()

        # Пули игрока → астероиды
        for bullet in self.player_bullet_list:
            hit_asts = arcade.check_for_collision_with_list(bullet,
                                                            self.asteroid_list)
            if hit_asts:
                for ast in hit_asts:
                    ast.remove_from_sprite_lists()
                    self.score += 5
                bullet.remove_from_sprite_lists()

        # *** НЕУЯЗВИМОСТЬ В НАЧАЛЕ ***
        # Если у игрока есть активный таймер «неуязвим», игнорируем
        # любые столкновения, которые могли бы отнять жизнь.
        invuln = self.player_sprite.invulnerable_timer > 0

        if not invuln:
            # Игрок → враги
            if arcade.check_for_collision_with_list(self.player_sprite,
                                                   self.enemy_list):
                if self.player_sprite.take_damage():
                    arcade.play_sound(self.explosion_sound)

            # Игрок → вражеские пули
            if arcade.check_for_collision_with_list(self.player_sprite,
                                                   self.enemy_bullet_list):
                if self.player_sprite.take_damage():
                    arcade.play_sound(self.explosion_sound)

            # Игрок → астероиды
            if arcade.check_for_collision_with_list(self.player_sprite,
                                                   self.asteroid_list):
                if self.player_sprite.take_damage():
                    arcade.play_sound(self.explosion_sound)

        # Игрок → power‑up'ы (неуязвимость здесь не мешает)
        for pu in arcade.check_for_collision_with_list(self.player_sprite,
                                                       self.powerup_list):
            if pu.power_type == "shield":
                self.player_sprite.activate_shield()
            elif pu.power_type == "rapid_fire":
                self.player_sprite.activate_rapid_fire()
            arcade.play_sound(self.powerup_sound)
            pu.remove_from_sprite_lists()

        # Враги стреляют (объединяем их пули)
        for enemy in self.enemy_list:
            self.enemy_bullet_list.extend(enemy.bullet_list)
            enemy.bullet_list = arcade.SpriteList()   # очистка

        # ------------------ Окончание игры ------------------
        if self.player_sprite.lives <= 0:
            # Импорт внутри функции, чтобы избежать циклической зависимости
            from views import GameOverView
            game_over_view = GameOverView(self, self.score)
            self.window.show_view(game_over_view)

    # -----------------------------------------------------------------
    # Управление клавиатурой
    # -----------------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player_sprite.fire(self.player_bullet_list)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player_sprite.change_y = 0
