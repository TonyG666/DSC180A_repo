import pandas as pd
import numpy as np
from scipy.stats import poisson
from tqdm import tqdm
import matplotlib.pyplot as plt


# Load ZIP codes data from an Excel file
zip_codes = 'data/sdge_zip.xlsx'
df_zip = pd.read_excel(zip_codes, dtype=str)
# print(df_zip)

# List of years to process
years = [2018, 2019, 2020, 2021, 2022, 2023]

# Initialize an empty list to store dataframes for each year
dfs = []

# Loop through each year to read, filter, and process data
for y in years:
    # Load the yearly CSV file
    file = f'data/vehicle-fuel-type-count-by-zip-code-{y}.csv'
    df_year = pd.read_csv(file, dtype={'Zip Code': str, 'Model Year': str})
    # Standardize column names to lowercase and replace spaces with underscores
    df_year.columns = [c.replace(" ", "_").lower() for c in df_year.columns]
    # Filter for ZIP codes present in the ZIP code file
    df_year = df_year[df_year.zip_code.astype(str).isin(df_zip['ZIP_CODE'])]
    # Filter for Battery Electric vehicles
    df_year = df_year[df_year.fuel == 'Battery Electric']
    # Append the filtered dataframe to the list
    dfs.append(df_year)

# Concatenate all the yearly dataframes into one
df = pd.concat(dfs, ignore_index=True)

# Aggregate vehicle counts by date and ZIP code
df = df.groupby(['date', 'zip_code']).vehicles.sum().reset_index()

# Pivot the data to create a table where rows are ZIP codes, columns are dates, and values are counts
df = df.pivot(index='zip_code', columns='date', values='vehicles').fillna(0).reset_index()

# Transform the data back into a long format for further processing
df = df.melt(id_vars=['zip_code'], var_name='date', value_name='counts')

# Display the transformed data
print(df)

# Plot a histogram of vehicle counts
df['counts'].hist(bins=200)
plt.title("Histogram of Vehicle Counts")
plt.xlabel("Vehicle Count")
plt.ylabel("Frequency")
plt.show()

# Fit a Poisson distribution for each ZIP code
poisson_params = {}
for zip_code in df['zip_code'].unique():
    counts = df[df['zip_code'] == zip_code]['counts']
    # Calculate the mean (lambda) for the Poisson distribution
    lambda_param = np.mean(counts)
    # Store the parameter in a dictionary
    poisson_params[zip_code] = lambda_param

# Perform Monte Carlo simulation to sample from the fitted Poisson distributions
samples_results = {}
n_samples = 1000    # Number of Monte Carlo simulations

# Loop through simulations
for n in tqdm(range(n_samples)):
    results = []
    for zip_code in poisson_params.keys():
        # Sample a random value from the Poisson distribution
        value = poisson.rvs(mu=poisson_params[zip_code], size=1)
        results.append(value[0])
    # Store the results for each simulation
    samples_results[n] = results

# Convert simulation results into a DataFrame
df_results = pd.DataFrame(samples_results, index=poisson_params.keys())

# Display head of the simulation results
print(df_results.head())

# Plot a histogram of the total counts across simulations
df_results.sum(axis=0).hist(bins=25)
plt.title("Histogram of Total Counts from Simulations")
plt.xlabel("Total Count")
plt.ylabel("Frequency")
plt.show()
