import random

"""Общий класс для шахматных фигур"""
class Piece:
  def __init__(self, data):
    for key, value in data.items():
      # "isWhite" - определяет цвет фигуры
      # "column" - определяет координату по вертикали
      # "row" - определяет координату по горизонтали
      # "board" - информация о шахматной доске
      # "addLog" - добавляет строку в файл лога
      # "find" - функция находит нужные элементы на доске
      # "randomBool" - функция рандомно выдаёт либо True либо False
      # "info"- словарь, служит для передачи важной информации от фигуры на доску


      setattr(self, key, value)
    self.pref = "" # Буква обозначающая фигуру N = Конь, K = Король и т.д.
    self.name = "" # Название фигуры
    self.points = 0 # Ценность фигуры. Король = 0(бесценен), Пешка = 1 Ферзь = 9 и т.д.
    self.alarms = [] # хранятся фигуры, которые угрожают нашей фигуре
    self.attackOnKing = None # У каждой фигуры, есть возможность атаковать короля
    self.attacks = [] # Хранит информацию о возможных атаках, в определённый шаг
    self.places = [] # Доступные шаги для фигур
    self.aims = []


  def icon(self):
    """Функция вернёт иконку, нужного цвета"""
    icons = {
      # White
      "bK": '♔',
      "bQ": '♕',
      "bR": '♖',
      "bB": '♗',
      "bN": '♘',
      "b": '♙',

      # Black
      "wK": '♚',
      "wQ": '♛',
      "wR": '♜',
      "wB": '♝',
      "wN": '♞',
      "w": '♟',
    }

    return icons[("w" if self.isWhite else "b") + self.pref]

  def getPlace(self):
    """Возвращает позицию фигуры, пример: (2,3)"""
    return (self.column, self.row)

  def getStrCell(self):
    """Возвращает позицию фигуры, понятную человеку, пример: e7"""
    return chr(97 + (self.column - 1)) + str(self.row)

  def move(self, newPlace):
    """Делает передвижение фигуры"""
    self.column, self.row = newPlace
    if self.pref == "": # если это Пешка
      self.firstStep = False # ставим флаг, что первый шаг более не доступен

  def findShifts(self, currentCol = None, currentRow = None, forKing = False):
    """
    Находит возможные ходы фигуры.

    Args:
        currentCol (int, optional): Колонка. Если None, берётся self.column.
        currentRow (int, optional): Строка. Если None, берётся self.row.
    """
    pass

  def walkEatKill(self, arrWalk, arrEat, cellKing):
    """Ф-я решает, что будет делать фигура? Просто ходить, есть фигуру противника или атаковать короля """

    if cellKing:
      self.addLog(f"{self.name} имеет возможность атаковать Короля на позиции {cellKing}, используем этот шанс !")
      return cellKing # если есть возможность атаковать короля, атакуй !!
    else:
      isAttack = False
      count = len(arrEat)
      if count:
        isAttack = self.randomBool()
        self.addLog(f"{self.name} имеет возможность атаковать {count} фигур противника. ПК решил {"" if isAttack else "не"} атаковать")
      else:
        self.addLog(f"{self.name} не имеет возможности атаковать фигуры противника")

      if isAttack:
        return random.choice(arrEat) # Рандом выбрал место атаки
      else:
        # Исключим атаки, из общего списка
        arr = []
        for cell in arrWalk:
          if not cell in arrEat:
            arr.append(cell)

        if len(arr) == 0:
          arr = arrWalk

        return random.choice(arr) # Рандом выбрал место, куда пойдёт

  def canGoOld(self):
    """Ф-я возвращает True - если фигура может перемещаться, и False - если фигура зажата, и не может двигаться """
    self.places = self.findShifts(self.column, self.row)
    self.addLog(f"\tКуда может пойти {self.name}: {self.places}")

    return bool(len(self.places))

  def whereGo(self):
    # Куда может пойти фигура
    places = self.findShifts()

    # Если список пустой, опросим врагов нашей фигуры, и запомним места, куда они могут пойти
    if(len(self.aims) == 0):
      temp = {}
      for enemyPiece in self.find("theirAll"):
        for place in enemyPiece.findShifts():
          temp[place] = True

      self.aims = list(temp.keys())

    attackPlaces = []
    safePlaces = []
    for place in places:
      if place is not None:
        attackPlaces.append(place) # Позиции, на которых можно съесть врага
      if place not in self.aims:
        safePlaces.append(place) # куда можно пойти, и враг тебя не атакует

    self.addLog(f"Для фигуры {self.name} находящейся по координатам {self.getPlace()}:")
    self.addLog(f"\tМожет ходить: {places}")
    self.addLog(f"\tОпасные места: {self.aims}")
    self.addLog(f"\tБезопасные места: {safePlaces}")
    self.addLog(f"\tАтакующие места: {attackPlaces}")

    # Если эта фигура, является коралём
    kingTroubles = None
    blockPiece = None
    if self.pref == "K":
      data = self.kingTroubles(places)

      self.addLog(f"\t---DATA: {data}")

      if isinstance(data[0], str):
        blockPiece = data[1]
        self.addLog("\t---DATA=1")

      elif data[0] is None:
        self.addLog("\t---DATA=2 - None ...")

      else:
        kingTroubles = data
        self.addLog("\t---DATA=3")

      # if isinstance(data[0], type):
      #   kingTroubles = data
      #   self.addLog("\t---DATA=1")

      # elif isinstance(data[0], str):
      #   blockPiece = data[1]
      #   self.addLog("\t---DATA=2")


      # Если есть угроза, тогда в переменную запишется, координата куда можно пойти, безопасно
      # Если угроз нет, выдаст None, и так мы поймём что всё окей

    if len(safePlaces):
      # Если в безопасном списке что-то есть, значит нужно исключить эти варианты из общего списка
      places = [cell for cell in places if cell not in safePlaces]

    # Возвращаем один рандомный вариант из опасного списка и безопасного списка
    return {
      "safe": random.choice(safePlaces) if len(safePlaces) else None,
      "danger": random.choice(places) if len(places) else None,
      "attack": random.choice(attackPlaces) if len(attackPlaces) else None,
      "king": kingTroubles,
      "block": blockPiece,
    }


  def canGo(self):
    for piece in self.find(): # цикл по всем фигурам на поле
      # piece.alarms = []
      pass

    self.places = self.findShifts(self.column, self.row)
    self.addLog(f"\tКуда может пойти {self.name}: {self.places}")

    return bool(len(self.places))

  def calculateMoves(self):
    cell = self.walkEatKill(self.places, self.attacks, self.attackOnKing)

    return cell

  def enemyAims(self):
    """Функция опрашивает всех противников, и узнаёт, куда они могут атаковать, и возвразает этот список"""
    aims = []
    enemyPieces = self.find("theirAll") # Получили список всех фигур противника
    for enemy in enemyPieces:
      aims += enemy.findShifts()

    return aims
