import osmnx as ox
import networkx as nx
import geopandas as gpd

place_name = "Hogwarts Castle, Scotland"

G = ox.graph_from_place(place_name, network_type='walk')

start_point = (55.955169, -3.1664778)
end_point = (55.933448, -3.2265285)

start_node = ox.nearest_nodes(G, X=start_point[1], Y=start_point[0])
end_node = ox.nearest_nodes(G, X=end_point[1], Y=end_point[0])

route = nx.shortest_path(G, start_node, end_node, weight='length')

route_edges = ox.graph_to_gdfs(G.subgraph(route), nodes=False)


# Clean the GeoDataFrame to ensure all attributes are GeoJSON-compatible
def clean_gdf(gdf):
    for column in gdf.columns:
        if gdf[column].dtype == object:  # Check if the column type is object (which can be anything, including lists)
            # Check if the column contains lists
            if any(isinstance(i, list) for i in gdf[column]):
                gdf = gdf.drop(columns=[column])  # Drop the column if it contains lists
    return gdf


# Clean the route_edges GeoDataFrame
route_edges_cleaned = clean_gdf(route_edges)

print(f"{round(sum(route_edges_cleaned['length'])/1000, 2)}km")

route_edges_cleaned.to_file("FILEPATH.geojson", driver='GeoJSON')

