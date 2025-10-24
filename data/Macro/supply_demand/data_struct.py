import json

month = {
    "In Thousands": {
        "Supply": {},
        "Demand": {}
    },
    "Occupancy": {},
    "$": {
    "Daily Rate": {}
    }
}

str_1 = {
    "Statewide": {},
    "Oahu": {
        "Total": {},
        "Waikiki": {},
        "North Shore": {},
        "Other Honolulu": {},
        "Leeward/Makaha Side": {},
        "Windward Side": {},
        "Ala Moana Area": {},
        "Airport Area": {},
    },
    "Maui": {
        "Total": {},
        "Wailea/Kihei": {},
        "Lahaina/Kaanapali/Napili/Kapalua": {},
        "Maalaea": {},
        "Kula/Makawao Area": {},
        "Hana Area": {},
        "Island of Maui": {},
        "Molokai": {},
        "Lanai": {},
    },
    "Hawaii Island": {
        "Total": {},
        "Kona": {},
        "Kohala/Waimea/Kawaihae": {},
        "Hilo/Honokaa": {},
        "Volcnao Area": {},
        "Naalehu/Kau": {}
    },
    "Kauai": {
        "Total": {},
        "Princeville/Hanalei": {},
        "Poipu/Kukuiula": {},
        "Lihue": {},
        "Kalaheo/Waimea": {},
    }
}

hotel_1 = {}

str_2 = {
    "In Thousands": {
        "Supply": str_1,
        "Demand": str_1
    },
    "Occupancy": str_1,
    "$": {
    "Daily Rate": str_1
    }
}

hotel_2 = {
    "In Thousands": {
        "Supply": hotel_1,
        "Demand": hotel_1
    },
    "Occupancy": hotel_1,
    "$": {
    "Daily Rate": hotel_1
    }   
}



data = {
    "Raw Data": {
        "Monthly": {
            "January": {},
            "April": {},
        },
        "YTD": {
            "December": {}
        }
    },
    "Estimated Data": {}
}