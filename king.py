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
    self.enemyPieces = [] # Позиции фигур противника

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

  def isNotDeadPosition(self, position):
    # если список пустой, выявляем все фигуры противника
    if len(self.enemyPieces) == 0:
      for cell in self.board:
        piece = self.board[cell]
        if piece is not None:
          if piece.isWhite != self.isWhite:
            self.enemyPieces.append(cell)

    log = f"Анализируем ситуацию, {self.name} идёт на позицию {position}. Список фигур противника с угрозами:\n"

    # Пробегаемся по списку вражеских фигур
    for enemyCell in self.enemyPieces:
      piece = self.board[enemyCell]
      log += f"\t {piece.name} на {enemyCell}. Может атаковать фигуры на позициях: {piece.newPlaces}\n"

      if position in piece.newPlaces:
        log += f"На данной позиции {self.name} грозит прямая угроза !!"
        self.log.append(log)
        return True

    log += f"Данная позиция, безопасна для {self.name}. Он будет перемещён на данную позицию"
    self.log.append(log)
    return False


  def calculateMoves(self):
    # Выбираем рандомную позицию из списка, чтобы сделать туда шаг
    cell = random.choice(self.places)
    places = self.places

    # Запускаем цикл с проверкой, что на новой позиции королю ничего не угрожает
    while self.isNotDeadPosition(cell):
        places = [item for item in places if item != cell] # исключаем из списка координату, которая является угрозой для короля
        if len(places) != 0:
          cell = random.choice(places) # рандомно выбираем координату из оставшегося списка
        else:
          print("Королю на позиции " + self.getStrCell() + " некуда ходить ...")
          break

    self.enemyPieces = [] # После проверки очищаем список
    return cell
