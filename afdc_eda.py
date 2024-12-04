#Electric Vehicle Charging Stations Analysis

import json
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as geo
import plotly.express as px

# retrieve the full AFDC dataset via a terminal command
# curl -o afdc_full.json "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key=ygp1Tgcbv8Set3iJJz3Fs87Vns7mUaqM2JH05hhD"

# load full afdc data into a dataframe
with open('data/afdc_full.json', 'r') as f:
    afdc = json.load(f)
fs = afdc.get('fuel_stations', [])
afdc_df = pd.DataFrame(fs)
print(afdc_df.head())


# Data EDA

# Filter data to analyze electric vehicle charging stations in San Diego City
sd = afdc_df[(afdc_df['city'] == 'San Diego')]
print(len(sd))

# Filter further by electric stations and select relevant columns
sd_data = afdc_df[(afdc_df['city'] == 'San Diego') & (afdc_df['fuel_type_code'] == 'ELEC')][['city', 'open_date']]
print(sd_data.head())
print(len(sd_data))


# Time series plot: Number of Electric Stations Opened in San Diego City by Year
sd_data['open_date'] = pd.to_datetime(sd_data['open_date'])
sd_data['year'] = sd_data['open_date'].dt.year
stations_each_year = sd_data.groupby('year').size()

plt.figure(figsize=(10, 6))
stations_each_year.plot(kind='line', marker='o')
plt.title('Number of Electric Stations Opened in San Diego City by Year')
plt.xlabel('Year')
plt.ylabel('Number of Electric Stations')
years = stations_each_year.index
plt.xticks(ticks=range(years.min(), years.max() + 1, 1))
plt.grid(True)
plt.show()


# Geospatial analysis of electric stations by state over time
afdc_by_state = afdc_df[afdc_df['fuel_type_code'] == 'ELEC'][['state', 'open_date']]
afdc_by_state['open_date'] = pd.to_datetime(afdc_by_state['open_date'], errors='coerce')
afdc_by_state['year'] = afdc_by_state['open_date'].dt.year
afdc_by_state = afdc_by_state[afdc_by_state['year'] <= 2024]

# Load US states GeoJSON data
with open("data/us-states.json") as f:
    us_states = json.load(f)

# Aggregate data by year and state
state_counts = afdc_by_state.groupby(['year', 'state']).size().reset_index(name='count')

# Normalize GeoJSON data for compatibility with the dataset
geo_data = pd.json_normalize(us_states['features'])
geo_data = geo_data[['properties.name', 'id']]
geo_data.columns = ['state_name', 'state_id']

# Create choropleth map using plotly to visualize the data
fig = px.choropleth(
    state_counts,
    geojson=us_states,
    locations='state',
    locationmode='USA-states',
    color='count',
    animation_frame='year',
    color_continuous_scale='Blues',
    scope='usa',
    title='Number of electric stations opened in each state (Yearly)'
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    transition_duration=500
)

# Display the interactive map
fig.show()

# Documentation:
# 1. The dataset is loaded from a JSON file retrieved using the AFDC API.
# 2. Initial filtering focuses on electric vehicle charging stations in San Diego City.
# 3. A time series analysis shows the number of electric stations opened yearly in San Diego City.
# 4. Data is grouped by year for visualization in a line plot.
# 5. Geospatial data is used to analyze trends across US states with a focus on electric charging stations.
# 6. The plotly choropleth map visualizes the count of stations by state for each year using an animated frame.
# 7. GeoJSON data is normalized for compatibility with the AFDC dataset to enable accurate state-level mapping