import requests
import time
import json
from utils.paths import get_project

path = get_project("HSTR") / "data" / "population" / "data_m.json"
path = '/home/amnesia/Documents/Projects/Active/HSTR/data/population/data_m.json'

with open(path, 'r') as f:
    data = json.load(f)

username = 'exhibit'

def get_population(place, county=''):
    params = {
        'q': place,
        'maxRows': 1,
        'username': username,
        'type': 'json',
    }
    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get('http://api.geonames.org/searchJSON', params=params, timeout=10)
            if response.status_code == 200:
                results = response.json().get('geonames', [])
                if results:
                    return int(results[0].get('population', 0))
            return 0
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {place}: {e}")
            time.sleep(2)  
    return 0

for county, places in data.items():
    for place in places:
        print(data[county][place])
        if data[county][place] == 0:
            print(f"Fetching population for {place} in {county}...")
            pop = get_population(place, county)
            if pop == 0:
                data[county][place] = -1
            elif pop == -1:
              pass
            else:
              data[county][place] = pop
              print(pop)
            try:
                with open(path, 'w') as f:
                    json.dump(data, f, indent=4)
                print("File written successfully.")
            except Exception as e:
                print(f"Error writing file: {e}")
            time.sleep(1) 
