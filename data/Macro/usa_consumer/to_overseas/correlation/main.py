import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Sample U.S. tourism data (millions) for years 2010–2020
# Domestic trips (in billions), International outbound trips (in millions)
data = {
    "Year": list(range(2010, 2021)),
    "Domestic_Tourism_Billion_Trips": [1.99, 2.03, 2.06, 2.10, 2.12, 2.14, 2.18, 2.20, 2.25, 2.29, 1.40],  # 2020 is pandemic dip
    "International_Trips_Million": [61.0, 60.8, 61.9, 61.4, 68.3, 73.4, 80.2, 87.7, 93.0, 93.0, 60.5]  # also dip in 2020
}

df = pd.DataFrame(data)

# Convert Domestic trips to millions to match units
df["Domestic_Trips_Million"] = df["Domestic_Tourism_Billion_Trips"] * 1000

# Exclude the 2020 pandemic year
df_no_2020 = df[df["Year"] != 2020]

# Recalculate correlation without 2020
correlation_no_2020, p_value_no_2020 = pearsonr(
    df_no_2020["Domestic_Trips_Million"],
    df_no_2020["International_Trips_Million"]
)

# Plotting without 2020
plt.figure(figsize=(10, 6))
plt.plot(df_no_2020["Year"], df_no_2020["Domestic_Trips_Million"], marker='o', label="Domestic Trips (M)")
plt.plot(df_no_2020["Year"], df_no_2020["International_Trips_Million"], marker='o', label="International Trips (M)")
plt.title("U.S. Domestic vs International Tourism (2010–2019)")
plt.xlabel("Year")
plt.ylabel("Trips (Millions)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

correlation_no_2020, p_value_no_2020
