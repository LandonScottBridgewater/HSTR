import json
from utils.paths import get_project
from pathlib import Path

project = get_project("HSTR")
parent = Path(__file__).resolve().parent

islands = ["Statewide", "Oahu", "Maui", "Hawaii Island", "Kauai"]

data = {}


def create_per_day():
    with open(project / 'data' / 'Macro' / 'supply_demand' / 'str' / 'data.json', 'r') as f:
        supply_demand = json.load(f)
    
    data["Daily"] = {}
    occupancy = supply_demand["Raw"]["YTD"]["December"]["Occupancy"]
    daily_rate = supply_demand["Raw"]["YTD"]["December"]["$"]["Daily Rate"]

    for island in islands:
        island_occ = occupancy.get(island, {})
        island_rate = daily_rate.get(island, {})

        # Check if nested (subregions)
        nested = any(isinstance(v, dict) for v in island_occ.values())

        if nested:
            data["Daily"][island] = {}
            for subregion, subregion_data in island_occ.items():
                data["Daily"][island][subregion] = {}
                for year in range(2019, 2025):
                    year_str = str(year)
                    occ = subregion_data.get(year_str, 0)/100
                    rate = island_rate.get(subregion, {}).get(year_str, 0)
                    data["Daily"][island][subregion][year_str] = round(occ * rate, 2)
        else:
            data["Daily"][island] = {}
            for year in range(2019, 2025):
                year_str = str(year)
                occ = island_occ.get(year_str, 0)/100
                rate = island_rate.get(year_str, 0)
                data["Daily"][island][year_str] = round(occ * rate, 2)

def create_yearly():

    data['Annual'] = {}

    for k, v in data['Daily'].items():
        data['Annual'][k] = {}
        for kk, vv in v.items():
            if not isinstance(vv, dict):
                data['Annual'][k][kk] = round(365 * vv, 2)
            else:
                data['Annual'][k][kk] = {}
                for kkk, vvv in vv.items():
                    data['Annual'][k][kk][kkk] = round(365 * vvv, 2)

    with open(parent / 'data_m.json','w') as f:
        json.dump(data,f,indent=4)

if __name__ == '__main__':
    create_per_day()
    create_yearly()