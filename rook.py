"""Шахматная фигура - Ладья. Стартовые позиции: a1, h1, a8, h8"""
# import random
from piece import Piece

class Rook(Piece):
  """Класс ладьи"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "R"
    self.name = "Ладья"
    self.points = 5

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

    for orientation in ["Up", "Rigth", "Down", "Left"]:
      countKing = 2

      if orientation == "Up" or orientation == "Down":
        step = 1 if orientation == "Up" else -1
        col = currentCol
        shift = currentRow
        def getCell():
          return (col, shift)
      elif orientation == "Rigth" or orientation == "Left":
        step = 1 if orientation == "Rigth" else -1
        shift = currentCol
        row = currentRow
        def getCell():
          return (shift, row)

      for i in range(1, 9):
        shift += step

        if not (0 < shift < 9): # Не выходи за пределы игрового поля
          break

        cell = getCell()
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
