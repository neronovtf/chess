"""Шахматная фигура - Пешка"""
# import random
from piece import Piece

class Pawn(Piece):
  """Класс пешки"""
  def __init__(self, data):
    super().__init__(data)
    self.firstStep = True
    self.name = "Пешка"
    self.pref = "" # Раньше пешку обозначали буквой 'P', но сейчас она без буквы
    self.points = 1

  def findShifts(self, currentCol = None, currentRow = None, forKing = False):
    """
    Находит возможные ходы фигуры.

    Args:
        currentCol (int, optional): Колонка. Если None, берётся self.column.
        currentRow (int, optional): Строка. Если None, берётся self.row.
    """
    currentCol = self.column if currentCol is None else currentCol
    currentRow = self.row if currentRow is None else currentRow
    places = []

    for orientation in ["UpRight", "UpLeft", "Up", "UpTwo"]:
      ind = 1 if self.isWhite else -1

      if orientation == "UpRight":
        newCol = currentCol + 1 * ind
        newRow = currentRow + 1 * ind
      elif orientation == "UpLeft":
        newCol = currentCol - 1 * ind
        newRow = currentRow + 1 * ind
      elif orientation == "Up":
        newCol = currentCol
        newRow = currentRow + 1 * ind
      elif orientation == "UpTwo":
        # self.addLog(f"Опрашивается пешка, может ли она ходить через одну клетку ?? Это её первый шаг: {"да" if self.firstStep else "нет" }")
        if not self.firstStep: continue # если это не первый шаг фигуры, то пропускаем это действие
        newCol = currentCol
        newRow = currentRow + 2 * ind

      if not ((0 < newCol < 9) and (0 < newRow < 9)): # Не выходи за пределы игрового поля
        continue

      cell = (newCol, newRow)
      piece = self.board[cell]

      if (orientation == "Up") or (orientation == "UpTwo"):
        if piece is not None:
          break
        else:
          # if orientation == "UpTwo":
            # self.addLog("Это второй шаг, и есть возможность так ходить!!")
          places.append(cell)

      if (orientation == "UpRight") or (orientation == "UpLeft"):
        if piece is not None:
          if piece.isWhite is not self.isWhite:
            places.append(cell)
        else:
          if forKing:
            places.append(cell)
          else:
            continue


      # # Если стоит фигура, дальше смотреть нет смысла
      # if ((orientation == "Up") or (orientation == "UpTwo")) and (piece is not None):
      #   break

      # if (orientation == "Up") or (orientation == "UpTwo"): # Просто идём вперёд
      #   # Если дошёл, значит ячейка пустая
      #   places.append(cell)

      # elif (orientation == "UpRight") or (orientation == "UpLeft"): # Смотрим, можно ли кушать фигуры
      #   # Есть фигура
      #   if piece.isWhite is not self.isWhite:
      #     places.append(cell)

    return places

  # def calculateMoves(self):
  #   cell = super().calculateMoves()
  #   self.firstStep = False # После того, как сделан шаг, пешка теряет возможность перепрыгивать через клетку
  #   return cell

  # def move(self, newPlace):
  #   """Делает передвижение фигуры"""
  #   super().move(newPlace)
  #   self.firstStep = False # После того, как сделан шаг, пешка теряет возможность перепрыгивать через клетку