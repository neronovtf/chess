"""Шахматная фигура - Конь. Стартовые позиции: b1, g1, b8, g8"""
# import random
from piece import Piece

class Knight(Piece):
  """Класс коня"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "N" # Потому что K уже занято королём
    self.name = "Конь"
    self.points = 3

  def findShifts(self, currentCol = None, currentRow = None, forKing = False):
    """
    Находит возможные ходы фигуры.

    Args:
        currentCol (int, optional): Колонка. Если None, берётся self.column.
        currentRow (int, optional): Строка. Если None, берётся self.row.
    """
    currentCol = self.column if currentCol is None else currentCol
    currentRow = self.row if currentRow is None else currentRow
    places = []

    for orientation in ["Up", "Right", "Down", "Left"]: # Проверяем все направления
      for turn in ["plus", "minus"]: # Каждое направление нужно отработать по два раза

        if (orientation == "Up") or (orientation == "Down"):
          row = 2 if orientation == "Up" else -2
          col = 1 if turn == "plus" else -1
        else: # "Right", "Left"
          col = 2 if orientation == "Right" else -2
          row = 1 if turn == "plus" else -1

        # Присоединяем новые значения к текущей позиции фигуры
        newCol = currentCol + col
        newRow = currentRow + row
        if not ((0 < newCol < 9) and (0 < newRow < 9)): # Не выходи за пределы игрового поля
          continue

        cell = (newCol, newRow)
        piece = self.board[cell]

        if piece is None:
          # Ячейка пустая
          places.append(cell)
        else:
          # Есть фигура
          if forKing:
            places.append(cell)
          else:
            if piece.isWhite is not self.isWhite:
              places.append(cell)

    return places
