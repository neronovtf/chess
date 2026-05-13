"""Шахматная доска."""
import datetime
import random

from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

class Board:
  """Класс шахматная доска."""

  history = [] # Записывает историю шагов в партии
  countLog = 0
  logFile = 'app.log'
  maxCountLog = 50000
  steps = 1
  maxSteps = 500
  gameOver = False
  info = {}

  def __init__(self, firstStep = "Any", conclusion = "inDetail"):
    """
    Инициализация класса Board

    Args:
      firstStep (str, optional): Определяет, какой цвет сделает первый шаг.
        Варианты: "Any" - решает рандом, "White" - ходят первыми белые, "Black" - ходят первыми чёрные
      conclusion (str, optional): Формат вывода истории партии.
        Варианты: "inDetail" - подробное описание, "inPGN" - в формате PGN

    Returns:
      None
    """
    # Очищаем файл при создании объекта
    with open(self.logFile, 'w') as f:
      pass

    self.conclusion = conclusion
    self.nowStepWhite = self.__whoFirst(firstStep)
    self.name = "Шахматная доска"
    if self.conclusion == "inDetail":
      self.history.append("Первыми ходят " + ("белые" if self.nowStepWhite is True else "чёрные"))
    self.__createBoard()
    self.__createChessPieces()
    self.go()
    self.finish()

  def __createBoard(self):
    """
    Функция создаёт шахматную доску. Создаёт матрицу, с пустыми ячейками

    Args:
      None

    Returns:
      None
    """
    self.cells = {}
    for i in range(1, 9):
      for j in range(1, 9):
        self.cells[(i, j)] = None

  def __whoFirst(self, color):
    """
    Функция возвращает, какой цвет будет ходить первым

    Args:
      color (str): Получает пожелание, кто будет идти первым
        "Any" - случайный выбор, "White" - ходят белые, "Black" - ходят чёрные

    Returns:
      bool: Если ходят первыми белые, то вернёт True, иначе False
    """
    if color == "White":
      return True
    elif color == "Black":
      return False
    else:
      return self.randomBool()

  def __makeChoice(self):
    """
    Функция опрашивает все фигуры определённого цвета, чей сейчас ход. И рандомно выбирает из тех фигур, которые могут ходить

    Args:
      None

    Returns:
      list: Возвращает список в виде [фигура, куда она пойдёт]
    """

    # Очищаем список возможных шагов у каждой фигуры
    for piece in self.find():
      piece.aims = []

    safePieces, dangerPieces, attackPieces, kingPieces, dataKing, blockPiece  = [], [], [], [], [], None

    ourPieces = self.find("ourAll")
    for piece in ourPieces:

      data = piece.whereGo()

      if piece.pref != "K":
        if data["safe"]: safePieces.append([piece, data["safe"]])
        elif data["danger"]: dangerPieces.append([piece, data["danger"]])
        elif data["attack"]: attackPieces.append([piece, data["attack"]])

      else:
        blockPiece = data["block"] # Определяется только Королём, и указывает на фигуру, котрую нельзя двигать, дабы не подвергать короля опасностям
        dataKing += [[piece, data["safe"]], [piece, data["danger"]]]
        if data["king"]:
          kingPieces = data["king"]

    self.addLog(f"Из всех {len(ourPieces)} фигур:")
    self.addLog(f"\tБезопасно для себя, могут перемещаться: {len(safePieces)} : {safePieces}")
    self.addLog(f"\tАтакующие движения: {len(attackPieces)} : {attackPieces}")
    self.addLog(f"\tОставшиеся {len(dangerPieces)} могут быть атакованы врагом")
    self.addLog(f"\tИ данные по Королю #001: 1 - Безопасный шаг, 2 - опасный шаг: {dataKing}")
    self.addLog(f"\tИ данные по Королю #002:: {kingPieces}")
    self.addLog(f"\tВот эта фигура не должна двигаться, чтобы Королю ничего не угрожало: {blockPiece}")
    dataPiece = None

    if len(kingPieces):
      dataPiece = kingPieces
      self.addLog(f"Есть угроза Королю! Была выбрана фигура: {dataPiece[0].name}, ход с позиции {dataPiece[0].getPlace()} на позицию {dataPiece[1]}")
    else:
      self.addLog(f"Угроза для Короля отсутсвует! Будем выбирать шаг:")
      self.addLog("\tЭтап 1. Пробуем безопасно атаковать противника")

      # for attack in attackPieces:

      if len(safePieces): # Безопасное перемещение доступно
        # Рандомно выбираем фигуру
        dataPiece = random.choice(safePieces)
        self.addLog(f"Безопасное перемещение фигур доступно! Была выбрана фигура: {dataPiece[0].name}, ход с позиции {dataPiece[0].getPlace()} на позицию {dataPiece[1]}")
      else: # Безопасное перемещение доступно
        self.addLog(f"Безопасное перемещение фигур не доступно! Будем пробовать выбирать из небезопасных ...")
        if len(dangerPieces):
          dataPiece = random.choice(dangerPieces)
          self.addLog(f"Небезопасное перемещение. Была выбрана фигура: {dataPiece[0].name}, ход с позиции {dataPiece[0].getPlace()} на позицию {dataPiece[1]}")
        else:
          self.addLog("Нет ни единой возможности, пойти хотябы одной фигурой ... Игра будет закончена ...")

    return dataPiece

  def addLog(self, text):
    """
    Функция добавляет текст в лог-файл

    Args:
      text (str): Строка, которая будет добавлена в лог-файл

    Returns:
      None
    """
    self.countLog += 1

    if self.countLog >= self.maxCountLog:
      text += f"\n\nКол-во строк для логирования, достигло своего предела, игра будет закончена ..."
      self.gameOver = True

    with open(self.logFile, 'a', encoding='utf-8') as log_file:
      log_file.write(f"\nШаг {self.__getStep()}{text}")

  def __getStep(self):
    """
    Функция возвращает номер строки

    Args:
      None

    Returns:
      str: выводит номер строки в виде 003, 038, 107
    """
    sNumber = str(self.steps)
    count = 3 - len(sNumber)
    for i in range(count):
      sNumber = "0" + sNumber
    sNumber += ". "

    return sNumber

  def go(self):

    dataPiece = self.__makeChoice()
    self.addLog(f"\t**{dataPiece}")
    if dataPiece:
      tt = dataPiece[0].getPlace()
      self.addLog(f"\t**{tt}")
      self.addLog(f"\t**{self.cells[tt]}")

    for item in self.find("ourAll"):
      self.addLog(f"\t**{item.getPlace()} >> {item}")


    if dataPiece is None:
      self.gameOver = True
    else:
      self.walk(dataPiece[0].getPlace(), dataPiece[1])

    self.nowStepWhite = not self.nowStepWhite
    self.screenBoard()
    self.addLog("================================================================================\n")
    self.steps += 1

    if self.gameOver is False:
      if self.steps <= self.maxSteps:
        self.go()
      else:
        self.addLog(f"Странное поведение! Прошло уже {self.maxSteps} шагов, а игра не закончена ... Завершаем принудительно!")

  def find(self, rule = "all"):
    # returnFirst = False

    if rule == "ourAll":
      def condition(piece): return piece.isWhite is self.nowStepWhite
      def finish(list): return list

    elif rule == "theirAll":
      def condition(piece): return piece.isWhite is not self.nowStepWhite
      def finish(list): return list

    elif rule == "ourKing":
      def condition(piece): return (piece.isWhite is self.nowStepWhite) and (piece.pref == "K")
      def finish(list): return list[0] if len(list) else None

    elif rule == "theirKing":
      def condition(piece): return (piece.isWhite is not self.nowStepWhite) and (piece.pref == "K")
      def finish(list): return list[0] if len(list) else None

    else:
      def condition(piece): return True
      def finish(list): return list

    pieces = []
    for cell in self.cells:
      if self.cells[cell] is not None:
        piece = self.cells[cell]
        if condition(piece):
          pieces.append(piece)

    return finish(pieces)

  def chessCoord(self, cell):
    return chr(97 + (cell[0] - 1)) + str(cell[1])

  def checkKing(self):
    """
    Ф-я опрашивает Короля, есть ли для него угроза и выводит результат

    Args:
      Аргументы отсутствуют

    Returns:
      String: Вернёт "+", если королю выставлен ШАХ, и "" если ШАХа нет
    """
    king = self.find("ourKing") # Обращаемся к нашему Королю
    isDanger = king.thisThreat() # Узнаём от него, если ли угроза

    return "+" if isDanger else ""

  def promotionPawn(self, piece, newPlace):
    """
    Ф-я отработает только на пешках, которые достигли поля превдащения

    Args:
      piece (class): Фигура, которая делает перемещение. Должна быть пешкой Pawn
      newPlace (tuple): Координаты нового места, куда попадёт фигура

    Returns:
      String: Вернёт "" если условия не соблюдены, и букву "R","N","B","Q" если пешка совершила превращение
    """

    if piece.pref != "":
      return ""

    self.addLog(f"\tПешка :: Её новые координаты: {newPlace}")

    if piece.isWhite:
      if newPlace[1] != 8: # Смотрим новое значение ряда
        return "" # Если белая пешка, не дошла до самого верхнего ряда, нам не интересно
    else:
      if newPlace[1] != 1: # Смотрим новое значение ряда
        return "" # Если чёрная пешка, не дошла до самого нижнего ряда, нам не интересно

    self.addLog("Пешка достигла поля превращения !!")
    # Рандом решит, в какую фигуру преобразуется пешка, которая дошла до конца
    newEntity = random.choice(["R", "N", "B", "Q"])

    data = self.__getData({
      "isWhite": piece.isWhite,
      "column": newPlace[0],
      "row": newPlace[1],
    })

    obj = None
    if newEntity == "R": obj = Rook(data)
    elif newEntity == "N": obj = Knight(data)
    elif newEntity == "B": obj = Bishop(data)
    elif newEntity == "Q": obj = Queen(data)

    self.addLog(f"Пешка превращается в - {obj.name}")
    self.info["promotion"] = obj

    return newEntity


    # ((newLink.isWhite and newLink.column == 8) or (not newLink.isWhite and newLink.column == 1))
    # Ф-я сработает только для пешек, которые дошли до противоположной стороны поля и преобразовались в другую фигуру, допустим: Q, N,...
    # data = self.__getData({
    #   "isWhite": isWhite,
    #   "column": col,
    #   "row": row,
    # })
    # self.cells[cell] = Rook(data)
    # self.cells[cell] = Knight(data)
    # self.cells[cell] = Bishop(data)
    # self.cells[cell] = Queen(data)
    # pass

  def inDetail(self, oldPlace, newPlace):
    oldLink = self.cells[oldPlace]
    newLink = self.cells[newPlace]
    hints = ""
    def addHint(text):
      if len(hints):
        hints += " + " + text
      else:
        hints += text

    def getHint():
      return (" <-- " + hints) if len(hints) else ""

    detail = "" # Начало строки

    detail += self.__getStep() # Записывает номер хода, пример: "001. "
    detail += "[" + ("White" if oldLink.isWhite is True else "Black") + ", " + oldLink.name + "] " # Выглядит примерно так: "[White, Слон] "
    detail += oldLink.pref # Берём букву фигуры, которая будет ходить
    detail += oldLink.getStrCell() # Берём координату фигуры, откуда она будет ходить

    if newLink is not None:
      detail += "x" # Происходит поедание фигуры противника
      detail += newLink.pref # Записываем букву фигуры, которую поедаем
      addHint(self.correctTextWhoEat(oldLink.name, newLink.name))
    else:
      detail += "-" # Этот символ говорит о том, что фигура перешла на пустую ячейку

    detail += self.chessCoord(newPlace) # Координаты, новой позиции, допустим - e5
    detail += self.promotionPawn(oldLink, newPlace) # Преобразование пешки, которая дошла до конца

    isCheck = self.checkKing() # Проверяем, поставили ли Королю - ШАХ
    if len(isCheck):
      detail += isCheck
      addHint("Королю выставлен ШАХ")

    if (newLink is not None) and (newLink.pref == "K"): # Проверяем, поставили ли Королю - МАТ
      detail += "#"
      addHint("Королю выставлен МАТ")

    detail += getHint() # В конце добавим подсказки

    self.history.append(detail)


  def inPGN(self, oldPlace, newPlace):
    oldLink = self.cells[oldPlace]
    newLink = self.cells[newPlace]

    self.addLog(f"\t{oldLink} <-=2=-> {newLink}")

    pref = oldLink.pref # Запоминаем букву фигуры
    oldCoord = oldLink.getStrCell()

    pgn = pref # Берём букву фигуры, которая будет ходить
    # pgn += "x" if newLink is not None else "" # Если происходит поедание фигуры то - x
    pgn += oldCoord # Координаты, старой позиции, допустим - e4
    if newLink is not None:
      # if pref == "":
      #   pgn += oldCoord[0]
      pgn += "x"
    else:
      pgn += ""
    pgn += self.chessCoord(newPlace) # Координаты, новой позиции, допустим - e5
    pgn += self.promotionPawn(oldLink, newPlace) # Преобразование пешки, которая дошла до конца
    pgn += self.checkKing() # Проверяем, поставили ли Королю ШАХ
    if (newLink is not None) and (newLink.pref == "K"):
      pgn += "#"

    self.history.append(pgn)

  def walk(self, oldPlace, newPlace):

    oldLink = self.cells[oldPlace]
    newLink = self.cells[newPlace]

    self.addLog(f"\t{oldLink} <-=1=-> {newLink}")
    self.addLog(f"\t{oldPlace} <-=1.1=-> {newPlace}")

    if self.conclusion == "inDetail":
      self.inDetail(oldPlace, newPlace)
    elif self.conclusion == "inPGN":
      self.inPGN(oldPlace, newPlace)

    if (newLink is not None) and (newLink.pref == "K"):
      self.gameOver = True # Останавливаем игру

    if self.gameOver and (self.conclusion == "inDetail"):
      self.history.append(("Белые" if oldLink.isWhite else "Чёрные") + " победили!")

    # Перемещаем фигуру со старой позации на новую

    # self.info["promotion"] = obj
    promotion = self.info.get("promotion", None)
    if promotion:
      self.addLog(f"Есть замеша пешки на другую фигуру !!! Новые координаты: {newPlace}, а фигура, это: {promotion.name} на позиции {promotion.getPlace()}")
      self.cells[newPlace] = promotion # Если есть подмена фигуры, реализуем
      del self.info["promotion"] # Удаляем из объекта, там больше это не нужно
    else:
      oldLink.move(newPlace) # Передаём классу фигуры, её новые координаты
      self.cells[newPlace] = oldLink # Присваиваем ячейке ссылку на объект, со старого места
    self.cells[oldPlace] = None # Очищаем старую позицию

  def correctTextWhoEat(self, nameLivePiece, nameKillPiece):
    word = "съел"
    lastLetterLivePiece = nameLivePiece[len(nameLivePiece)-1]
    if lastLetterLivePiece in ["a", "я"]:
      word += "a"

    lastCharacter = len(nameKillPiece)-1
    lastLetterKillPiece = nameKillPiece[lastCharacter]
    if lastLetterKillPiece == "ь":
      nameKillPiece = nameKillPiece[:-1] + "я"
    elif lastLetterKillPiece == "н":
      nameKillPiece += "а"
    elif lastLetterKillPiece == "а":
      nameKillPiece = nameKillPiece[:-1] + "у"
    elif lastLetterKillPiece == "я":
      nameKillPiece = nameKillPiece[:-1] + "ю"

    nameKillPiece = nameKillPiece.lower()

    return f"{nameLivePiece} {word} {nameKillPiece}"

  def randomBool(self):
    """
    Функция возвращает True \ False в рандомном порядке (привязано к миллисекундам)

    Args:
      None

    Returns:
      bool: Функция возвращает True \ False в рандомном порядке (привязано к миллисекундам)
    """
    return bool(datetime.datetime.now().microsecond % 2)

  def __getData(self, data):
    obj = {
      "board": self.cells,
      "addLog": self.addLog,
      "find": self.find,
      "randomBool": self.randomBool,
    }

    return obj | data


  def __createChessPieces(self):
    startRows = [1,2,7,8]
    for row in startRows:
      for col in range(1, 9):
        isWhite = True
        if row > 2:
          isWhite = False

        data = self.__getData({
          "isWhite": isWhite,
          "column": col,
          "row": row,
        })

        cell = (col, row)
        if row == 2 or row == 7:
          self.cells[cell] = Pawn(data)
        else:
          if col == 1 or col == 8:    self.cells[cell] = Rook(data)
          elif col == 2 or col == 7:  self.cells[cell] = Knight(data)
          elif col == 3 or col == 6:  self.cells[cell] = Bishop(data)
          elif col == 4:              self.cells[cell] = Queen(data)
          elif col == 5:              self.cells[cell] = King(data)

  def finish(self):

    if self.conclusion == "inDetail":
      for row in self.history:
        print(row)



    elif self.conclusion == "inPGN":
      ind, isRow, text = 1, True, ""

      for row in self.history:

        if isRow:
          text += f"{ind}. "
          ind += 1

        text += f"{row} "
        isRow = not isRow

      print(text)

    # if self.hints_old:
      # for row in self.history:
      #   print(row)
    # else:
    #   # Если без подсказок, то выводим по нормам PGN
    #   # 1. f2-f4 Nb8-a6 2. h2-h4 e7-e5 3. d2-d3 f7-f6 4. a2-a4 e5-e4 5. Ra1-a3 Na6-b4 6. Nb1-d2 c7-c5
    #   ind = 1
    #   isRow = True
    #   text = ""

    #   for row in self.history:

    #     if isRow:
    #       text += f"{ind}. "
    #       ind += 1

    #     text += f"{row} "
    #     isRow = not isRow

    #   print(text)

  def screenBoard(self):
    clearCell = '  '
    text = "\n"

    for row in range(8, 0, -1):
      text += "\n\t"

      for col in range(1,9):
        piece = self.cells[(col, row)]

        if piece is not None:
          text += piece.icon()
        else:
          text += clearCell

    text += "\n"
    self.addLog(text)
