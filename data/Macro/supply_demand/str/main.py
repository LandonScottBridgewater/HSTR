import json

data = {
    "Hotel": {},
    "STR": {}
}

with open("/home/amnesia/Documents/Projects/Active/HSTR/data/Hawaii/supply_demand/hotel/data.json","r") as f:
    data["Hotel"] = json.load(f)

with open("/home/amnesia/Documents/Projects/Active/HSTR/data/Hawaii/supply_demand/str/data.json","r") as f:
    data["STR"] = json.load(f)