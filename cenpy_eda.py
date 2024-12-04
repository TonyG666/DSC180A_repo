# San Diego City Population

import cenpy as cp
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import plotly.express as px


# Step 1: Connect to the Census API
# Connect to the ACS 5-Year Estimates for 2022
conn = cp.remote.APIConnection("ACSDT5Y2022")

# Specify variables to pull from the Census data
# - B01001_001E: Total Population
# - NAME: Geographical identifier (not used in the final output)
variables_to_pull = ['B01001_001E', 'NAME']
geo_unit = 'zip code tabulation area:*'

# Query the data from the Census API
data = conn.query(variables_to_pull, geo_unit)

# Clean up the data: Remove the NAME column and rename the remaining columns for clarity
data.drop(columns = ['NAME'], inplace=True)
data.columns = ['Total Population', 'zip']

# Step 2: Load Alternative Fuel Data Center (AFDC) data
# Load the JSON file containing AFDC data
with open('data/afdc_full.json', 'r') as f:
    afdc = json.load(f)
fs = afdc.get('fuel_stations', [])

# Extract fuel stations data from the loaded JSON
afdc_df = pd.DataFrame(fs)

# Filter the AFDC data for San Diego and electric fuel type stations
sd = afdc_df[(afdc_df['city'] == 'San Diego') & (afdc_df['fuel_type_code'] == 'ELEC')]

# Merge the AFDC data with Census data on zip codes
sd_acs = sd.merge(data, how='left',on='zip')

# Extract essential columns for clear plotting
sd_acs_clear = sd_acs[['zip', 'Total Population', 'latitude', 'longitude']]
print(sd_acs_clear.head())


# Step 3: Load GeoJSON for zip code boundaries
# Load the GeoJSON file containing zip code boundaries for mapping
zip_geo = gpd.read_file("data/Zipcodes.geojson")
print(zip_geo.head())

# Ensure zip codes are treated as strings for consistent merging
zip_geo['zip'] = zip_geo['zip'].astype(str)
sd_acs_clear['zip'] = sd_acs_clear['zip'].astype(str)

# Merge the zip code geometries with the Census and AFDC data
sd_geo_merged = zip_geo.merge(sd_acs_clear, on='zip', how='left')

# Step 4: Plotting using Matplotlib and GeoPandas
# Create a choropleth map of San Diego population by zip code
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
sd_geo_merged.plot(
    column='Total Population',  # Column used to color the map
    cmap='OrRd',    # Colormap for visualization
    linewidth=0.8,  # Line width for zip code boundaries
    edgecolor='black',  # Color for the boundaries
    ax=ax
)

# Add title and remove axes for cleaner visualization
ax.set_title('San Diego Population by Zip Code', fontsize=20)
ax.set_axis_off()
plt.show()


