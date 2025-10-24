d2 = {
    "2024":0,
    "2025":0
}


d1 = {
    "Statewide":d2,
    "Oahu":d2,
    "Maui":{
        "Total":d2,
        "Wailea/Kihei":d2,
        "Lahaina/Kanapali":d2,
    },
    "Hawaii Island":{
        "Kona":d2,
        "Hilo/Honokaa":d2
    },
    "Kauai":d2
}
import json
with open('data1.json','w') as f:
    json.dump(d1,f,indent=4)