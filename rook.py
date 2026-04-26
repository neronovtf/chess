"""Шахматная фигура - Ладья. Стартовые позиции: a1, h1, a8, h8"""
import random
from piece import Piece

class Rook(Piece):
  """Класс ладьи"""
  def __init__(self, data):
    super().__init__(data)
    self.pref = "R"
    self.name = "Ладья"
    self.points = 5

  def findShifts(self, currentCol, currentRow, verify = False):
    places = []
    if verify is False:
      self.attackOnKing = None # Обнуляем координаты атаки на короля

    for orientation in range(1,5): # 1 = Up, 2 = Rigth, 3 = Down, 4 = Left
      if orientation == 1 or orientation == 3: # Проверяем ячейки вверх = 1 (Up) и ячейки вниз = 3 (down)
        step = 1 if orientation == 1 else -1
        col = currentCol
        shift = currentRow
        def getCell():
          return (col, shift)
      elif orientation == 2 or orientation == 4: # Проверяем ячейки вправо = 2 (rigth) и ячейки влево = 4 (left)
        step = 1 if orientation == 2 else -1
        shift = currentCol
        row = currentRow
        def getCell():
          return (shift, row)

      for i in range(1, 9):
        shift += step
        if 0 < shift < 9: # Не выходи за диапозон
          cell = getCell()
          piece = self.board[cell]

          if piece is not None:
            if piece.isWhite is not self.isWhite:
              if verify is False and piece.pref == "K": # Если это не проверка и есть реальная угроза королю
                self.attackOnKing = cell # Отмечаем данные координаты как приоритетный
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
    """Функция проверяет, каким фигурам будет угрожать наша фигура на новом месте"""
    places = self.findShifts(cell[0], cell[1], verify = True)
    for cell in places:
      piece = self.board[cell]
      if piece is not None:
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self

  def calculateMoves(self):
    if self.attackOnKing:
      cell = self.attackOnKing # если есть возможность атаковать короля, атакуй !!
    else:
      cell = random.choice(self.places) # Рандом выбрал место, куда пойдёт

    self.canEat(cell)
    return cell
