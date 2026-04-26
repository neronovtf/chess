"""Шахматная фигура - Пешка"""
import random
from piece import Piece

class Pawn(Piece):
  """Класс пешки"""
  def __init__(self, data):
    super().__init__(data)
    self.firstStep = True
    self.name = "Пешка"
    self.pref = "" # Раньше пешку обозначали буквой 'P', но сейчас она без буквы
    self.points = 1

  def getStep(self):
    return 1 if self.isWhite else -1

  def canGoForAdvance(self):
    newColumn = self.column
    places = []
    steps = [1]
    if self.firstStep:
      steps.append(2)
    for i in steps:
      newRow = self.row + i * self.getStep()
      if (0 < newColumn < 9) and (0 < newRow < 9): # Не выходи за диапозон
        if self.board[(newColumn, newRow)] is None:
          places.append((newColumn, newRow))
        else:
          break # Если первая позиция занята, дальше смотреть не надо
    return places

  def canGoForEat(self, currentRow):
    newRow = currentRow + self.getStep()
    places = []
    for i in [1, -1]:
      newColumn = self.column + i
      if (0 < newColumn < 9) and (0 < newRow < 9): # Не выходи за диапозон
        place = self.board[(newColumn, newRow)]
        if place is not None: # Место должно быть не пустым
          if place.isWhite is not self.isWhite: # Цвет фигуры на позиции для еды, должна отличаться от цвета текущей фигуры
            places.append((newColumn, newRow))
    return places

  def canGo(self):
    self.places = self.canGoForAdvance() + self.canGoForEat(self.row)
    return bool(len(self.places))

  def canEatKing(self, cell):
    places = self.canGoForEat(cell[1]) # 0 = column, 1 = row
    for cell in places:
      piece = self.board[cell]
      if piece is not None:
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self

  def calculateMoves(self):
    self.firstStep = False
    cell = random.choice(self.places)
    self.canEatKing(cell)
    return cell