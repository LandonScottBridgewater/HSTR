data = {
"Per Month":{
    "Electricity":{
        "Statewide":{
            "2024":{
                "R": 44.07,
                "G": 45.72,
                "J": 38.63,
                "P": 35.96,
                "DS": 31.02,
                "F":  40.79
            }
        },
        "Oahu": {
            "2024":{
                "R": 42.87,
                "G": 42.68,
                "J": 36.02,
                "P": 33.75,
                "DS": 31.57,
                "F": 40.41
            }
        },
        "Maui": {
            "Total":{
                "2024":{
                    "R": 43.59,
                    "G": 48.05,
                    "J": 41.16,
                    "P": 38.13,
                    "F": 39.85
                }
            },
            "Molokai":{
                "2024":{
                    "R": 50.60,
                    "G": 50.14,
                    "J": 39.54,
                    "P": 47.06,
                    "F": 47.06
                }
            },
            "Lanai":{
                "2024":{
                    "R": 50.39,
                    "G": 54.46,
                    "J": 52.19,
                    "P": 48.48,
                    "F": 48.98
                }
            }
        },
        "Hawaii Island": {
            "2024":{
                "R": 48.31,
                "G": 52.79,
                "J": 43.83,
                "P": 39.73,
                "F": 45.50
            }
        }
    },
    "Water & Sewer":{
        "Oahu":{
                "2021":53.83
            }
    },
    "Internet":{
        "Statewide":{
            "2025":29.17
        }
    },
    "Gas":{
        "Statewide": {
          "2025": 102.11
        },
        "Oahu":{
            "2025":102.11
        },
        "Maui":{
            "2025":102.11
        },
        "Hawaii Island":{
            "2025":102.11
        },
        "Kauai":{
            "2025":102.11
        }
    },
    "Trash Collection":{
        "Statewide":{
            "2025":19.96
        },
        "Lanai":{
            "2025":17.50
        },
        "Maui":{
            "2025":35.01
        },
        "Molokai":{
            "2025":35.01
        },
        "Oahu":{
            "2025":0
        },
        "Kauai":{
            "2025":15.56
        },
        "Hawaii Island":{
            "2025":43.76
        }
    }
}
}

def calculate(location="Oahu", year="2025", electricity_plan_avg=True):
    total = 0.0

    # --- Electricity ---
    elec_data = data["Per Month"]["Electricity"]
    elec_costs = []

    if location in elec_data and year in elec_data[location]:
        elec_costs = list(elec_data[location][year].values())
    elif location in elec_data:
        # Check nested (like Maui -> Lanai)
        for sub in elec_data[location]:
            if isinstance(elec_data[location][sub], dict) and year in elec_data[location][sub]:
                elec_costs += list(elec_data[location][sub][year].values())
    elif "Statewide" in elec_data and year in elec_data["Statewide"]:
        elec_costs = list(elec_data["Statewide"][year].values())
    
    if electricity_plan_avg and elec_costs:
        total += sum(elec_costs) / len(elec_costs)

    # --- Water & Sewer ---
    water_data = data["Per Month"]["Water & Sewer"]
    if location in water_data and year in water_data[location]:
        total += water_data[location][year]

    # --- Internet ---
    internet_data = data["Per Month"]["Internet"]
    if "Statewide" in internet_data and year in internet_data["Statewide"]:
        total += internet_data["Statewide"][year]

    # --- Gas ---
    gas_data = data["Per Month"]["Gas"]
    if location in gas_data and year in gas_data[location]:
        total += gas_data[location][year]
    elif "Statewide" in gas_data and year in gas_data["Statewide"]:
        total += gas_data["Statewide"][year]

    # --- Trash Collection ---
    trash_data = data["Per Month"]["Trash Collection"]
    if location in trash_data and year in trash_data[location]:
        total += trash_data[location][year]
    elif "Statewide" in trash_data and year in trash_data["Statewide"]:
        total += trash_data["Statewide"][year]

    return round(total, 2)

for island in ['Oahu','Maui','Molokai','Lanai','Hawaii Island']:
    print(f"Total cost for {island}: {calculate(island)}")