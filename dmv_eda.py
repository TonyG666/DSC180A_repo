import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# get the dataset
dmv_df = pd.read_csv('data/dmv.csv')
print(dmv_df.head())
print(len(dmv_df))


# vehicle fuel type counts over the years graph
dmv_df = dmv_df[(dmv_df['Model Year'] != '<2010') & (dmv_df['Model Year'] != 'Unk')]
grouped_df = dmv_df.groupby(['Model Year', 'Fuel'])['Vehicles'].sum().reset_index()
md_years = sorted(grouped_df['Model Year'].unique())

initial = md_years[0]
fil_df = grouped_df[grouped_df['Model Year'] == initial]
bar_data = [go.Bar(x=fil_df['Fuel'], y=fil_df['Vehicles'], name=f"Year {initial}")]

frames = []
for year in md_years:
    year_data = grouped_df[grouped_df['Model Year'] == year]
    frame = go.Frame(data=[go.Bar(x=year_data['Fuel'], y=year_data['Vehicles'])], name=str(year))
    frames.append(frame)

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

fig = go.Figure(data=bar_data, layout=layout, frames=frames)
fig.show()
