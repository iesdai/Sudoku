import settings
import pygame as pg


class Cube:

    def __init__(self, value, row, col, screen):
        """
        Инициализация класса Cube.

        :param value: Значение ячейки.
        :param row: Индекс строки ячейки.
        :param col: Индекс столбца ячейки.
        :param screen: Экран для отрисовки ячейки.
        """
        self.temp = 0
        self.value = value
        self.row = row
        self.col = col
        self.selected = False
        self.screen = screen

    def draw(self):
        """
        Отрисовка ячейки на экране.
        """
        x = self.col * settings.TILE
        y = self.row * settings.TILE

        if self.temp != 0 and self.value == 0:
            # Если есть временное значение и значение ячейки равно 0, отображаем его серым цветом
            text = settings.FONT_MAIN.render(str(self.temp), True, settings.GRAY)
            self.screen.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            # Если значение ячейки не равно 0, отображаем его белым цветом
            text = settings.FONT_MAIN.render(str(self.value), True, settings.WHITE)
            self.screen.blit(text, (x + (settings.TILE / 2 - text.get_width() / 2),
                                    y + (settings.TILE / 2 - text.get_height() / 2)))

        if self.selected and self.value == 0:
            # Если ячейка выбрана и ее значение равно 0, рисуем красную обводку вокруг ячейки
            pg.draw.rect(self.screen, settings.RED, (x, y, settings.TILE, settings.TILE), 3)

    def draw_change(self, selected=True):
        """
        Отрисовка изменения ячейки.

        :param selected:  Флаг, указывающий на выбор ячейки (True - выбрана, False - не выбрана).
                                  По умолчанию равен True.
        """
        x = self.col * settings.TILE
        y = self.row * settings.TILE

        # Отрисовываем фон ячейки заданным фоновым цветом
        pg.draw.rect(self.screen, settings.BACKGROUND, (x, y, settings.TILE, settings.TILE), 0)

        # Отрисовываем значение ячейки белым цветом
        text = settings.FONT_MAIN.render(str(self.value), True, settings.WHITE)
        self.screen.blit(text, (x + (settings.TILE / 2 - text.get_width() / 2),
                                y + (settings.TILE / 2 - text.get_height() / 2)))
        if selected:
            # Если ячейка выбрана, рисуем зеленую обводку вокруг ячейки
            pg.draw.rect(self.screen, (0, 255, 0), (x, y, settings.TILE, settings.TILE), 3)
        else:
            # Если ячейка не выбрана, рисуем красную обводку вокруг ячейки
            pg.draw.rect(self.screen, (255, 0, 0), (x, y, settings.TILE, settings.TILE), 3)
