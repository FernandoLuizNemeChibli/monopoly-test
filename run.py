from csv import DictReader
from os import path
from game_analysis import GameAnalysis
from monopoly_game import Building
from monopoly_game import GameTable
from monopoly_game.player import CautiousPlayer
from monopoly_game.player import DemandingPlayer
from monopoly_game.player import ImpulsivePlayer
from monopoly_game.player import RandomPlayer

"""This method instantiates all monopoly_game components
returns GameTable loaded
"""
def load_game():
  game_table = GameTable()

  game_table.add_player(CautiousPlayer("Cautious Player"))
  game_table.add_player(DemandingPlayer("Demanding Player"))
  game_table.add_player(ImpulsivePlayer("Impulsive Player"))
  game_table.add_player(RandomPlayer("Random Player"))

  with open(path.join('resource','buildings.csv')) as buildings_csv:
    building_list = [{key: val for key, val in row.items()}
      for row in DictReader(buildings_csv)]

  """this iteration sanitize the list, removing the ones that doesn't have rent_2 value,
  then uses its firsts 20 data to instance a Building and add in the game_table
  """
  building_count = 0
  for building_dict in filter(lambda building: len(building['rent_2']), building_list):
    game_table.add_building(
      Building(
        name = building_dict['name'],
        sell_cost = int(building_dict['cost']),
        rent_cost = int(building_dict['rent_2'])
      )
    )
    building_count += 1
    if building_count == 20:
      break
  return game_table

"""this method instantiates and executes GameAnalysis, 
which will execute and analyze the GameTable instance.
"""
def run_analysis():
  game_table = load_game()
  game_analysis = GameAnalysis(game_table)
  game_analysis.run()