import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

sdge_coords = (32.8335, -117.1571)
my_station_coords = (32.874618, -117.219413)

graph = ox.graph_from_point(sdge_coords, dist=10000, network_type='drive')

sdge_node = ox.distance.nearest_nodes(graph, sdge_coords[1], sdge_coords[0])
station_node = ox.distance.nearest_nodes(graph, my_station_coords[1], my_station_coords[0])

distance_meters = nx.shortest_path_length(graph, sdge_node, station_node, weight='length')
route = nx.shortest_path(graph, sdge_node, station_node, weight='length')

distance_km = distance_meters / 1000
travel_time_minutes = nx.shortest_path_length(graph, sdge_node, station_node, weight='travel_time')

fig, ax = ox.plot_graph_route(graph, route, route_linewidth=3, node_size=0, bgcolor='w')

print(f"Distance: {distance_km:.2f} km\nDrive time: {travel_time_minutes:.2f} minutes")
