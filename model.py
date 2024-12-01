import pandas as pd
import numpy as np
from scipy.stats import poisson
from tqdm import tqdm
import matplotlib.pyplot as plt


zip_codes = 'data/sdge_zip.xlsx'
df_zip = pd.read_excel(zip_codes, dtype=str)
# print(df_zip)

years = [2018, 2019, 2020, 2021, 2022, 2023]
dfs = []

for y in years:
    file = f'data/vehicle-fuel-type-count-by-zip-code-{y}.csv'
    df_year = pd.read_csv(file, dtype={'Zip Code': str, 'Model Year': str})
    df_year.columns = [c.replace(" ", "_").lower() for c in df_year.columns]
    df_year = df_year[df_year.zip_code.astype(str).isin(df_zip['ZIP_CODE'])]
    df_year = df_year[df_year.fuel == 'Battery Electric']
    dfs.append(df_year)

df = pd.concat(dfs, ignore_index=True)

df = df.groupby(['date', 'zip_code']).vehicles.sum().reset_index()

df = df.pivot(index='zip_code', columns='date', values='vehicles').fillna(0).reset_index()

df = df.melt(id_vars=['zip_code'], var_name='date', value_name='counts')
print(df)

# Plot a histogram of counts
df['counts'].hist(bins=200)
plt.show()

# Fit a Poisson distribution for each ZIP code
poisson_params = {}
for zip_code in df['zip_code'].unique():
    counts = df[df['zip_code'] == zip_code]['counts']
    lambda_param = np.mean(counts)
    poisson_params[zip_code] = lambda_param

# Monte Carlo simulation to sample from the Poisson distribution
samples_results = {}
n_samples = 1000
for n in tqdm(range(n_samples)):
    results = []
    for zip_code in poisson_params.keys():
        value = poisson.rvs(mu=poisson_params[zip_code], size=1)
        results.append(value[0])
    samples_results[n] = results

# Convert results to a DataFrame
df_results = pd.DataFrame(samples_results, index=poisson_params.keys())
print(df_results.head())

df_results.sum(axis=0).hist(bins=25)
plt.show()
