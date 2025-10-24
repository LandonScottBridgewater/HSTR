Hawiian Short-Term Rentals

This project is intended to value vacation rentals in Hawaii

---

Key Findings Summary

See revenue and expenses for short term rentals annually per island at HSTR/data/Macro/model/data.json

Annually, The mean average Hawaiian Short Term Rental had a revenue of 64 thousand and with an estimated 26 thousand expense. (Not factoring the cost of buying the residence)

Hawaiian travel volume has a ~.93 correlation to the broader US-International travel market. (See HSTR/data/.../usa_consumer/to_overseas)

USA to international destination travel has a ~.52 correlation with the Air Affordability Index (I created this index). This means that as travel becomes more expensive in preportion with disposable income, travel has increased at a correlation of ~.52. This is contrary to my prediction that as it would become less affordable to travel, travel would decrease. (See HSTR/data/.../usa_consumer/cpi)

---

Notes

Visitor nights in short term rentals in Hawaii
Oahu: ~17.7%
Maui: 38.9%
Kauai: 39.2%
Hawaii Island: 43.7% 

STRs generated $6.1 billion in 2023, supporting ~66,000 jobs. They also impact housing: about 5% of Hawai‘i’s total housing stock is tied up as STRs—30,000 out of 565,000 units.

STRs as housing stock: ~5% statewide
Visitor spending via STRs: $6.1 B in 2023
Visitor nights in STRs: 29.6%

Interest Rate calculation:

1. Your cost of funds (CoF)
CoF: The interest rate you pay to get the capital (e.g., 5%)

2. Borrower risk (Risk Premium)
Probability of Default (PD): The chance the borrower will default (e.g., 2%)

3. Operating costs (Admin costs)
Loss Given Default (LGD): Percentage of the loan you lose if default happens (e.g., 60%)

4. Desired profit margin (optional)
Profit Margin (PM): Desired return above costs (e.g., 2%)

5. Market/benchmark rates (for sanity check)

Calculate Expected Loss (EL) due to default
EL=PD*LGD

Calculate Minimum Interest Rate (r) to break even
r=CoF+EL+AC+PM

Example:

CoF = 5% (0.05)
PD = 2% (0.02)
LGD = 60% (0.60)
AC = 1% (0.01)
PM = 2% (0.02)
EL = 1.2% (0.012) 

r=0.05+0.012+0.01+0.02= 0.092 / 9.2%

---
