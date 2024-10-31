import cenpy as cp
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import plotly.express as px


# Connect to ACS 5-year estimates for 2022
conn = cp.remote.APIConnection("ACSDT5Y2022")

# Specify variables
variables_to_pull = ['B01001_001E', 'NAME']
geo_unit = 'zip code tabulation area:*'

# Query
data = conn.query(variables_to_pull, geo_unit)
data.drop(columns = ['NAME'], inplace=True)
data.columns = ['Total Population', 'zip']
# print(data.head())
# print(len(data))
# print(len(set(data['zip'].unique())))

# Save to a CSV
data.to_csv("acs_5y_2022.csv", index=False)
print("acs_5y_2022.csv created!")


# get afdc
with open('afdc_full.json', 'r') as f:
    afdc = json.load(f)
fs = afdc.get('fuel_stations', [])
afdc_df = pd.DataFrame(fs)
sd = afdc_df[(afdc_df['city'] == 'San Diego') & (afdc_df['fuel_type_code'] == 'ELEC')]
# print(sd.head())
# print(len(sd))
# print(len(set(sd['zip'].unique())))

sd_acs = sd.merge(data, how='left',on='zip')
# print(sd_acs[['zip', 'Total Population']][:10])

sd_acs.to_csv("sd_acs.csv", index=False)
print("sd_acs.csv created!")

# extract some columns for clearer plotting
sd_acs_clear = sd_acs[['zip', 'Total Population', 'latitude', 'longitude']]
print(sd_acs_clear.head())




# start plotting
zip_geo = gpd.read_file("Zipcodes.geojson")
print(zip_geo.head())

zip_geo['zip'] = zip_geo['zip'].astype(str)
sd_acs_clear['zip'] = sd_acs_clear['zip'].astype(str)

sd_geo_merged = zip_geo.merge(sd_acs_clear, on='zip', how='left')




fig, ax = plt.subplots(1, 1, figsize=(15, 10))
sd_geo_merged.plot(
    column='Total Population',
    cmap='OrRd',
    linewidth=0.8,
    edgecolor='black',
    ax=ax
)


ax.set_title('San Diego Population by Zip Code', fontsize=20)
ax.set_axis_off()
plt.show()



# sd_geo_merged_json = sd_geo_merged.__geo_interface__

# fig = px.choropleth(
#     sd_geo_merged,
#     geojson=sd_geo_merged_json,
#     locations='zip',
#     # featureidkey='properties.zip',
#     color='Total Population',
#     color_continuous_scale='OrRd',
#     hover_data=['zip', 'Total Population'],
#     title='San Diego Population by Zip Code'
# )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(
#     title=dict(x=0.5, xanchor='center'),
#     margin={"r":0, "t":30, "l":0, "b":0}
# )

# fig.show()