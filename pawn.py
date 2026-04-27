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

  def findShifts(self, currentCol, currentrow, verify = False):
    places = []
    if verify is False:
      self.attackOnKing = None # Обнуляем координаты атаки на короля

    for orientation in ["UpRight", "UpLeft", "Up", "UpTwo"]:

      if orientation == "UpRight":
        newCol = currentCol + 1
        newRow = currentrow + 1
      elif orientation == "UpLeft":
        newCol = currentCol - 1
        newRow = currentrow + 1
      elif orientation == "Up":
        newCol = currentCol
        newRow = currentrow + 1
      elif orientation == "UpTwo":
        if not self.firstStep: continue # если это не первый шаг фигуры, то пропускаем это действие
        newCol = currentCol
        newRow = currentrow + 2

      if (0 < newCol < 9) and (0 < newRow < 9): # Не выходи за диапозон
        cell = (newCol, newRow)
        piece = self.board[cell]
        if piece is not None: # Не пустая
          if piece.isWhite is not self.isWhite: # Фигура соперника
            if not verify and (piece.pref == "K"): # Если это не проверка и есть реальная угроза королю
              self.attackOnKing = cell # Отмечаем данные координаты как приоритетный
            places.append(cell) # Если ячейка не пустая и фигура является противником
        else:
          if (orientation == "Up") and (orientation == "UpTwo"): # Если клетка путая, то добавляем при условии что это шаг(или два) вперёд
            places.append(cell) # Если ячейка пустая

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
    self.firstStep = False # После того, как сделан шаг, пешка теряет возможность перепрыгивать через клетку

    if self.attackOnKing:
      cell = self.attackOnKing # если есть возможность атаковать короля, атакуй !!
    else:
      cell = random.choice(self.places) # Рандом выбрал место, куда пойдёт

    self.canEat(cell)
    return cell