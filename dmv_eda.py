# Vehicle Count by Fuel Type and Model Year (datasets from DMV)

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load and preprocess the dataset
# The dataset is expected to have columns: 'Model Year', 'Fuel', and 'Vehicles'.
dmv_df = pd.read_csv('data/dmv.csv')

# Display the first few rows of the dataset and its length for verification
print(dmv_df.head())
print(len(dmv_df))

# Filter out unwanted data
# Exclude rows where 'Model Year' is '<2010' or 'Unk' as these do not represent specific years.
dmv_df = dmv_df[(dmv_df['Model Year'] != '<2010') & (dmv_df['Model Year'] != 'Unk')]

# Group data by 'Model Year' and 'Fuel', summing up the 'Vehicles' for each group
grouped_df = dmv_df.groupby(['Model Year', 'Fuel'])['Vehicles'].sum().reset_index()

# Extract unique model years and sort them for chronological visualization
md_years = sorted(grouped_df['Model Year'].unique())

# Initialize the bar chart with data from the first model year
initial = md_years[0]
fil_df = grouped_df[grouped_df['Model Year'] == initial]
bar_data = [go.Bar(x=fil_df['Fuel'], y=fil_df['Vehicles'], name=f"Year {initial}")]

# Create frames for animation, one for each model year
frames = []
for year in md_years:
    year_data = grouped_df[grouped_df['Model Year'] == year]
    frame = go.Frame(data=[go.Bar(x=year_data['Fuel'], y=year_data['Vehicles'])], name=str(year))
    frames.append(frame)

# Define the layout of the figure, including sliders and play/pause buttons
layout = go.Layout(
    title="Vehicle Count by Fuel Type and Model Year",
    xaxis=dict(title="Fuel Type"),
    yaxis=dict(title="Vehicle Count"),
    sliders=[{
        "active": 0,
        "currentvalue": {"prefix": "Model Year: "},
        "pad": {"t": 50},
        "steps": [{"method": "animate", "label": str(year), "args": [[str(year)], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}]} for year in md_years]
    }],
    updatemenus=[{
        "buttons": [
            {"args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True, "mode": "immediate"}],
             "label": "Play", "method": "animate"},
            {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
             "label": "Pause", "method": "animate"}
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons"
    }]
)

# Create the figure and display it
fig = go.Figure(data=bar_data, layout=layout, frames=frames)
fig.show()


# Documentation Notes:
# 1. Dataset:
#    - The script expects a CSV file at 'data/dmv.csv' with columns:
#      'Model Year' (vehicle model year), 'Fuel' (fuel type), and 'Vehicles' (vehicle count).
# 2. Preprocessing:
#    - Rows with 'Model Year' values '<2010' or 'Unk' are excluded as they lack specific information.
# 3. Visualization:
#    - An animated bar chart is created using Plotly.
#    - The animation transitions through vehicle counts by fuel type for each model year.
#    - Sliders and play/pause buttons allow interactive exploration of the data.
# 4. Interaction:
#    - Use the slider to select a specific year.
#    - Use the play button to animate through all years sequentially.