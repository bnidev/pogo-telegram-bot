import telegram
import json
from datetime import datetime
import requests
import time

class Telegram(object):
    def __init__(self, pokedex, config):
        self.token = config["telegram"]["token"]
        self.userId = config["telegram"]["userId"] 
        self.rareChannelId = config["telegram"]["rareChannelId"]
        self.greatChannelId = config["telegram"]["greatChannelId"]
        self.ultraChannelId = config["telegram"]["ultraChannelId"]
        self.bot = telegram.Bot(token=self.token)
        self.pokedex = pokedex
        self.retry_errors = [500, 502, 504]     

    def send(self, msg, id = None):
        if id is None:
            id = self.userId        
        self.bot.sendMessage(chat_id=id, text=msg, parse_mode=telegram.ParseMode.HTML)

    def load_notified(self):
        with open("notified.json") as notified_file:
            notified = json.load(notified_file)
            now = datetime.now().timestamp()
            for notification in notified:
                if now > notification["despawn"]:
                    notified.remove(notification)
            return notified

    def save_notified(self, data):
        json_object = json.dumps(data, indent = 4)
        with open("notified.json", "w") as file:
            file.write(json_object)


    def get_location(self, lat, lon):        
        retries = 0        
        while retries <= 5:
            res = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}")

            if res.status_code == 200:
                print("got data from adress lookup")
                return res.json()
            else:
                time.sleep(1)
                retries += 1
                print(f"not successful, trying again ({retries})")           
        
        print("no success, more than 5 trys")
        self.send("Failed to get adress data")
        return False

    def send_notification(self, scantype, pokemon, nearby):
        name = self.pokedex.get_pokemon_name(pokemon["pokemon_id"])
        IVperc = None
        if pokemon["level"] is not None:            
            IVperc = ((pokemon["atk_iv"] + pokemon["def_iv"] + pokemon["sta_iv"]) / 45) * 100

        # convert despawn time and calculate time remaining
        despawn = datetime.fromtimestamp(pokemon["expire_timestamp"])
        despawn_formatted = despawn.strftime("%H:%M:%S")
        now = datetime.now().timestamp()
        timer = datetime.fromtimestamp(pokemon["expire_timestamp"] - now)
        timer_formatted = timer.strftime("%Mm %Ss")        
        
        # check for location
        location_address = "Unbekannt"
        location_postcode = ""
        location = self.get_location(pokemon["lat"], pokemon["lon"])

        if location:            
            adress = location["address"]
            postcode = adress.get("postcode")            
            road = adress.get("road")            
            number = adress.get("house_number")
            suburb = adress.get("suburb")
            city = adress.get("city")

            if postcode:
                location_postcode = f"- {postcode}"
                if road:       
                    location_address = f"{road} ({postcode})"
                    if number:
                        location_address = f"{road} {number} ({postcode})"
                elif suburb:
                    location_address = f"{suburb} ({postcode})"       
                elif city:
                     location_address = f"{city} ({postcode})"   
        
        
        # emotes 
        emote_hundo = "\U0001F4AF"
        emote_male = "\u2642"
        emote_female = "\u2640"
        emote_neutral = "\u26B2"
        emote_stardust = "\u2728"
        emote_candy = "\U0001F36C"
        emote_rare = "\u2B50"

        symbol = None
        if scantype == "hundo":
            symbol = emote_hundo            
        elif scantype == "rare":            
            symbol = emote_rare
        elif scantype == "candy":
            symbol = emote_candy        
        else:
            symbol = ""

        if IVperc and scantype == "hundo":
            IVperc = int(IVperc)
        elif IVperc:
            IVperc = "{:.2f}".format(IVperc)
        
        #gender 1=male, 2=female, 3=neutral
        gender = None
        if pokemon["gender"] == 1:
            gender = emote_male
        elif pokemon["gender"] == 2:
            gender = emote_female
        elif pokemon["gender"] == 3:
            gender = emote_neutral
        else:
            gender = ""

        
        nearby_objects = None
        if nearby:
            # print(nearby)
            nearby_objects = ", ".join(nearby)


        msg = ""
        if pokemon["level"] is not None:  
            msg += f"{symbol} <b>{name}</b> {gender} {IVperc}% ({pokemon['atk_iv']}|{pokemon['def_iv']}|{pokemon['sta_iv']}) {location_postcode}\n"
        else:
            msg += f"{symbol} <b>{name}</b> {gender} {location_postcode}\n"
        msg += f"Despawn: {despawn_formatted} ({timer_formatted})\n"
        if pokemon["level"] is not None:  
            msg += f"WP: {pokemon['cp']} (Lvl. {pokemon['level']})\n"
        msg += f"Ort: <a href='https://maps.google.com/?q={pokemon['lat']},{pokemon['lon']}'>{location_address}</a>\n"
        if(nearby_objects):
            msg+= f"In der Nähe: {nearby_objects}"

        if scantype == "candy":
            self.send(msg, self.rareChannelId)
        else:
            self.send(msg)

        
    def send_pvp_notification(self, league, base_pokemon, pvp_pokemon, nearby):
        print(league, base_pokemon["pokemon_id"], pvp_pokemon["pokemon_id"])

        base_name = self.pokedex.get_pokemon_name(base_pokemon["pokemon_id"])
        pvp_name = self.pokedex.get_pokemon_name(pvp_pokemon["pokemon_id"])
     
        # convert despawn time and calculate time remaining
        despawn = datetime.fromtimestamp(base_pokemon["expire_timestamp"])
        despawn_formatted = despawn.strftime("%H:%M:%S")
        now = datetime.now().timestamp()
        timer = datetime.fromtimestamp(base_pokemon["expire_timestamp"] - now)
        timer_formatted = timer.strftime("%Mm %Ss")        
        
        # check for location
        location_address = "Unbekannt"
        location_postcode = ""
        location = self.get_location(base_pokemon["lat"], base_pokemon["lon"])

        if location:            
            adress = location["address"]
            postcode = adress.get("postcode")            
            road = adress.get("road")            
            number = adress.get("house_number")
            suburb = adress.get("suburb")
            city = adress.get("city")

            if postcode:
                location_postcode = f"- {postcode}"
                if road:       
                    location_address = f"{road} ({postcode})"
                    if number:
                        location_address = f"{road} {number} ({postcode})"
                elif suburb:
                    location_address = f"{suburb} ({postcode})"       
                elif city:
                     location_address = f"{city} ({postcode})"   
        
        
        # emotes       
        emote_male = "\u2642"
        emote_female = "\u2640"
        emote_neutral = "\u26B2"
        emote_stardust = "\u2728"
        emote_candy = "\U0001F36C"  
       
        # symbol
        symbol = "\u2694"
        
        
        #gender 1=male, 2=female, 3=neutral
        gender = None
        if base_pokemon["gender"] == 1:
            gender = emote_male
        elif base_pokemon["gender"] == 2:
            gender = emote_female
        elif base_pokemon["gender"] == 3:
            gender = emote_neutral
        else:
            gender = ""

        
        nearby_objects = None
        if nearby:
            # print(nearby)
            nearby_objects = ", ".join(nearby)


        msg = f"{symbol} <b>{pvp_name} (#1) {location_postcode}</b>\n"
        msg += f"Despawn: {despawn_formatted} ({timer_formatted})\n\n"
        msg += f"{base_name} {gender} (#{base_pokemon['pokemon_id']})\n"
        msg += f"IVs: {base_pokemon['atk_iv']}|{base_pokemon['def_iv']}|{base_pokemon['sta_iv']}\n"
        msg += f"WP: {base_pokemon['cp']} (Lvl. {base_pokemon['level']})\n\n"
        msg += f"Ort: <a href='https://maps.google.com/?q={base_pokemon['lat']},{base_pokemon['lon']}'>{location_address}</a>\n"
        if(nearby_objects):
            msg+= f"In der Nähe: {nearby_objects}"

        self.send(msg, self.greatChannelId)