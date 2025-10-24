import pandas as pd
import statsmodels.api as sm

# Load your data, example:
data = {
    'Year': list(range(2010, 2020)),
    'Domestic': [60.37,58.7,60.7,61.34,68.12,74.19,80.23,87.55,92.59,99.74],
    'International': [1963.7,1997.5,2030.3,2059.6,2131.3,2178.7,2206.6,2240.8,2278,2317],
}
df = pd.DataFrame(data)

# Create the time index
df['t'] = df['Year'] - df['Year'].min()

# Define independent variables and add a constant term (intercept)
X = df[['International', 't']]
X = sm.add_constant(X)

# Define dependent variable
y = df['Domestic']

# Fit the regression
model = sm.OLS(y, X).fit()

print(model.summary())
