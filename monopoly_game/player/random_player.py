from .abstract_player import AbstractPlayer
from random import getrandbits

class RandomPlayer(AbstractPlayer):
  """This function decides the buying of a building,
  with enough money,
  equally and randomly between 0 and 1 as bits, 
  then transforms it into boolean before returning it.

  That's the best approach for performance so far.
  """
  def do_buy(self, building):
    return super().do_buy(building) and bool(getrandbits(1))