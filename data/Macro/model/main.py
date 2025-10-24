import json
from utils.paths import get_project
from utils.io import load_json
from pathlib import Path
import copy

project = get_project("HSTR")
parent = Path(__file__).resolve().parent

class Property:
    def __init__(self, year=2020, island="Statewide"):
        self.occupancy = 0
        self.revenue = {
            "Gross Annual Revenue": 0
        }
        self.price = 0
        self.year = str(year)
        self.island = island

        base_structure = {
            'Operating': {
                'Platforms': 0, 
                'Maintenance': 0,
                'Utilities': 0,
                'Insurance': 0
            },
            'Capital': {
                'Furniture': 0
            },
            'Property Taxes': 0,
            'Total': 0
        }
        self.expenses = {'Annual': copy.deepcopy(base_structure)}
        self.profit = 0

        self.expenses["Annual"]["Capital"]["Furniture"] = 720
        self.expenses["Annual"]["Operating"]["Insurance"] = 2500

        # Utility costs
        utility_data = load_json(project / 'data' / 'Macro' / 'utility_bills' / 'data.json')
        self.expenses["Annual"]['Operating']["Utilities"] = utility_data["Monthly"]["Total"]["Statewide"].get(self.year, 0) * 12
        
        # Revenue
        revenue_data = load_json(project / 'data' / 'Macro' / 'revenue' / 'data.json')
        self.revenue["Gross Annual Revenue"] = revenue_data["Annual"].get(self.island, {}).get(self.year, 0)

        # House price and maintenance
        price_data = load_json(project / 'data' / 'Macro' / 'house_price_median' / 'data.json')
        self.price = price_data.get(self.island, {}).get(self.year, 0)

        self.expenses["Annual"]["Operating"]["Maintenance"] = 0.02 * self.price
        # Platform fees
        platform_data = load_json(project / 'data' / 'Macro' / 'platform_fees' / 'data.json')
        total_market = 0
        weighted_sum = 0
        for platform, p_data in platform_data.items():
            market = p_data.get("MKT", 0)
            rate = p_data.get("Rate", 0)
            total_market += market
            weighted_sum += market * rate
        avg_rate = weighted_sum / total_market if total_market else 0
        self.expenses["Annual"]["Operating"]["Platforms"] = round(self.revenue["Gross Annual Revenue"] * avg_rate, 2)

        # Supply & Demand
        supply_demand = load_json(project / 'data' / 'Macro' / 'supply_demand' / 'str' / 'data.json')
        demand = supply_demand["Raw"]["YTD"]["December"]["In Thousands"]["Demand"].get(self.island,{}).get(self.year,-1)
        supply = supply_demand["Raw"]["YTD"]["December"]["In Thousands"]["Supply"].get(self.island,{}).get(self.year,-1)
        self.occupancy = min(1.0, demand / supply)

        # Taxes
        tax_data = load_json(project / 'data' / 'Macro' / 'taxes' / 'data.json')

        print("Island:", self.island)
        print("Available islands:", tax_data["Property"].keys())
        print("Year:", self.year)
        tax_rate = tax_data["Property"].get(self.island, tax_data["Property"].get("Statewide", {})).get(self.year, 0)
        print("Tax rate:", tax_rate)


        print(tax_rate)
        self.expenses["Annual"]["Property Taxes"] = round(tax_rate * self.price, 2)

        # Expenses
        for i in self.expenses["Annual"].values():
            if isinstance(i, dict):
                for ii in i.values():
                    self.expenses["Annual"]["Total"] += ii
        self.expenses["Annual"]["Total"] = round(self.expenses["Annual"]["Total"])

        # Profit
        self.profit = round(self.revenue["Gross Annual Revenue"] - self.expenses["Annual"]["Total"])

    def to_json(self):
        return {
            "Revenue": self.revenue,
            "Expenses": self.expenses,
            "Profit": self.profit,
            "Home Value": self.price,
            "Occupancy": self.occupancy,
            "Island": self.island,
            "Year": self.year
        }


data = {}
islands = ['Statewide', 'Oahu', 'Maui', 'Molokai', 'Lanai', 'Hawaii Island']
for island in islands:
    data[island] = {}
    for year in range(2020, 2025):
        p = Property(year=year, island=island)
        data[island][year] = p.to_json()

with open(parent / "data_m.json", "w") as f:
    json.dump(data, f, indent=4)
