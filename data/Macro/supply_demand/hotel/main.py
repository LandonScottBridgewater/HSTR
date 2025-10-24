import json

def calculate_occupancy(supply, demand):
    """
    Calculate occupancy rates as percentage (demand / supply * 100),
    rounded to one decimal place.
    """
    occupancy = {}

    for region in supply:
        occupancy[region] = {}
        if isinstance(supply[region], dict) and all(isinstance(v, dict) for v in supply[region].values()):
            for subregion in supply[region]:
                occupancy[region][subregion] = {}
                for year in supply[region][subregion]:
                    sup_val = supply[region][subregion][year]
                    dem_val = demand[region][subregion][year]
                    if sup_val:
                        occ = (dem_val / sup_val) * 100
                        occupancy[region][subregion][year] = round(occ, 1)
                    else:
                        occupancy[region][subregion][year] = None
        else:
            for year in supply[region]:
                sup_val = supply[region][year]
                dem_val = demand[region][year]
                if sup_val:
                    occ = (dem_val / sup_val) * 100
                    occupancy[region][year] = round(occ, 1)
                else:
                    occupancy[region][year] = None

    return occupancy


path = "/home/amnesia/Documents/Projects/Active/HSTR/data/supply_demand/hotel/data.json"

with open(path, "r") as f:
    file = json.load(f)
    
for k in file.keys():
    for month in file[k]:
        supply = file[k][month]["In Thousands"]["Supply"]
        demand = file[k][month]["In Thousands"]["Demand"]
        # Calculate occupancy and update the dict
        occupancy = calculate_occupancy(supply, demand)
        file[k][month]["Occupancy"] = occupancy

out_path = "/home/amnesia/Documents/Projects/Active/HSTR/data/supply_demand/hotel/data_m.json"

with open(out_path, "w") as f:
    json.dump(file, f, indent=4)

print(f"Updated data saved to {out_path}")
