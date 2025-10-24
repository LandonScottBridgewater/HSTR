data = {
    "hotel": {},
    "str": {},
    "migrants": {}
}

from collections import OrderedDict
import json

hotel_path = "/home/amnesia/Documents/Projects/Active/HSTR/data/supply_demand/hotel/data.json"
str_path = "/home/amnesia/Documents/Projects/Active/HSTR/data/supply_demand/str/data.json"

with open(hotel_path, 'r') as f:
    data["hotel"] = json.load(f, object_pairs_hook=OrderedDict)

with open(str_path, 'r') as f:
    data["str"] = json.load(f, object_pairs_hook=OrderedDict)
     
def merge_sum_common(d1, d2):
    if isinstance(d1, dict) and isinstance(d2, dict):
        common_keys = d1.keys() & d2.keys()
        if not common_keys:
            return None

        merged = {}
        for key in common_keys:
            v1, v2 = d1[key], d2[key]
            if isinstance(v1, dict) and isinstance(v2, dict):
                merged_val = merge_sum_common(v1, v2)
                if merged_val is not None:
                    merged[key] = merged_val
            elif isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                merged[key] = round(v1 + v2, 2)
        return merged if merged else None

    elif isinstance(d1, (int, float)) and isinstance(d2, (int, float)):
        return round(d1 + d2, 2)
    else:
        return None

def merge_mean_common(d1, d2):
    if isinstance(d1, dict) and isinstance(d2, dict):
        common_keys = d1.keys() & d2.keys()  # only shared keys
        if not common_keys:
            return None  # no common keys to merge

        merged = {}
        for key in common_keys:
            v1, v2 = d1[key], d2[key]
            if isinstance(v1, dict) and isinstance(v2, dict):
                merged_val = merge_mean_common(v1, v2)
                if merged_val is not None:
                    merged[key] = merged_val
            elif isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                merged[key] = round((v1 + v2) / 2, 2)
        return merged if merged else None

    elif isinstance(d1, (int, float)) and isinstance(d2, (int, float)):
        return round((d1 + d2) / 2, 2)
    else:
        return None


    
for i in data["str"].keys():
    if i not in data["migrants"]:
        data["migrants"][i] = {}
    for month in data["str"][i].keys():
        if month not in data["migrants"][i]:
            data["migrants"][i][month] = {}
        data["migrants"][i][month]["In Thousands"] = merge_sum_common(data["str"][i][month]["In Thousands"], data["hotel"][i][month]["In Thousands"])
        data["migrants"][i][month]["Occupancy"] = merge_mean_common(data["str"][i][month]["Occupancy"], data["hotel"][i][month]["Occupancy"])
        data["migrants"][i][month]["$"] = merge_mean_common(data["str"][i][month]["$"], data["hotel"][i][month]["$"])



with open("/home/amnesia/Documents/Projects/Active/HSTR/data/supply_demand/total_travellers/data_m.json","w") as f:
    json.dump(data["migrants"],f,indent=4, sort_keys=True)