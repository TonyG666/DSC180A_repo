import pandas as pd
import numpy as np
import statsmodels.api as sm


# get the dataset
dmv_df = pd.read_csv('data/dmv.csv')
print(dmv_df.head())
print(len(dmv_df))
print(dmv_df.columns)

dmv_df['Date'] = pd.to_datetime(dmv_df['Date'], errors='coerce')

electric_vehicles_2023 = dmv_df[
    (dmv_df['Fuel'].str.contains("Electric", case=False, na=False)) & 
    (dmv_df['Date'].dt.year == 2023)
]

zip_code_electric_totals = electric_vehicles_2023.groupby('ZIP Code')['Vehicles'].sum()
zip_code_electric_totals = zip_code_electric_totals.sort_values(ascending=False)
print(zip_code_electric_totals.head())

electric_counts = zip_code_electric_totals.values

poisson_model = sm.GLM(electric_counts, np.ones_like(electric_counts), family=sm.families.Poisson())
poisson_results = poisson_model.fit()

print(poisson_results.summary())

predicted_values = poisson_results.predict()
print("Predicted counts:", predicted_values)