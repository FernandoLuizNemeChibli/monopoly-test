import logging as log
import random

"""This class manages all players, buildings and its tools.
According to the phases of a players shift, 
  this class implements functions to trigger the actions of its agents.
"""
class GameTable:
  def __init__(self, players = [], buildings = [], dice_faces = 6, turn_payment = 100, turns_limit = 1000):
    self._players = players
    self._buildings = buildings
    self._dice_faces = dice_faces
    self._turn_payment = turn_payment
    self._winner = None
    self._turns_counter = 0
    self._turns_limit = turns_limit
    """do the first shuffle"""
    self.shuffle_players()

  def reset(self):
    self._winner = None
    self._turns_counter = 0
    self.shuffle_players()
    for player in self._players:
      player.reset()
    for building in self._buildings:
      building.reset()

  def get_winning_ratio(self):
    winning_ratio = {}
    for player in self._players:
      winning_ratio[type(player).__name__] = {
        "name": player.get_name(),
        "winning_count": player.get_winning_count()
      }
    return winning_ratio

  def get_turns_counter(self):
    return self._turns_counter
  
  def has_timedout(self):
    return self._turns_counter >= self._turns_limit

  def add_player(self, player):
    self._players.append(player)
    log.info(f'add player {player.get_name()}')

  def add_building(self, building):
    self._buildings.append(building)
    log.info(f'add building {building.get_name()}')

  def shuffle_players(self):
    random.shuffle(self._players)
  
  """TODO: create separate class for Dice and DicePooling"""
  def roll_dice(self):
    return random.randint(1, self._dice_faces)

  """The following function moves a given player through the buildings list.
  The movement is equivalent of the dice rolling result.
  If the player position exceeds the number of buildings, the movement is subtracted with this number, simulating a circuit.
  """
  def move_player(self, player):
    dice_result = self.roll_dice()
    player.move_position(dice_result)
    log.info(f'player got dice {dice_result}, moved to: {player.get_position()}')
    if (player.get_position() >= len(self._buildings)):
      player.move_position(-len(self._buildings))
      log.info(f'player realocated to: {player.get_position()}')
      player.receive_money(self._turn_payment)

  """Once moved, the player must enter the building of its position.
  The following funciton apply all the actions of entering a building.
  If previously owned, the player must pay the rent for the owner, otherwise it is opened for appropriation.
  The given player is willing to buy according the do_buy abstrct method.
  """
  def enter_building(self, player):
    building = self._buildings[player.get_position()]
    log.info(f'{player.get_name()} is entering {building.get_name()}')
    if (player != building.get_owner()):
      if (building.get_owner()):
        player.pay_rent(building)
        log.info(f'Payed {building.get_rent_cost()}$ for rent to {building.get_owner().get_name()}')
      elif (player.do_buy(building)):
        player.buy_building(building)
        building.appropriate_building(player)
        log.info(f'Bought building for {building.get_sell_cost()}$')

  """Applied all the previous actions, the given player must end its shift.
  The following function verifies if the player lost the game and, 
    if confirmed, expropriates all its buildings in this game table
  """
  def end_shift(self, player):
    if (not player.is_playing()):
      log.info(f'player {player.get_name()} lost the game')
      for building in filter(lambda building: building.get_owner() == player, self._buildings):
        building.expropriate_building()

  def end_turn(self):
    self._turns_counter += 1
    current_players = list(filter(lambda player: player.is_playing(), self._players))
    if len(current_players) == 1:
      self._winner = current_players[0]

  def end_by_timeout(self):
    self._winner = next(filter(lambda player: player.is_playing(), self._players))

  """Runs the phases of a turn, iterating players until the end condition of the game is fulfiled."""
  def run(self):
    while not self._winner and not self.has_timedout():
      for player in filter(lambda player: player.is_playing(), self._players):
        log.info(f'player {player.get_name()} turn')
        self.move_player(player)
        self.enter_building(player)
        self.end_shift(player)
      self.end_turn()

    if not self._winner:
      self.end_by_timeout()

    self._winner.won()
    log.info(f'player {self._winner.get_name()} won the game in {self._turns_counter} turns, with {self._winner.get_money()}$.')