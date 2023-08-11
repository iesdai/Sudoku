import sys
import time
import pygame as pg
import settings
import menu
import board
from enum import Enum


# Определение перечисления для состояний игры
class GameState(Enum):
    START_MENU = 1
    GAME = 2


class Game:
    def __init__(self):
        """
        Инициализация класса Game.

        Создает экран для игры, устанавливает заголовок окна, задает начальное состояние игры,
        создает объекты меню и игрового поля, инициализирует переменные для времени игры и счетчика ошибок.
        """
        # Инициализируем библиотеку Pygame.
        pg.init()
        # Создаем экран для игры согласно настройкам.
        self.screen = pg.display.set_mode(settings.GAME_WINDOWS)
        # Устанавливаем заголовок окна игры.
        pg.display.set_caption('Sudoku Game')
        # Изначальное состояние игры - стартовое меню
        self.game_state = GameState.START_MENU
        # Создаем объекты для меню и игрового поля.
        self.menu = menu.Menu()
        self.board = board.Board(self.screen)
        # Переменные для отслеживания времени игры и количества ошибок.
        self.start_time = time.time()
        self.play_time = 0
        self.strikes = 0

    def run(self):
        """
        Основной цикл игры. Обрабатывает события, обновляет экран и ограничивает FPS.
        """
        while True:
            # Обработка событий (нажатия клавиш, клики мыши, закрытие окна).
            self.handle_events()

            if self.game_state == GameState.START_MENU:
                # Отображение стартового меню игры.
                self.menu.draw_start_menu()
            elif self.game_state == GameState.GAME:
                # Обновление времени игры и отрисовка игрового поля.
                self.play_time = round(time.time() - self.start_time)
                self.screen.fill(settings.BACKGROUND)
                self.board.draw_grid()
                self.board.draw_number()
                self.draw_game_info()

            # Обновление экрана и ограничение FPS.
            pg.display.update()
            pg.time.Clock().tick(settings.FPS)

    def handle_events(self):
        """
        Обработка всех событий, таких как нажатия клавиш, клики мыши и закрытие окна.
        """
        for event in pg.event.get():
            # Закрытие окна игры при нажатии кнопки "ESC" или нажатии на крестик.
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                # Обработка нажатия клавиш.
                self.handle_keyboard_input(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Обработка кликов мыши.
                self.handle_mouse_click(pg.mouse.get_pos())

    def handle_keyboard_input(self, key):
        """
        Обработка нажатий клавиш клавиатуры.
        """
        if key == pg.K_SPACE:
            # При нажатии клавиши "Пробел" переходим в состояние игры.
            self.game_state = GameState.GAME
        elif key == pg.K_UP:
            # При нажатии клавиши "Вверх" вызываем метод для решения судоку.
            self.board.sudoku_solver(0, 0)
        elif key in (pg.K_1, pg.K_KP1, pg.K_2, pg.K_KP2, pg.K_3, pg.K_KP3, pg.K_4, pg.K_KP4, pg.K_5, pg.K_KP5,
                     pg.K_6, pg.K_KP6, pg.K_7, pg.K_KP7, pg.K_8, pg.K_KP8, pg.K_9, pg.K_KP9):
            # Обработка нажатий цифровых клавиш (от 1 до 9).
            self.board.num = int(pg.key.name(key))
        elif key in (pg.K_BACKSPACE, pg.K_DELETE):
            # При нажатии клавиш "Backspace" или "Delete" очищаем текущую ячейку.
            self.board.clear()
            self.board.num = None
        elif key == pg.K_RETURN:
            # При нажатии клавиши "Enter" проверяем правильность заполнения ячейки.
            i, j = self.board.selected
            if self.board.check(i, j, self.board.cubes[i][j].temp):
                self.board.cubes[i][j].value = self.board.num
                self.board.cubes[i][j].temp = 0
            else:
                # Увеличиваем счетчик ошибок.
                self.strikes += 1
            if self.strikes == 3:
                # Если количество ошибок равно 3, завершаем игру.
                pg.quit()
                sys.exit()
            if self.board.is_finished():
                # Если игровое поле заполнено правильно, выводим сообщение о победе.
                print("You won!")
            # Сбрасываем значение и выбор текущей ячейки.
            self.board.num = None
            self.board.selected = None
        if self.board.selected and self.board.num is not None:
            # Если есть выбранная ячейка и назначена цифра, отображаем ее на поле.
            self.board.sketch()

    def handle_mouse_click(self, pos):
        """
        Обработка кликов мыши на игровом поле.
        """
        clicked = self.board.click(pos)
        if clicked:
            self.board.select(clicked[0], clicked[1])

    def draw_game_info(self):
        """
        Отображение информации о времени игры и счетчика ошибок.
        """
        text = settings.FONT_MAIN.render('Time: ' + self.format_time(), True, settings.WHITE)
        self.screen.blit(text, (500, 710))
        text = settings.FONT_MAIN.render('X' * self.strikes, True, settings.RED)
        self.screen.blit(text, (20, 710))

    def format_time(self):
        """
        Форматирование времени игры в минуты и секунды.
        """
        sec = self.play_time % 60
        minute = self.play_time // 60
        mat = ' ' + str(minute) + ':' + str(sec)
        return mat


if __name__ == '__main__':
    # Создание объекта игры и запуск игрового цикла.
    game = Game()
    game.run()
