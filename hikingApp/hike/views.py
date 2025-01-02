from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.functions import *
import logging
from .mongo_helper import MongoDBHelper
from bson.json_util import dumps
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

logger = logging.getLogger(__name__)

# Create your views here.
def routeplanner(request):
    return render(request, "hike/routeplanner.html")

# Create your views here.
def frontpage(request):
    # Check if "visits" is already in the session
    if 'visits' not in request.session:
        # Initialize it if it doesn't exist
        request.session['visits'] = 0

    # Increment the visits
    request.session['visits'] += 1
    return render(request, "hike/frontpage.html", {'visits': request.session['visits']})

def login(request):
    return render(request, "hike/login.html")

def history(request):
    return render(request, "hike/history.html")

@csrf_exempt
def receive_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data
            marker1_lat = data.get('marker1').get('lat')
            marker1_lng = data.get('marker1').get('lng')
            marker2_lat = data.get('marker2').get('lat')
            marker2_lng = data.get('marker2').get('lng')

            coord1 = (marker1_lng, marker1_lat)
            coord2 = (marker2_lng, marker2_lat)
            route = plan_route(coord1, coord2)
            # Store in the session
            request.session["route"] = route

            return JsonResponse({"status": "success", "line_data": route, "route":request.session["route"]})
        except Exception as e:
            print(f"Error in POST: {e}")  # Debugging line
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


@csrf_exempt  # Exempt CSRF protection for simplicity in testing
def save_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data
            route_data = data.get('route')
            route_name = data.get("name")

            if len(route_name) == 0:
                route_name = get_random_string(5)

            # Ensure valid route data
            if not route_data:
                return JsonResponse({"status": "error", "message": "No route data provided"}, status=400)

            # Prepare the document to save in MongoDB
            document = {
                "route_name": route_name,  # You can change this or make it dynamic
                "route": route_data
            }

            # Insert the document into the 'routes' collection in MongoDB
            mongo_helper = MongoDBHelper()
            inserted_id = mongo_helper.insert_document('routes', document)

            # Return a success response with the inserted ID
            return JsonResponse({"status": "success", "inserted_id": str(inserted_id)})

        except Exception as e:
            print(f"Error saving route: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
@csrf_exempt
def load_routes(request):
    if request.method == "GET":
        try:
            logging.info("Fetching routes from MongoDB")
            mongo_helper = MongoDBHelper()
            collection = mongo_helper.get_collection("routes")
            
            # Serialize MongoDB data
            serialized_data = dumps(collection)  # Converts ObjectId and other BSON types
            
            return JsonResponse({
                "status": "success",
                "collection_data": serialized_data
            }, safe=False)
        
        except Exception as e:
            logging.error(f"Error fetching routes: {e}")
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid HTTP method. Only GET is allowed."
        }, status=405)
