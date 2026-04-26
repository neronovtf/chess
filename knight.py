"""Шахматная фигура - Конь. Стартовые позиции: b1, g1, b8, g8"""
import random
from piece import Piece

class Knight(Piece):
  """Класс коня"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "N" # Потому что K уже занято королём
    self.name = "Конь"
    self.points = 3

  def findShifts(self, currentCol, currentrow):
    places = []

    for orientation in range(1,5): # 1 = Up, 2 = Right, 3 = Down, 4 = Left

      for turn in range(1,3): # Каждое направление нужно отработать по два раза

        # Up + Down
        if orientation == 1 or orientation == 3:
          col = 1 if turn == 1 else -1
          row = 2 if orientation == 3 else -2

        # Right + Left
        elif orientation == 2 or orientation == 4:
          col = 2 if orientation == 4 else -2
          row = 1 if turn == 1 else -1

        # Присоединяем новые значения к текущей позиции фигуры
        newCol = currentCol + col
        newRow = currentrow + row

        if (0 < newCol < 9) and (0 < newRow < 9): # Не выходи за диапозон
          cell = (newCol, newRow)
          piece = self.board[cell]

          if piece is not None:
            if piece.isWhite is not self.isWhite:
              places.append(cell) # Если ячейка не пустая и фигура является противником
            break
          else:
            places.append(cell) # Если ячейка пустая

    return places

  def canGo(self):
    self.places = self.findShifts(self.column, self.row)
    return bool(len(self.places))

  def canEatKing(self, cell):
    places = self.findShifts(cell[0], cell[1])
    for cell in places:
      piece = self.board[cell]
      if piece is not None:
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self

  def calculateMoves(self):
    cell = random.choice(self.places)
    self.canEatKing(cell)

    return cell
