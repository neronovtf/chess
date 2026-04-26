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
    """Функция опрашивает все фигуры, оставшиеся на поле, и уточняет могут ли они ходить"""
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

  def findDangerKing(self, places):
    dangers = []
    for cell in places:
      if self.cells[cell].attackOnKing is not None:
        dangers.append(cell)
    return dangers

  def go(self):
    canGoPieces = self.__havePieceCanGoByColor()
    dangers = self.findDangerKing(canGoPieces)
    if dangers:
      canGoPieces = dangers # если есть фигуры, угрожающие королю, выбирать нужно из них

    # Рандомом выбираем координаты фигуры, которая будет ходить
    place = random.choice(canGoPieces)
    # Получаем фигуру
    piece = self.cells[place]
    oldPlace = piece.getPlace()
    # Фигура, через рандом (у себя) выбирает, какой она сделает шаг
    newPlace = piece.calculateMoves()
    self.walk(oldPlace, newPlace)

    self.nowStepWhite = not self.nowStepWhite
    self.steps += 1

    if self.gameOver is False:
      if self.steps <= self.maxSteps:
        self.go()
      else:
        print(f"Странное поведение! Прошло уже {self.maxSteps} шагов, а игра не закончена ... Завершаем принудительно!")

  def findKingOpponent(self):
    for i, j in self.cells:
      if self.cells[(i,j)] is not None:
        piece = self.cells[(i,j)]
        if(piece.pref == "K") and (piece.isWhite is not self.nowStepWhite):
          return piece

  def walk(self, oldPlace, newPlace):
    oldLink = self.cells[oldPlace]
    nameOldCell = oldLink.getStrCell()
    number = self.steps
    color = ""
    if self.hints:
      color = "[" + ("White" if oldLink.isWhite is True else "Black") + ", " + oldLink.name + "] "

    newLinkBeforeChange = self.cells[newPlace]
    active = '-' # Означает что фигура просто пошла
    whoWasEaten = ""
    finalText = ""
    if newLinkBeforeChange is not None:
      active = 'x' # Означает, что фируга съела другую фигуру

      if newLinkBeforeChange.pref == "K": # Был съеден король, а это конец игры
        # newLinkBeforeChange это фигура которую съедают. И если она белая, значит победили чёрные, и наоборот
        if self.hints:
          finalText += "Белые" if newLinkBeforeChange.isWhite is False else "Чёрные"
          finalText += " победили!"
        self.gameOver = True # Останавливаем игру
      else:
        # Для понимания, какую фигуру съели. На короля не распростроняется т.к. короля формально съесть невозможно
        active += newLinkBeforeChange.pref
        if self.hints:
          whoWasEaten += " <-- " + self.correctTextWhoEat(oldLink.name, newLinkBeforeChange.name)

    # Перемещаем фигуру со старой позации на новую
    self.cells[newPlace] = oldLink
    # Очищаем старую позицию
    self.cells[oldPlace] = None

    # Переназначаем переменную, которая отвечала за новую позицию фигуры
    newLink = self.cells[newPlace]

    # Передаём классу фигуры, её новые координаы
    newLink.move(newPlace)

    # Блок, отвечает за нумерцию шагов, пример: 001, 002 и т.д.
    sNumber = ""
    if self.hints: # Если включены подсказки
      sNumber = str(number)
      count = 3 - len(sNumber)
      for i in range(count):
        sNumber = "0" + sNumber
      sNumber += ". "

    toGiveCheck = "" # ШАХ

    if newLink.pref != "K":
      pieceKingOpponent = self.findKingOpponent()
      if (pieceKingOpponent is not None) and (pieceKingOpponent.alarm == newLink):
        toGiveCheck = "+" # Плюс говорит о том, что Королю поставлен ШАХ
        if self.hints:
          toGiveCheck += " <-- Королю выставлен ШАХ"
          if whoWasEaten:
            whoWasEaten = whoWasEaten.replace("<--", "+")

    toBeCheckmated = "" # МАТ
    if self.gameOver:
      toBeCheckmated = "#" # Решётка означает, что королю был поставлен мат, и партия закончена
      if self.hints:
        toBeCheckmated += " <-- ШАХ и МАТ. Игра окончена!"

    self.history.append(
      sNumber +
      color +
      newLink.pref +
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
          "log": self.log,
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
