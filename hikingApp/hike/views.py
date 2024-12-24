from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.functions import *
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

@csrf_exempt
def receive_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data
            marker1_lat = data.get('marker1').get('lat')
            marker1_lng = data.get('marker1').get('lng')
            marker2_lat = data.get('marker2').get('lat')
            marker2_lng = data.get('marker2').get('lng')

            coord1 = (marker1_lat, marker1_lng)
            coord2 = (marker2_lat, marker2_lng)
            straight_line = create_straight_line_json(coord1, coord2)

            # Store in the session
            request.session["route"] = straight_line
            print("Saved route to session:", straight_line)  # Debugging line
            return JsonResponse({"status": "success", "line_data": straight_line, "route":request.session["route"]})
        except Exception as e:
            print(f"Error in POST: {e}")  # Debugging line
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

   