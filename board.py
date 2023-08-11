
import random
import numpy as np
import pandas as pd
import pygame as pg

import settings
import cube


class Board:
    def __init__(self, screen):
        """
        Конструктор класса Board. Инициализирует игровое поле.

        :param screen: экран Pygame для отображения игры.
        """
        self.screen = screen

        # Создаем прямоугольники для отрисовки сетки и ячеек игрового поля.
        self.grid_sup = [pg.Rect(x * settings.TILE_SUP, y * settings.TILE_SUP, settings.TILE_SUP, settings.TILE_SUP)
                         for x in range(settings.ROW // 3) for y in range(settings.COL // 3)]
        self.grid = [pg.Rect(x * settings.TILE, y * settings.TILE, settings.TILE, settings.TILE)
                     for x in range(settings.ROW) for y in range(settings.COL)]

        # Загружаем судоку из CSV-файла и выбираем случайную схему и ее решение.
        self.df = pd.read_csv('sudoku.csv')
        self.index = random.randint(0, 1000000)
        self.sud = np.array(list(map(int, list(self.df['quizzes'][self.index])))).reshape(9, 9)
        self.solution = np.array(list(map(int, list(self.df['solutions'][self.index])))).reshape(9, 9)

        # Создаем объекты кубиков (ячеек) на игровом поле и заполняем их значениями судоку.
        self.cubes = [[cube.Cube(self.sud[i][j], i, j, self.screen)
                       for j in range(settings.ROW)] for i in range(settings.COL)]

        # Переменные для отслеживания текущего выбранного и введенного числа.
        self.clicked = None
        self.selected = None
        self.num = None

    def sketch(self):
        """
        Устанавливает значение временной переменной temp для текущей выбранной ячейки.
        """
        row, col = self.selected
        self.cubes[row][col].temp = self.num

    def select(self, row, col):
        """
        Выбирает ячейку в позиции (row, col) и снимает выделение со всех остальных ячеек.

        :param row: Индекс строки ячейки.
        :param col: Индекс столбца ячейки.
        """
        for i in range(settings.ROW):
            for j in range(settings.COL):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """
        Очищает значение временной переменной temp для текущей выбранной ячейки.
        """
        row, col = self.selected
        self.cubes[row][col].temp = 0

    @staticmethod
    def click(pos):
        """
        Определяет, на какую ячейку игрового поля было произведено нажатие мыши.

        :param pos: Координаты клика мыши (x, y).
        :return: Позиция выбранной ячейки (row, col) или None, если клик был за пределами игрового поля.
        """
        if pos[0] < settings.GAME_WINDOWS[0] and pos[1] < settings.GAME_WINDOWS[1] - 100:
            col_index = pos[0] // settings.TILE
            row_index = pos[1] // settings.TILE
            return int(row_index), int(col_index)
        else:
            return None

    def is_finished(self):
        """
        Проверяет, закончена ли игра, т.е. все ли ячейки заполнены.

        :return: True, если все ячейки заполнены, и False в противном случае.
        """
        for i in range(settings.ROW):
            for j in range(settings.COL):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def draw_grid(self):
        """
        Отрисовывает сетку игрового поля.
        """
        [pg.draw.rect(self.screen, settings.GRID, i, 1) for i in self.grid]
        [pg.draw.rect(self.screen, settings.WHITE, i, 1) for i in self.grid_sup]

    def draw_number(self):
        """
        Отрисовывает значения ячеек на игровом поле.
        """
        for i in range(settings.ROW):
            for j in range(settings.COL):
                self.cubes[i][j].draw()

    def check(self, row, col, num):
        """
        Проверяет, является ли значение num правильным для ячейки в позиции (row, col).

        :param row: Индекс строки ячейки.
        :param col: Индекс столбца ячейки.
        :param num: Значение для проверки.
        :return: True, если значение num правильное, и False в противном случае.
        """
        if num == self.solution[row][col]:
            return True
        else:
            return False

    def solve(self, row, col, num):
        """
        Проверяет, можно ли установить значение num для ячейки в позиции (row, col)
        без нарушения правил игры.

        :param row: Индекс строки ячейки.
        :param col: Индекс столбца ячейки.
        :param num: Значение для проверки.
        :return: True, если значение num допустимо, и False в противном случае.
        """
        for x in range(9):
            if self.cubes[row][x].value == num or self.cubes[x][col].value == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.cubes[i + start_row][j + start_col].value == num:
                    return False
        return True

    def sudoku_solver(self, row, col):
        """
        Рекурсивный метод для решения судоку с использованием метода "backtracking".

        :param row: Индекс строки ячейки, с которой начинается решение.
        :param col: Индекс столбца ячейки, с которой начинается решение.
        :return: True, если судоку решено, и False в противном случае.
        """
        if row == settings.ROW - 1 and col == settings.ROW:
            return True
        if col == settings.ROW:
            row += 1
            col = 0
        if self.cubes[row][col].value > 0:
            return self.sudoku_solver(row, col + 1)
        for num in range(1, settings.ROW + 1, 1):

            if self.solve(row, col, num):

                self.cubes[row][col].value = num
                self.cubes[row][col].draw_change(True)
                pg.display.update()
                pg.time.delay(100)
                if self.sudoku_solver(row, col + 1):
                    return True
            self.cubes[row][col].value = 0
            self.cubes[row][col].draw_change(False)
            pg.display.update()
            pg.time.delay(100)
        return False
