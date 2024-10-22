import json
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as geo
import plotly.express as px

# command lines to get the full afdc dataset
# curl -o afdc_full.json "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key=ygp1Tgcbv8Set3iJJz3Fs87Vns7mUaqM2JH05hhD"

# convert full afdc data into a dataframe
with open('afdc_full.json', 'r') as f:
    afdc = json.load(f)
fs = afdc.get('fuel_stations', [])
afdc_df = pd.DataFrame(fs)
print(afdc_df.head())

# # get all zip codes in which there are in SDGE service territory
# sdge_terri = pd.read_excel('SDGE_zip.xlsx')
# print(sdge_terri.head())
# uni_zip = sdge_terri['ZIP_CODE'].unique()
# zip_str = ','.join(map(str, uni_zip))
# print(zip_str)

# use the coma-separated zip codes to get the count of total fuel stations in SDGE service territory
# https://developer.nrel.gov/api/alt-fuel-stations/v1.json?&api_key=ygp1Tgcbv8Set3iJJz3Fs87Vns7mUaqM2JH05hhD&fuel_type=ELEC&zip=91901,91902,91905,91906,91910,91911,91912,91913,91914,91915,91916,91917,91931,91932,91934,91935,91941,91942,91945,91948,91950,91962,91963,91970,91977,91978,91980,92003,92004,92007,92008,92009,92010,92011,92014,92019,92020,92021,92023,92024,92025,92026,92027,92028,92029,92032,92036,92037,92040,92041,92050,92054,92055,92056,92057,92058,92059,92060,92061,92062,92064,92065,92066,92067,92068,92069,92070,92071,92072,92075,92078,92079,92081,92082,92083,92084,92085,92086,92091,92092,92093,92096,92101,92102,92103,92104,92105,92106,92107,92108,92109,92110,92111,92112,92113,92114,92115,92116,92117,92118,92119,92120,92121,92122,92123,92124,92126,92127,92128,92129,92130,92131,92132,92133,92134,92135,92136,92139,92145,92150,92152,92154,92155,92158,92161,92173,92179,92182,92199,92536,92624,92629,92649,92651,92653,92654,92656,92672,92673,92674,92675,92676,92677,92679,92688,92690,92691,92692,92693,92694,92697,95126
# total = 1728
# It seems difficult to get the number of stations that are SDGE-owned because there are other provides of G&E, and they are not specified in afdc dataset.



# Data EDA


# stations in san diego city
sd = afdc_df[(afdc_df['city'] == 'San Diego')]
print(len(sd))
sd_data = afdc_df[(afdc_df['city'] == 'San Diego') & (afdc_df['fuel_type_code'] == 'ELEC')][['city', 'open_date']]
print(sd_data.head())
print(len(sd_data))


# time series plot
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


# geospatial plot
afdc_by_state = afdc_df[afdc_df['fuel_type_code'] == 'ELEC'][['state', 'open_date']]
afdc_by_state['open_date'] = pd.to_datetime(afdc_by_state['open_date'], errors='coerce')
afdc_by_state['year'] = afdc_by_state['open_date'].dt.year
afdc_by_state = afdc_by_state[afdc_by_state['year'] <= 2024]

with open("us-states.json") as f:
    us_states = json.load(f)

state_counts = afdc_by_state.groupby(['year', 'state']).size().reset_index(name='count')

geo_data = pd.json_normalize(us_states['features'])
geo_data = geo_data[['properties.name', 'id']]
geo_data.columns = ['state_name', 'state_id']

# Create choropleth map using plotly
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

# Show the plot
fig.show()