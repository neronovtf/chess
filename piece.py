"""Общий класс для шахматных фигур"""
import random

class Piece:
  def __init__(self, data):
    for key, value in data.items():
      setattr(self, key, value)
    self.pref = "" # Буква обозначающая фигуру N = Конь, K = Король и т.д.
    self.name = "" # Название фигуры
    self.points = 0 # Ценность фигуры. Король = 0(бесценен), Пешка = 1 Ферзь = 9 и т.д.
    self.alarm = None # сюда записывается фигура, которая представляет угрозу


  def getPlace(self): # Возвращает позицию фигуры, пример: (2,3)
    return (self.column, self.row)

  def getStrCell(self): # Возвращает позицию фигуры, понятную человеку, пример: e7
    return chr(97 + (self.column - 1)) + str(self.row)

  def move(self, newPlace): # Делает передвижение фигуры
    self.column, self.row = newPlace

  # Обязательные для реализации методы (!)
  def calculateMoves(self): pass # Выбирает один из нескольких ходов
  def canGo(self): return False # определяет, может ли фигура двигаться
