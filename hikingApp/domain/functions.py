import openrouteservice
from openrouteservice.convert import decode_polyline
import os
from decouple import config

def say_hello_to_coordinates(coord1, coord2):
    lat1, lng1 = coord1
    lat2, lng2 = coord2

    # Example: return a simple message with the coordinates
    return f"Hello, your coordinates are: Marker 1 at ({lat1}, {lng1}), Marker 2 at ({lat2}, {lng2})"


def create_straight_line_json(coord1, coord2, num_points=100):
    """
    Create a JSON object representing a straight line between two points.

    Args:
        coord1 (tuple): The starting point as (latitude, longitude).
        coord2 (tuple): The ending point as (latitude, longitude).
        num_points (int): Number of points in the straight line. Default is 100.
    
    Returns:
        dict: A JSON-like dictionary representing the line.
    """
    try:
        # Unpack coordinates
        lat1, lng1 = coord1
        lat2, lng2 = coord2

        lat1 = float(lat1)
        lat2 = float(lat2)
        lng1 = float(lng1)
        lng2 = float(lng2)

        # Generate points along the line
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)  # Linear interpolation factor (0 to 1)
            lat = lat1 + t * (lat2 - lat1)
            lng = lng1 + t * (lng2 - lng1)
            points.append({"latitude": round(lat, 6), "longitude": round(lng, 6)})

        # Create JSON structure
        line_data = {
            "type": "LineString",
            "coordinates": [[point["longitude"], point["latitude"]] for point in points]
        }

        return line_data  # Return the dictionary directly
    
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")
    

def plan_route(coord1, coord2):
    try:
        # Initialize the client with your API key
        client = openrouteservice.Client(key=config('ORS_API_KEY'))
        route = client.directions(
            coordinates=[coord1, coord2],
            profile='foot-hiking',  # Other options: 'cycling-regular', 'foot-walking', etc.
        )
        route = decode_polyline(route['routes'][0]['geometry'])
        return route
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")