"""Шахматная фигура - Слон. Стартовые позиции: c1, f1, c8, f8"""
import random
from piece import Piece

class Bishop(Piece):
  """Класс слона"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "B"
    self.name = "Слон"
    self.points = 3

  def findShifts(self, currentCol, currentRow):
    # newCol = currentCol
    # newRow = currentRow
    places = []
    for orientation in range(1,5): # 1 = Up + Right(UR), 2 = Down + Right(DR), 3 = Down + Left(DL), 4 = Up + Left(UL)

      col = 1 if orientation == 1 or orientation == 4 else -1 # DL + UL
      row = 1 if orientation == 1 or orientation == 2 else -1 # UR + DR
      # Сбрасываем позиции на исходное положение
      newCol = currentCol
      newRow = currentRow

      for i in range(1, 9):
        newCol += col
        newRow += row

        if (0 < newCol < 9) and (0 < newRow < 9): # Не выходи за диапозон
          cell = (newCol, newRow)
          piece = self.board[cell]

          if piece is not None:
            if piece.isWhite is not self.isWhite:
              places.append(cell) # Если ячейка не пустая и фигура является противником
            break
          else:
            places.append(cell) # Если ячейка пустая
        else:
          break

    return places

  def canGo(self):
    self.places = self.findShifts(self.column, self.row)
    return bool(len(self.places))

  def canEat(self, cell):
    """Функция определяет, каким фигурам будет угрожать наша фигура"""
    places = self.findShifts(cell[0], cell[1])
    for cell in places:
      piece = self.board[cell]
      if piece is not None:
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self

  def calculateMoves(self):
    cell = random.choice(self.places) # Рандом выбрал место, куда пойдёт
    self.canEat(cell)

    return cell
