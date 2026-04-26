"""Шахматная фигура - Ферзь(Королева). Стартовые позиции: d1, d8"""
import random
from piece import Piece

class Queen(Piece):
  """Класс ферзя"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "Q"
    self.name = "Ферзь"
    self.points = 9

  def findShifts(self, currentCol, currentRow):
    places = []

    orientation = ["Up", "UpRight", "Right", "DownRight", "Down", "DownLeft", "Left", "UpLeft"]
    for arrow in orientation:
      newCol = currentCol
      newRow = currentRow
      for i in range(1,9):

        # Задаём правила увеличения
        if arrow == "Up":
          newRow += 1
        elif arrow == "UpRight":
          newCol += 1
          newRow += 1
        elif arrow == "Right":
          newCol += 1
        elif arrow == "DownRight":
          newCol += 1
          newRow -= 1
        elif arrow == "Down":
          newRow -= 1
        elif arrow == "DownLeft":
          newCol -= 1
          newRow -= 1
        elif arrow == "Left":
          newCol -= 1
        elif arrow == "UpLeft":
          newCol -= 1
          newRow += 1

        #Проверки
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
