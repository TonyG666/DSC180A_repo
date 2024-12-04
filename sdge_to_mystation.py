import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Coordinates for SDG&E campus and the station I visited in person
sdge_coords = (32.8335, -117.1571)
my_station_coords = (32.874618, -117.219413)

# Generate a street network graph within 10,000 meters (10 km) of SDG&E
# using OSMnx, filtering for drivable roads
graph = ox.graph_from_point(sdge_coords, dist=10000, network_type='drive')

# Find the closest graph nodes to the given coordinates
# OSMnx expects coordinates in the order (longitude, latitude)
sdge_node = ox.distance.nearest_nodes(graph, sdge_coords[1], sdge_coords[0])
station_node = ox.distance.nearest_nodes(graph, my_station_coords[1], my_station_coords[0])

# Calculate the shortest path distance (in meters) between the two nodes
# This uses the "length" attribute (representing edge distance in meters)
distance_meters = nx.shortest_path_length(graph, sdge_node, station_node, weight='length')

# Find the shortest route between the two nodes
# Also using the "length" attribute as the weight
route = nx.shortest_path(graph, sdge_node, station_node, weight='length')

# Convert the distance from meters to kilometers
distance_km = distance_meters / 1000

# Calculate the estimated travel time (in minutes)
# Assuming 'travel_time' attribute exists for graph edges
travel_time_minutes = nx.shortest_path_length(graph, sdge_node, station_node, weight='travel_time')

# Plot the street network graph with the computed route highlighted
# Customizing plot aesthetics: wider route line and no visible nodes
fig, ax = ox.plot_graph_route(graph, route, route_linewidth=3, node_size=0, bgcolor='w')

# Print the results: distance in kilometers and travel time in minutes
print(f"Distance: {distance_km:.2f} km\nDrive time: {travel_time_minutes:.2f} minutes")
