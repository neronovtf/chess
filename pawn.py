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
        cell = (newColumn, newRow)
        if self.board[cell] is None:
          places.append(cell)
        else:
          break # Если первая позиция занята, дальше смотреть не надо
    return places

  def canGoForEat(self, currentRow, verify = False):
    newRow = currentRow + self.getStep()
    places = []
    if verify is False:
      self.attackOnKing = None # Обнуляем координаты атаки на короля
    for i in [1, -1]:
      newColumn = self.column + i
      if (0 < newColumn < 9) and (0 < newRow < 9): # Не выходи за диапозон
        cell = (newColumn, newRow)
        piece = self.board[cell]
        if piece is not None: # Место должно быть не пустым
          if piece.isWhite is not self.isWhite: # Цвет фигуры на позиции для еды, должна отличаться от цвета текущей фигуры
            if verify is False and piece.pref == "K": # Если это не проверка и есть реальная угроза королю
              self.attackOnKing = cell # Отмечаем данные координаты как приоритетный
            places.append(cell)
    return places

  def canGo(self):
    self.places = self.canGoForAdvance() + self.canGoForEat(self.row)
    return bool(len(self.places))

  def canEat(self, cell):
    """Функция проверяет, каким фигурам будет угрожать наша фигура на новом месте"""
    places = self.canGoForEat(cell[1]) # 0 = column, 1 = row
    for cell in places:
      piece = self.board[cell]
      if piece is not None:
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self

  def calculateMoves(self):
    self.firstStep = False # После того, как сделан шаг, пешка теряет возможность перепрыгивать через клетку

    if self.attackOnKing:
      cell = self.attackOnKing # если есть возможность атаковать короля, атакуй !!
    else:
      cell = random.choice(self.places) # Рандом выбрал место, куда пойдёт

    self.canEat(cell)
    return cell