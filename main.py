# main.py
import arcade
from constants import *
from views import MainMenuView

def main():
    """Основная функция для запуска игры."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

