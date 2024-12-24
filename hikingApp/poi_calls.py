#### API request voor POIs (Points of Interest)

# Load packages
import pandas as pd 
import requests
import geopandas as gpd
import json
import requests
import json
import math



### Prepare test route ####
# Load pieterpad
route_gdf = gpd.read_file("25_sittard_strabeek(1).gpx", layer = "tracks") ### Tijdelijke line_shape voor testen van request.

route_gdf = route_gdf[["name", "geometry"]]

# Convert the GeoDataFrame to GeoJSON format
geojson_data = route_gdf.to_json()

# Optionally, print or save the GeoJSON data
print(geojson_data)

# Save GeoJSON data to a file
with open("route.json", "w") as f:
    f.write(geojson_data)

# Open the json as a json file
with open("route.json", "r") as file:
    geojson_data = json.load(file)


#### FUNCTIES
# 1. Haversine: berekent afstand tussen twee geografische puntlocaties.
# 2.: Get bounding box: bepaalt de bounding box van de route, met een buffer eromheen van 2 kilometer om er zeker van te zijn dat alle relevante opties worden getoond.
# 3.: fetch_pois: api requests voor supermarkten, horeca en OV.
# 4.: get_closest_pois: bereken voor elke node welke POI het dichstbij is.
# 5.: add_pois_to_geojson: voeg de resultaten toe aan de json van de line feature
# 6: process_route: toepassen van alle bovenstaande functies. 
# Haversine formula to calculate distance between two coordinates (in kilometers)
import requests
import json
import math

# Haversine formula to calculate distance between two coordinates (in kilometers)
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the distance between two points on the Earth using the Haversine formula.
    """
    R = 6371  # Radius of the Earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in km

def get_bounding_box(route_feature, buffer=0.02):
    """
    Calculate the bounding box around a route feature with a buffer.
    """
    min_lon, min_lat = float('inf'), float('inf')
    max_lon, max_lat = float('-inf'), float('-inf')

    # Loop through all coordinates in the route (MultiLineString)
    for line in route_feature['geometry']['coordinates']:
        for coord in line:
            lon, lat = coord
            # Update min/max coordinates
            min_lon = min(min_lon, lon)
            min_lat = min(min_lat, lat)
            max_lon = max(max_lon, lon)
            max_lat = max(max_lat, lat)

    # Add buffer to the bounding box
    min_lon -= buffer
    min_lat -= buffer
    max_lon += buffer
    max_lat += buffer
    
    return min_lon, min_lat, max_lon, max_lat

def fetch_pois(min_lon, min_lat, max_lon, max_lat, facility_type):
    """
    Fetch Points of Interest (POIs) from the Overpass API within a bounding box.
    """
    if facility_type == "supermarket":
        overpass_query = f'''
        [out:json];
        (node[shop="supermarket"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out body;
        '''
    if facility_type == "horeca":
        overpass_query = f'''
            [out:json];
            (
            node[amenity="cafe"]({min_lat},{min_lon},{max_lat},{max_lon});
            node[amenity="restaurant"]({min_lat},{min_lon},{max_lat},{max_lon});
            );
            out body;
            '''

    if facility_type == "bus": 
        overpass_query = f'''
        [out:json];
        (node[highway="bus_stop"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out body;
        '''
    
    # Make the API request
    overpass_url = 'https://overpass-api.de/api/interpreter'
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching POIs:", response.status_code)
        return None

def get_closest_pois(route_feature, pois_data):
    """
    For each node in the route, find the closest POI and store it in a dictionary.
    """
    unique_pois = {}

    for element in pois_data['elements']:
        poi_lon, poi_lat = element['lon'], element['lat']
        
        # For each coordinate (node) in the route, calculate the closest POI
        for line in route_feature['geometry']['coordinates']:
            for coord in line:
                node_lon, node_lat = coord
                
                # Calculate distance to the POI
                distance = haversine(poi_lon, poi_lat, node_lon, node_lat)

                # If this POI is closer than the current one (or not yet assigned), assign it
                if (node_lon, node_lat) not in unique_pois or unique_pois[(node_lon, node_lat)]['distance'] > distance:
                    unique_pois[(node_lon, node_lat)] = {
                        "poi_name": element.get('tags', {}).get('name', 'Unknown'),
                        "coordinates": [poi_lon, poi_lat],
                        "distance": distance,
                        "properties": {**element['tags'], "distance": distance}
                    }

    return unique_pois

def add_pois_to_geojson(geojson_data, unique_pois):
    """
    Add unique POIs to the GeoJSON data.
    """
    search_results = []
    for poi_info in unique_pois.values():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": poi_info["coordinates"]
            },
            "properties": poi_info["properties"]
        }
        search_results.append(feature)

    geojson_data["features"].extend(search_results)
    return geojson_data

def process_route(geojson_data, facility_type):
    """
    Process the route and add closest unique POIs to the GeoJSON data.
    """
    # Get the first route feature
    route_feature = geojson_data['features'][0]
    
    # Step 1: Calculate bounding box around the route
    min_lon, min_lat, max_lon, max_lat = get_bounding_box(route_feature)
    
    # Step 2: Fetch POIs within the bounding box
    pois_data = fetch_pois(min_lon, min_lat, max_lon, max_lat, facility_type)
    
    if pois_data:
        # Step 3: Get closest unique POIs for each node
        unique_pois = get_closest_pois(route_feature, pois_data)
        
        # Step 4: Add unique POIs to the GeoJSON data
        updated_geojson = add_pois_to_geojson(geojson_data, unique_pois)
        return updated_geojson
    else:
        print("No POIs found.")
        return geojson_data

### Functie call en opslaan 

# Process the route and get the updated GeoJSON data
updated_geojson = process_route(geojson_data, facility_type="horeca")

# Print the updated GeoJSON data
print(json.dumps(updated_geojson, indent=4))

with open('route_with_pois.json', 'w') as f:
    json.dump(updated_geojson, f)


