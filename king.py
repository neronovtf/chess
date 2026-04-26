"""Шахматная фигура - Король. Стартовые позиции: d1, d8"""
import random
from piece import Piece

class King(Piece):
  """Класс короля"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "K"
    self.name = "Король"
    self.points = 0 # бесценен

  def findShifts(self):
    places = []
    col = self.column
    row = self.row
    haveKing = False

    # Нужно проверить два круга вокруг короля т.к. короли не могут находиться на соседних клетках
    for i in range(col-2, col+3):
      for j in range(row-2, row+3):
        if i == col and j == row: # Игнорируем позиции, где находится наша фигура
          continue
        else:
          if (0 < i < 9) and (0 < j < 9): # Не выходи за диапозон
            cell = (i, j)
            piece = self.board[cell]
            if (piece is not None) and (piece.pref == self.pref): # Если совпадают, значит это король
              haveKing = True
              places = [] # Обнуляем список доступных шагов т.к. двигаться нельзя
              break # Прерываем циклы, нет смысла проверять всё остальное
            else:
              if(abs(i - col) <= 1 and abs(j - row) <= 1): # Ячейки, вокруг нашей фигуры

                if piece is not None:
                  if piece.isWhite is not self.isWhite:
                    places.append(cell) # Если ячейка не пустая и фигура является противником
                else:
                  places.append(cell) # Если ячейка пустая
      # Конец первого цикла
      if haveKing:
        break # Прерываем первый цикл т.к. в ближнем окружении был найден второй король

    return places

  def canGo(self):
    self.places = self.findShifts()
    return bool(len(self.places))

  def calculateMoves(self):
    return random.choice(self.places)
