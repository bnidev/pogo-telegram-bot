import requests

class CandyMap(object):
    def __init__(self, telegram, config):
        self.base_url = config["api"]["baseUrl"]
        self.success = None
        self.telegram = telegram

    def get_data(self, datatype):
        print("getting new data now...")
        retries = 0
        while retries <= 5:

            res = requests.get(f"{self.base_url}{datatype}",)        
            if res.status_code == 200 and "Fatal" not in res.text:
                print("got some data...")            
                response = res.json()
                if not response and self.success != False:
                    self.telegram.send("Pokemon list was empty.")
                    self.success = False
                elif response and self.success != True:
                    self.success = True
                    self.telegram.send("Pokemon are available.")
                return res.json()
            else:
                time.sleep(1)
                retries += 1
                print(f"not successful, trying again ({retries})")  
        
        print("no success, more than 5 trys")
        self.send("Failed to get candymap data")
        return False
            