"""Шахматная фигура - Слон. Стартовые позиции: c1, f1, c8, f8"""
# import random
from piece import Piece

class Bishop(Piece):
  """Класс слона"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "B"
    self.name = "Слон"
    self.points = 3

  def findShifts(self, currentCol = None, currentRow = None, forKing = False):
    """
    Находит возможные ходы фигуры.

    Args:
        currentCol (int, optional): Колонка. Если None, берётся self.column.
        currentRow (int, optional): Строка. Если None, берётся self.row.
        forKing (bool, optional): Флаг. Означающий, что опрос делает король, и ему нужно больше данных
    """
    currentCol = self.column if currentCol is None else currentCol
    currentRow = self.row if currentRow is None else currentRow
    places = []

    for orientation in ["UpRight", "DownRight", "DownLeft", "UpLeft"]:
      # Указываю координаты, для проверки
      col = 1 if orientation == "UpRight" or orientation == "UpLeft" else -1
      row = 1 if orientation == "UpRight" or orientation == "DownRight" else -1
      # Сбрасываем позиции на исходное положение
      newCol = currentCol
      newRow = currentRow
      countKing = 2

      for i in range(1, 9):
        newCol += col
        newRow += row

        if not ((0 < newCol < 9) and (0 < newRow < 9)): # Не выходи за пределы игрового поля
          break

        cell = (newCol, newRow)
        piece = self.board[cell]

        if piece is None:
          # Ячейка пустая
          places.append(cell)
        else:
          # Есть фигура
          if forKing: # запрос от Короля
            # if piece.isWhite is self.isWhite:
            places.append(cell)
            countKing -= 1
            # else:
              # Прекратить добавлять, если встретился не с противником
            if countKing == 0:
              break
          else:
            if piece.isWhite is not self.isWhite:
              places.append(cell)
            # Прекратить добавлять, сразу как встретился с фигурой
            break

    return places
