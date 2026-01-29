# views.py
import arcade
import os
from constants import *
from game import Game


class MainMenuView(arcade.View):
    """Главное меню."""

    def on_show_view(self):
        """Вызывается при переходе в это меню."""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """Отрисовка меню."""
        self.clear()
        arcade.draw_text("Star Defender", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите SPACE чтобы начать", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Нажмите ESC чтобы выйти", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """Обработка нажатий в меню."""
        if key == arcade.key.SPACE:
            game_view = Game()
            game_view.window = self.window
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class GameOverView(arcade.View):
    """Экран окончания игры."""

    def __init__(self, game_view, final_score):
        super().__init__()
        self.game_view = game_view
        self.final_score = final_score
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Загружает рекорд из файла."""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Сохраняет новый рекорд."""
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()

        arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        score_text = f"Ваш счет: {self.final_score}"
        arcade.draw_text(score_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=24, anchor_x="center")

        if self.final_score > self.high_score:
            self.high_score = self.final_score
            self.save_high_score()

        high_score_text = f"Рекорд: {self.high_score}"
        arcade.draw_text(high_score_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                         arcade.color.GOLD, font_size=20, anchor_x="center")

        arcade.draw_text("Нажмите C чтобы сыграть снова", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Нажмите ESC для выхода в меню", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.C:  # C как "Continue"
            self.game_view.setup()  # Перезапускаем игру
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
