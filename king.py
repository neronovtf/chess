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

    kingEnemy = self.find("theirKing")
    placesKingEnemy = kingEnemy.ring()

    # Нужно проверить два круга вокруг короля т.к. короли не могут находиться на соседних клетках
    for newCol in range(currentCol - 2, currentCol + 3):
      # haveKing = False
      for newRow in range(currentRow - 2, currentRow + 3):

        if newCol == currentCol and newRow == currentRow: # Игнорируем позиции, где находится наша фигура
          continue

        if not ((0 < newCol < 9) and (0 < newRow < 9)): # Не выходи за пределы игрового поля
          continue

        cell = (newCol, newRow)
        piece = self.board[cell]

        #  !!!! Странное условие ...
        # if (piece is not None) and (piece.pref == self.pref): # Если совпадают, значит это король
        #   haveKing = True
        #   places = [] # Обнуляем список доступных шагов т.к. двигаться нельзя
        #   self.addLog(f"Король, на позиции {self.getPlace()} обнаружил, рядом с собой другого короля на позиции: {piece.getPlace()}. Движение короля, невозможно ... ") # Почему ?!
        #   break # Прерываем циклы, нет смысла проверять всё остальное

        if(abs(newCol - currentCol) <= 1 and abs(newRow - currentRow) <= 1): # Ячейки, вокруг нашей фигуры

          if cell in placesKingEnemy:
            continue

          if piece is None:
            # Ячейка пустая
            places.append(cell)
          else:
            # Есть фигура
            if piece.isWhite is not self.isWhite:
              places.append(cell)

      # Конец первого цикла
      # if haveKing:
        # break # Прерываем первый цикл т.к. в ближнем окружении был найден второй король

    return places

  def ring(self):
    """
    Ф-я возвращает список координат, вокруг себя. Игнорируются другие фигуры. В списке будет 8 координат, меньше, если король стоит у края

    Args:
      Аргументы отсутствуют

    Returns:
      list: Список, с координатами, куда может пойти Король
    """
    currentCol = self.column
    currentRow = self.row
    places = []

    for i in range(currentCol-1, currentCol+2):
      for j in range(currentRow-1, currentRow+2):
        if i == currentCol and j == currentRow:
          continue

        places.append((i, j))

    return places

  def forPawn(self, pawn):
    ind = 1 if pawn.isWhite else -1
    places = []

    for i in [1, -1]:
      newCol = pawn.column + i * ind
      newRow = pawn.row + 1 * ind
      if not ((0 < newCol < 9) and (0 < newRow < 9)): # Не выходи за пределы игрового поля
        continue

      cell = (newCol, newRow)
      piece = self.board[cell]
      if piece is not None:
        if piece.isWhite is pawn.isWhite:
          places.append(cell) # если цвет совпадает с противником, то король может съесть эту фигуру и попасть на его место и быть съеден
      else:
        places.append(cell) # король может попасть на это место и быть съеден

    return places

  def thisThreat(self):
    """
    Ф-я сообщает, что Королю поставлен ШАХ

    Args:
      Аргументы отсутствуют

    Returns:
      bool: Если True, королю выставлен ШАХ, если False - угрозы королю нет
    """
    coord = self.getPlace()
    for piece in self.find("theirAll"):
      places = piece.findShifts()
      if coord in places:
        return True

    return False


  def isNotDeadPosition(self, position): # True - Проблема есть, False - Проблемы нет
    # если список пустой, выявляем все фигуры противника
    # if len(self.enemyPieces) == 0:
    #   for cell in self.board:
    #     piece = self.board[cell]
    #     if piece is not None:
    #       if piece.isWhite != self.isWhite:
    #         self.enemyPieces.append(cell)

    log = f"Анализируем ситуацию, {self.name} идёт на позицию {position}. Список фигур противника:"

    # Пробегаемся по списку вражеских фигур
    for piece in self.theirPieces:
      cell = piece.getPlace()
      if piece.pref == "": # Отдельное условие для пешки
        mines = self.forPawn(piece)
      else:
        mines = piece.findShifts(cell[0], cell[1]) # !!!
      log += f"\n\t{piece.name} на {cell}. Может атаковать фигуры на позициях: {mines}. "

      if position in mines:
        log += " <-- Данная фигура угрожает королю !!"
        self.addLog(log)
        return True
      else:
        log += " <-- Угроз не обнаружено"

    log += f"\n\t[!] Все фигуры противника проанализированы, угроз для короля не обнаружено"
    self.addLog(log)
    return False


  def calculateMoves(self):
    # Выбираем рандомную позицию из списка, чтобы сделать туда шаг
    if(len(self.places) == 0):
      # print("Было найдено:", self.places)
      return None

    cell = random.choice(self.places)
    places = self.places
    self.theirPieces = self.find("theirAll")

    self.addLog(f"Начинается ЦИКЛ ... Королю доступны ходы: {places}, в самом начале, жребий пал на: {cell}")

    # Запускаем цикл с проверкой, что на новой позиции королю ничего не угрожает
    while self.isNotDeadPosition(cell):
        self.addLog(f"{cell} -- не подошёл ... Исключим этот вариант из списка")
        places = [item for item in places if item != cell] # исключаем из списка координату, которая является угрозой для короля
        cell = None # Обнуляем список, если запрещён ход для короля ...
        self.addLog(f"Список доступных шагов для Короля, теперь выглядит вот так: {places}")

        if len(places) != 0:
          cell = random.choice(places) # рандомно выбираем координату из оставшегося списка
          self.addLog(f"Теперь же, выбор пал на: {cell}")
        else:
          # print("Королю на позиции " + self.getStrCell() + " некуда ходить ...")
          self.addLog("Королю на позиции " + self.getStrCell() + " некуда ходить ...")
          break

    self.enemyPieces = [] # После проверки очищаем список
    return cell

  def kingTroubles(self, whereGo): # whereGo - куда может пойти Король
    temp = {}
    enemies = []
    kingCoord = self.getPlace()
    # Пробегаемся по всем вражеским фигурам
    for enemyPiece in self.find("theirAll"):
      # Прокидывае аргумент, что результат нужен для Короля
      places = enemyPiece.findShifts(forKing = True)
      self.addLog(f"\t>-> Фигура {enemyPiece}, куда может ходить: {places}")
      # savePieces.append([enemyPiece, places])
      for place in places:
        temp[place] = True
        if place == kingCoord:
          enemies.append(enemyPiece)

    # Получили места, куда могут атаковать противники
    kingAims = list(temp.keys())

    self.addLog(f"Начинается проверка Короля на позиции {kingCoord}")
    self.addLog(f"Противники Короля, могут пойти вот сюда: {kingAims}")

    isAlarm = False
    defender = None
    if kingCoord in kingAims:
      if self.thisThreat():
        self.addLog("Король находится под ударом")
        isAlarm = True
      else:
        self.addLog(f"Король находится не под прямым ударом. Скорее всего, его защищает какая-то фигура. Угроза исходит от: {enemies}")
        self.addLog("Сейчас попрбуем определить, что это за фигура, и убрать у неё возможность ходить, чтобы исключить возможность открытия короля !")
        if len(enemies) == 1:
          enemy = enemies[0]
          steps = self.cellsBetween(self, enemy)
          self.addLog(f"Список ячеек между королём и угрозой: {steps}")
          for step in steps:
            piece = self.board[step]
            if (piece is not None) and (piece.isWhite is self.isWhite):
              defender = piece
              break

          if defender:
            self.addLog(f"Защитник найден, это: {defender}")
          else:
            self.addLog("Защитник не найден ...")

        else:
          self.addLog(f"Кол-во угроз для Короля = {len(enemies)}, такое, я пока не обрабатываю ...")


    # Проверяем текущую позицию Короля
    if isAlarm:
      self.addLog("Шаг 0. Пробуем убежать ...")
      # Пробуем убежать Королём
      safePieces = []
      for cell in whereGo:
        text = f"\tПозиция {cell} является: "
        if cell in kingAims:
          text += "опасной! т.к. находится в списке атак!!"
        else:
          text += "безопасной! т.к. отсутсвует в списке атак!!"
          safePieces.append(cell)
        self.addLog(text)


      if len(safePieces):
        self.addLog("Есть возможность убежать, её и реализуем!")
        return [self, random.choice(safePieces)]
      else:
        self.addLog("Нет возможности убежать ...")
        # Пробуем защититься или атаковать ...
        return self.coverAttack(enemies, kingAims)

    else:
      text = "Королю, ничего не угрожает"
      if defender:
        text += ", потому что, есть защитник! И ему нельзя двигаться!!"
        self.addLog(text)
        return ["block", defender]
      else:
        text += ", и он никем не прикрывается!"
        self.addLog(text)
        return [None, None]

  def cellsBetween(self, firstPiese, secondPiese):
    # print(firstPiese, secondPiese)

    # if (firstPiese is None) or (secondPiese is None):
    #   self.addLog(f"В функцию 'cellsBetween' переданы пустые фигуры .. 1){firstPiese}, 2){secondPiese}")
    #   return []

    firstCoord = firstPiese.getPlace()
    secondCoord = secondPiese.getPlace()

    addCol, addRow = 0, 0

    if firstCoord[0] > secondCoord[0]: addCol = 1
    elif firstCoord[0] == secondCoord[0]: addCol = 0
    else: addCol = -1

    if firstCoord[1] > secondCoord[1]: addRow = 1
    elif firstCoord[1] == secondCoord[1]: addRow = 0
    else: addRow = -1

    # Идём от короля к угрозе
    steps = []
    newCol = secondCoord[0]
    newRow = secondCoord[1]
    for i in range(1, 9):
      newCol += addCol
      newRow += addRow
      if(newCol == firstCoord[0]) and (newRow == firstCoord[1]):
        break
      steps.append((newCol, newRow))

    return steps

  def coverAttack(self, enemies, kingAims):
    if len(enemies) == 1:
      # Определили какая фигура нам угрожает
      enemy = enemies[0]

      enemyCoord = enemy.getPlace()
      kingCoord = self.getPlace()

      self.addLog("Шаг 1. Пробуем атаковать фигуру, которая угрожает королю")

      # Опрашиваем своих, куда они могут пойти
      ourPieces = self.find("ourAll")
      # В начале пробуем атаковать
      ourPlaces = []
      killer = []
      for piece in ourPieces:
        places = piece.findShifts()
        ourPlaces.append([piece, places])
        for place in places:
          if place == enemyCoord:
            killer += [piece, place]
            break
        if len(killer) > 0:
          break

      if len(killer):
        self.addLog(f"Шаг 1. Итог: была найдена! Это {killer[0].name}, пойдёт с координаты {killer[0].getPlace()} на координату {killer[1]}")
        return killer
      else:
        self.addLog(f"Шаг 1. Итог: Нет такой возможности ...")
        self.addLog(f"Шаг 2. Пробуем укрыться от противника. Для начала определим, в какой стороне от короля находится угроза")

        steps = self.cellsBetween(enemy, self)
        # addCol, addRow = 0, 0

        # if enemyCoord[0] > kingCoord[0]: addCol = 1
        # elif enemyCoord[0] == kingCoord[0]: addCol = 0
        # else: addCol = -1

        # if enemyCoord[1] > kingCoord[1]: addRow = 1
        # elif enemyCoord[1] == kingCoord[1]: addRow = 0
        # else: addRow = -1

        # # Идём от короля к угрозе
        # steps = []
        # newCol = kingCoord[0]
        # newRow = kingCoord[1]
        # for i in range(1, 9):
        #   newCol += addCol
        #   newRow += addRow
        #   if(newCol == enemyCoord[0]) and (newRow == enemyCoord[1]):
        #     break
        #   steps.append((newCol, newRow))

        self.addLog(f"Шаг 2. Мы нашли все шаги от Короля до угрозы, вот они: {steps}")
        self.addLog(f"Шаг 2. Теперь нужно определить, могут ли наши фигуры занять какую-то из ячеек ?")

        text = ""
        for step in steps:
          text += f"Позиция {step}:"
          for data in ourPlaces:
            piece = data[0]
            if piece.pref == "K": continue
            cells = data[1]
            text += f"\n\tФигура {piece.name} на координате {piece.getPlace()} - "
            if step in cells:
              text += "Может занять нужную позицию !!"
              self.addLog(f"Шаг 2. {text}")
              return [piece, step]
            else:
              text += "Не может занять, нужную позицию ..."

        self.addLog(f"Шаг 2. {text}")
        self.addLog(f"Шаг 2. К сожалению ... У Короля нет возможности прикрыться другими фигурами ...")
        self.addLog(f"Для Короля, нет возможности спастись ...")
        return [None, None]

        # ourPlaces


        # Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft
        # eC, eR = enemyCoord
        # kC, kR = kingCoord
        # travel = None
        # text = "От короля, нужно двигаться: "

        # if eC == kC: # Значит угроза по вертикали: Up + Down
        #   if eR > kR: # Значит угроза находится выше короля
        #     travel = "Up" # От короля, нужно двигаться вверх
        #     text += "вверх"
        #   else: # Иначе
        #     travel = "Down" # От короля, нужно двигаться вниз
        #     text += "вниз"

        # if eR == kR: # Значит угроза по горизонтали: Right + Left
        #   if eC > kC: # Значит угроза находится с права от короля
        #     travel = "Right" # От короля, нужно двигаться в право
        #     text += "на право"
        #   else: # Иначе
        #     travel = "Left" # От короля, нужно двигаться в лево
        #     text += "на лево"

        # if (eC > kC) and (eR > kR):
        #   travel = "UpRight" # От короля, нужно двигаться в правый верхний угол
        #   text += "в правый верхний угол"

        # if (eC < kC) and (eR < kR):
        #   travel = "DownLeft" # От короля, нужно двигаться в левый нижний угол
        #   text += "в левый нижний угол"

        # if (eC < kC) and (eR > kR):
        #   travel = "UpLeft" # От короля, нужно двигаться в левый верхний угол
        #   text += "в левый верхний угол"

        # if (eC > kC) and (eR < kR):
        #   travel = "DownRight" # От короля, нужно двигаться в правый нижний угол
        #   text += "в правый нижний угол"

        # self.addLog(text)







    else:
      self.addLog(f"На короля, нацелились одновременно: {len(enemies)}, это из ряда вон выходящяя ситуация ...")
      return [None, None]
