import json
from datetime import datetime
import geopandas as gpd
from shapely.geometry import Point
from utils.paths import get_project
import copy
from pathlib import Path

project = get_project("HSTR")
parent = Path(__file__).resolve().parent.name

class Transaction:
    def __init__(self, price=0, unix=0):
        self.price = price
        self.unix = unix
        self.date = datetime.fromtimestamp(unix) if unix > 0 else None

    def to_json(self):
        return {
            'price': self.price,
            'unix': self.unix,
            'date': self.date.isoformat() if self.date else None
        }

    def __repr__(self):
        return f"Transaction(price={self.price}, date={self.date})"
    
class Property:
    def __init__(self, coordinates=(0, 0), **kwargs):
        self.coordinates = coordinates
        self.longitude, self.latitude = coordinates
        self.transactions = []
        self.occupancy = 0
        self.revenue = {
            "annual": {
                "Gross": 0,
                "Net": 0
            }
        }
        self.price = 0
        self.island = "Statewide"
        base_structure = {
            'operating': {
                'Platforms': 0, 
                'Maintenance': 0,
                'Utilities': 0,
                'Insurance': 0
            },
            'capital': {
                'Furniture': 0
            },
            'taxes': {
                'Property': 0,
                'Income': 0
            },
            'Total': 0
        }

        self.expenses = {
            'annual': copy.deepcopy(base_structure)
        }
        self.profit = 0

        self.expenses["annual"]["capital"]["Furniture"] = 720
        self.expenses["annual"]["operating"]["Insurance"] = 2500

        try:
            island_shp = f'{project}/data/land/Island_boundaries.shp'
            gdf = gpd.read_file(island_shp)
            if gdf.crs and gdf.crs.to_string() != "EPSG:4326":
                gdf = gdf.to_crs(epsg=4326)
            point = Point(self.longitude, self.latitude)
            match = gdf[gdf.contains(point)]
            if not match.empty:
                self.island = match.iloc[0]['Island']
        except Exception as e:
            print(f"Island lookup failed: {e}")

        try:
            year = str(datetime.now().year)
            with open(f'{project}/data/utilities/data.json') as f:
                data = json.load(f)
            self.expenses["annual"]['operating']["Utilities"] = data["Monthly"]["Total"][self.island]["2025"] * 12
        except Exception as e:
            print(f"Failed to load utility cost: {e}")

        try:
            with open(f'{project}/data/revenue/data.json', 'r') as f:
                r = json.load(f)
            if r["Annual"][self.island]["2025p"]:
                self.revenue["annual"]["Gross"] = r["Annual"][self.island]["2025p"]
        except Exception as e:
            print(f"Failed to load revenue: {e}")

        try:
            with open(f'{project}/data/house_price_median/data.json', 'r') as f:
                r = json.load(f)
            if r[self.island]["2025"]:
                self.price = r[self.island]["2025"]
                self.expenses["annual"]["operating"]["Maintenance"] = 0.02 * self.price
        except Exception as e:
            print(f"Failed to load median house prices: {e}")

        try:
            total_market = 0
            weighted_sum = 0

            with open(f"{project}/data/platform_fees/data.json", "r") as f:
                r = json.load(f)

            for platform, p_data in r.items():
                market = p_data["MKT"]
                rate = p_data["Rate"]
                total_market += market
                weighted_sum += market * rate

            avg_rate = weighted_sum / total_market
            self.expenses["annual"]["operating"]["Platforms"] = round(self.revenue["annual"]["Gross"] * avg_rate,2)
        except Exception as e:
            print(f"Failed to load platform fees: {e}")

        try:
            with open(f'{project}/data/supply_demand/data.json', "r") as f:
                r = json.load(f)
            ratio = r["Raw"]["YTD"]["December"]["In Thousands"]["Demand"][self.island][year] / r["Raw"]["YTD"]["December"]["In Thousands"]["Supply"][self.island][year]
            self.occupancy = min(1.0, ratio)
        except Exception as e:
            print(f"Failed to load supply and demand: {e}")

        try:
            with open(f'{project}/data/house_price_median/data.json','r') as f:
                r = json.load(f)
            self.price = r[self.island]["2025"]
        except Exception as e:
            print(f"Failed to load median house price: {e}")

        try:
            with open(f"{project}/data/taxes/data.json","r") as f:
                r = json.load(f)
            self.expenses["annual"]["taxes"]["Property"] = round(r["Property"][self.island]["2025"] * self.price, 2)
        except Exception as e:
            print(f"Failed to load taxes: {e}")

        for i in self.expenses["annual"].values():
            if isinstance(i,dict):
                for ii in i.values():
                    self.expenses["annual"]["Total"] += ii

        self.profit = self.revenue["annual"]["Gross"] - self.expenses["annual"]["Total"]

    def to_json(self):
        data = {
            "Revenue":self.revenue,
            "Expenses":self.expenses,
            "Profit":self.profit,
            "Home Value":self.price,
            "Transactions":[t.to_json() for t in self.transactions],
            "Coordinates":self.coordinates,
            "Occupancy":self.occupancy,
            "Island":self.island
        }
        return data

    def __repr__(self):
        try:
            island_shp = f"{project}/data/land/Island_boundaries.shp"
            gdf = gpd.read_file(island_shp)
            matches = gdf[gdf.geometry.contains(Point(self.longitude, self.latitude))]
            island_name = matches['Island'].values[-1] if not matches.empty else "Unknown Island"
        except Exception:
            island_name = "Unknown Island"

        if self.transactions:
            last_transaction = self.transactions[-1]
            return f"On {island_name} and last sold at {last_transaction.price} on {last_transaction.date}"
        else:
            return f"On {island_name} with no transaction history"
        
p = Property()

with open(f"{parent}/data_m.json","w") as f:
    json.dump(p.to_json(), f, indent=4)