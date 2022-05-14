import geopy.distance
import json

class PokemonFilter(object):
    def __init__(self, config):
        self.filter_radius = config["pokemon_filter"]["filterRadius"]
        self.poi_list = self.load_poi_list()
        self.metro_list = self.load_metro_list()
        self.rare_list = config["pokemon_filter"]["rareList"]
        self.candy_list = config["pokemon_filter"]["candyList"]

    def load_poi_list(self):        
        with open("data/poi_list.json") as poi_file:
            poi_list = json.load(poi_file)
            return poi_list

    def load_metro_list(self):        
        with open("data/metro_list.json") as metro_file:
            metro_list = json.load(metro_file)
            return metro_list

    def calc_distance(self, lat1, lon1, lat2, lon2):        
        coords_pkm = (lat1, lon1)
        coords_poi = (lat2, lon2)
        return geopy.distance.geodesic(coords_pkm, coords_poi).km


    def check_for_hundo(self, pokemon):
        if pokemon["atk_iv"] == pokemon["def_iv"]  == pokemon["sta_iv"] == 15:
            print(f"Hundo: {pokemon['pokemon_id']} - {pokemon['lat']}, {pokemon['lon']}")
            return True

    def check_for_rare(self, pokemon):
        if pokemon['pokemon_id'] in self.rare_list:
            print(f"Rare: {pokemon['pokemon_id']} - {pokemon['lat']}, {pokemon['lon']}")
            return True

    def check_for_candy(self, pokemon):
        if pokemon['pokemon_id'] in self.candy_list:
            print(f"Candy: {pokemon['pokemon_id']} - {pokemon['lat']}, {pokemon['lon']}")
            return True          

    def check_for_great_league(self, pokemon, dex_pokemon):
        if pokemon["atk_iv"] == dex_pokemon["great_league_best"]["atk_iv"] and pokemon["def_iv"] == dex_pokemon["great_league_best"]["def_iv"] and pokemon["sta_iv"] == dex_pokemon["great_league_best"]["sta_iv"] and pokemon["level"] <= dex_pokemon["great_league_best"]["lvl"]:
            print(f"Great League R1: {pokemon['pokemon_id']} ({pokemon['atk_iv']}/{pokemon['def_iv']}/{pokemon['sta_iv']}) - {pokemon['lat']}, {pokemon['lon']}")
            return True

    def get_metros_and_pois(self, lat, lon):        
        nearby = []
        for metro in self.metro_list:
            dis = self.calc_distance(lat, lon, metro["lat"], metro["lon"])
            if dis < 0.5:
                icon = None
                name = metro['name']
                if metro["line"] == "S":
                    icon = "\U0001F682"
                else:
                    icon = "\U0001F687"
                nearby.append(f"{icon} {metro['line']} {name} ({round(dis*1000)}m)")
                #nearby.append("test")

        for poi in self.poi_list:
            dis = self.calc_distance(lat, lon, poi["lat"], poi["lon"])
            if dis < 0.5:
                nearby.append(f"\U0001F4CD {poi['name']} ({round(dis*1000)}m)")
        return nearby