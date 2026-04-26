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
  log = [] # Логирует код, для выявления некорректного поведения
  steps = 1
  maxSteps = 500
  gameOver = False

  def __init__(self, hints = True, firstStep = "Any"): # firstStep = "Any" (White or Black), "White", "Black"
    self.nowStepWhite = self.__random()
    self.hints = hints
    self.name = "Шахматная доска"
    if self.hints:
      self.history.append("Первыми ходят " + ("белые" if self.nowStepWhite is True else "чёрные"))
    self.__createBoard()
    self.__createChessPieces()
    self.go()
    self.finish()

  def __createBoard(self):
    self.cells = {}
    for i in range(1, 9):
      for j in range(1, 9):
        self.cells[(i, j)] = None
        # self.cells[chr(97 + j) + str(i)] = None

  def __random(self):
    return bool(datetime.datetime.now().microsecond % 2)

  def __havePiece(self):
    return [(i,j) for i,j in self.cells if self.cells[(i,j)] != None]

  def __havePieceCanGoByColor(self):
    places = []
    for i, j in self.cells:
      cell = (i, j)
      valueCell = self.cells[cell]
      if valueCell is not None:
        if valueCell.isWhite == self.nowStepWhite:
          if valueCell.canGo() is True:
            places.append(cell)
    return places
    # return [(i, j) for i,j in self.cells if self.cells[(i,j)] != None   if self.cells[(i, j)].canGo() == True and self.nowStepWhite == self.cells[(i, j)].isWhite]

  def go(self):
    canGoPieces = self.__havePieceCanGoByColor()

    place = random.choice(canGoPieces)
    piece = self.cells[place]
    oldPlace = piece.getPlace()
    newPlace = piece.calculateMoves()
    self.walk(oldPlace, newPlace)

    self.nowStepWhite = not self.nowStepWhite
    self.steps += 1

    if self.gameOver is False:
      if self.steps <= self.maxSteps:
        self.go()
      else:
        print(f"Странное поведение! Прошло уже {self.maxSteps} шагов, а игра не закончена ... Завершаем принудительно!")

  def walk(self, oldPlace, newPlace):
    oldLink = self.cells[oldPlace]
    nameOldCell = oldLink.getStrCell()
    number = self.steps
    color = ""
    if self.hints:
      color = "[" + ("White" if oldLink.isWhite is True else "Black") + ", " + oldLink.name + "] "

    newLink = self.cells[newPlace]
    active = '-' # Означает что фигура просто пошла
    whoWasEaten = ""
    finalText = ""
    if newLink is not None:
      active = 'x' # Означает, что фируга съела другую фигуру

      if newLink.pref == "K": # Был съеден король, а это конец игры
        # newLink это фигура которую съедают. И если она белая, значит победили чёрные, и наоборот
        if self.hints:
          finalText += "Белые" if newLink.isWhite is False else "Чёрные"
          finalText += " победили!"
        self.gameOver = True # Останавливаем игру
      else:
        # Для понимания, какую фигуру съели. На короля не распростроняется т.к. короля формально съесть невозможно
        active += newLink.pref
        if self.hints:
          whoWasEaten += " <-- " + self.correctTextWhoEat(oldLink.name, newLink.name)

    self.cells[newPlace] = oldLink
    self.cells[oldPlace] = None

    newLink = self.cells[newPlace]
    pref = newLink.pref # Обозначение для фигуры, допустим король = K, для пешки нет буквы. Так понятно, какая фигрура ходит
    newLink.move(newPlace)

    sNumber = ""
    if self.hints:
      sNumber = str(number)
      count = 3 - len(sNumber)
      for i in range(count):
        sNumber = "0" + sNumber
      sNumber += ". "

    toGiveCheck = "" # ШАХ
    if (newLink.alarm is not None) and (newLink.pref == "K"):
      toGiveCheck = "+" # Плюс говорит о том, что Королю поставлен ШАХ
      if self.hints:
        toGiveCheck += " <-- Королю выставлен ШАХ"

    toBeCheckmated = "" # МАТ
    if self.gameOver:
      toBeCheckmated = "#" # Решётка означает, что королю был поставлен мат, и что партия закончена
      if self.hints:
        toBeCheckmated += " <-- ШАХ и МАТ. Игра окончена!"

    self.history.append(
      sNumber +
      color +
      pref +
      nameOldCell +
      active +
      newLink.getStrCell() +
      toGiveCheck +
      whoWasEaten +
      toBeCheckmated
    )
    if self.gameOver and self.hints:
      self.history.append(finalText)

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

  def __createChessPieces(self):
    startRows = [1,2,7,8]
    for row in startRows:
      for col in range(1, 9):
        isWhite = True
        if row > 2:
          isWhite = False

        data = {
          "isWhite": isWhite,
          "column": col,
          "row": row,
          "board": self.cells,
          "history": self.history,
          "log": self.log
        }

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
    for row in self.history:
        print(row)
