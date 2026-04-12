import osmnx as ox

# Step 1: Select a small area (IMPORTANT: keep it small)
place_name = "Adyar, Chennai, India"

# Step 2: Download road network from OpenStreetMap
print("Downloading map data...")
G = ox.graph_from_place(place_name, network_type='drive')

# Step 3: Save as OSM XML file (for SUMO)
print("Saving map as OSM file...")
ox.save_graph_xml(G, filepath="map.osm")

print("Map saved as map.osm")