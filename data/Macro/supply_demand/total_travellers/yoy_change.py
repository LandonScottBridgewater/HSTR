import json

def hasyears(d):
    """Check if all keys are years between 1900 and 2100."""
    try:
        return all(1900 < int(k) < 2100 for k in d.keys())
    except ValueError:
        return False

def function(d, parent_d, path):
    for key in list(d.keys()):
        if isinstance(d[key], dict):
            if hasyears(d[key]):
                years = sorted(int(y) for y in d[key].keys())
                first_year = years[0]
                last_year = years[-1]

                d["YOY % Change"] = {}
                for year in years[1:]:
                    prev_year = str(year - 1)
                    if prev_year in d[key] and d[key][prev_year] != 0:
                        d["YOY % Change"][str(year)] = round(
                            100 * ((d[key][str(year)] - d[key][prev_year]) / d[key][prev_year]),
                            1
                        )


            else:
                # ✅ Pass the path so recursion works
                function(d[key], d, path)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# Usage example
path = "/home/amnesia/Documents/Projects/Active/HSTR/data/Hawaii/supply_demand/total_travellers/data.json"
with open(path, 'r') as f:
    data = json.load(f)

path2 = "/home/amnesia/Documents/Projects/Active/HSTR/data/Hawaii/supply_demand/total_travellers/data_m.json"

function(data, data, path2)
