#!/usr/bin/env python3

import requests
import time
import json
from pokemonfilter import PokemonFilter
from candymap import CandyMap
from telegramlib import Telegram
from pokedexlib import Pokedex

def load_config():
    with open("config.json") as config_file:
        config = json.load(config_file)
        return config
        
config = load_config()


pokedex = Pokedex()
pkmfilter = PokemonFilter(config)
telegram = Telegram(pokedex, config)
candymap = CandyMap(telegram, config)



def run():
    try:
        while True:
            notified = telegram.load_notified()
            pokemon_data = candymap.get_data("pokemon")
            if pokemon_data:
                for pokemon in pokemon_data:
                    dis = pkmfilter.calc_distance(pokemon["lat"], pokemon["lon"], config["pokemon_filter"]["centerLat"], config["pokemon_filter"]["centerLon"])
                    if dis < pkmfilter.filter_radius:
                        # check for hundo
                        if pokemon["level"] is not None:                     
                            if pkmfilter.check_for_hundo(pokemon):                            
                                vorhanden = False
                                for notification in notified:                   
                                    if pokemon["id"] == notification["id"]:
                                        vorhanden =  True     
                                if vorhanden != True:
                                    nearby = pkmfilter.get_metros_and_pois(pokemon["lat"], pokemon["lon"])                              
                                    telegram.send_notification("hundo", pokemon, nearby)                                
                                    notified.append({"id": pokemon["id"], "despawn": pokemon["expire_timestamp"]})
                                    time.sleep(2)
                                else:
                                    print("[hundo] already notified!")

                        # check for rare
                        if pkmfilter.check_for_rare(pokemon):
                            vorhanden = False
                            for notification in notified:                   
                                if pokemon["id"] == notification["id"]:
                                    vorhanden =  True                               
                            if vorhanden != True:
                                nearby = pkmfilter.get_metros_and_pois(pokemon["lat"], pokemon["lon"])                              
                                telegram.send_notification("rare", pokemon, nearby)                                
                                notified.append({"id": pokemon["id"], "despawn": pokemon["expire_timestamp"]})
                                time.sleep(2)
                            else:
                                print("[rare] already notified!")

                        # check for candy
                        if pkmfilter.check_for_candy(pokemon):
                            vorhanden = False
                            for notification in notified:                   
                                if pokemon["id"] == notification["id"]:
                                    vorhanden =  True
                            if vorhanden != True:
                                nearby = pkmfilter.get_metros_and_pois(pokemon["lat"], pokemon["lon"])                              
                                telegram.send_notification("candy", pokemon, nearby)                                
                                notified.append({"id": pokemon["id"], "despawn": pokemon["expire_timestamp"]})
                                time.sleep(1)
                            else:
                                print("[candy] already notified!")
                        
                        # get pvp check ids for pokemon
                        pvp_check_ids = pokedex.get_pvp_check_ids(pokemon["pokemon_id"])           
                                    
                        # check for great league                        
                        for id in pvp_check_ids:
                            dex_pokemon = pokedex.get_pokemon(pokemon["pokemon_id"])
                            if dex_pokemon["great_league_filter"] > 0:
                                if pkmfilter.check_for_great_league(pokemon, dex_pokemon):
                                    vorhanden = False
                                    for notification in notified:                   
                                        if pokemon["id"] == notification["id"]:
                                            vorhanden =  True                               
                                    if vorhanden != True:
                                        nearby = pkmfilter.get_metros_and_pois(pokemon["lat"], pokemon["lon"])                              
                                        telegram.send_pvp_notification("great", pokemon, dex_pokemon, nearby)                                
                                        notified.append({"id": pokemon["id"], "despawn": pokemon["expire_timestamp"]})
                                        time.sleep(2)
                                    else:
                                        print("[GL] already notified!")

                        


                            
            
            telegram.save_notified(notified)
            time.sleep(30) 
    except KeyboardInterrupt:
        print("Exit on keyboard interupt ...")
        exit(0)


if __name__ == "__main__":
    telegram.send("CMBot started.")
    run()