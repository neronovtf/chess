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

  def findShifts(self, currentCol, currentRow, verify = False):
    places = []
    if verify is False:
      self.attackOnKing = None # Обнуляем координаты атаки на короля
    for orientation in ["UpRight", "DownRight", "DownLeft", "UpLeft"]:
      # Указываю координаты, для проверки
      col = 1 if orientation == "UpRight" or orientation == "UpLeft" else -1
      row = 1 if orientation == "UpRight" or orientation == "DownRight" else -1
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
              if not verify and (piece.pref == "K"): # Если это не проверка и есть реальная угроза королю
                self.attackOnKing = cell # Отмечаем данные координаты как приоритетный
              places.append(cell) # Если ячейка не пустая и фигура является противником
              break
            else: # Если фигура = друг
              if verify and (piece == self): # Проверка, и фигура на проверяемом месте, является нашей фигурой
                places.append(cell) # Если ячейка не пустая и фигура является противником
              else:
                break
          else:
            places.append(cell) # Если ячейка пустая
        else:
          break

    return places

  def canGo(self):
    self.places = self.findShifts(self.column, self.row)
    return bool(len(self.places))

  def canEat(self, position):
    """Функция проверяет, каким фигурам будет угрожать наша фигура на новом месте"""
    places = self.findShifts(position[0], position[1], verify = True)
    self.newPlaces = [] # Очищаем список доступных координат, до перемещения фригуры
    log = f"{self.name} на новой позиции {position}, будет угрожать: "
    for cell in places:
      piece = self.board[cell]
      self.newPlaces.append(cell) # Запоминаем все новые позиции, куда теоретически может пойти данная фигура
      if (piece is not None) and (piece != self) :
        # Указываем фигурам, что они находятся под ударом нашей фигуры
        piece.alarm = self
        log += f"{piece.name} на {cell}, "
    self.log.append(log)

  def calculateMoves(self):
    if self.attackOnKing:
      cell = self.attackOnKing # если есть возможность атаковать короля, атакуй !!
    else:
      cell = random.choice(self.places) # Рандом выбрал место, куда пойдёт

    self.canEat(cell)

    return cell
