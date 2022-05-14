import json

class Pokedex(object):
    def __init__(self):      
        self.pokedex = self.load_pokedex()        

    def load_pokedex(self):
        with open("data/pokedex.json") as dex_file:
            pokedex = json.load(dex_file)
            return pokedex

    def get_pokemon_name(self, id):
        for pokemon in self.pokedex:
            if pokemon["pokemon_id"] == id:
                return pokemon["pokemon_name_de"]

    def get_pvp_check_ids(self, id):
        for pokemon in self.pokedex:
            if pokemon["pokemon_id"] == id:
                return pokemon["pvp_check_id"]

    def get_pokemon(self, id):
         for pokemon in self.pokedex:
            if pokemon["pokemon_id"] == id:
                return pokemon
    
  