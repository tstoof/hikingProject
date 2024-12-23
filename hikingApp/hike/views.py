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
    return render(request, "hike/frontpage.html")


# View to handle the incoming coordinates
@csrf_exempt  # You might want to use CSRF protection in a production app
def receive_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data
            marker1_lat = data.get('marker1').get('lat')
            marker1_lng = data.get('marker1').get('lng')
            marker2_lat = data.get('marker2').get('lat')
            marker2_lng = data.get('marker2').get('lng')

            # Do something with the coordinates (e.g., pass them to a function)
            # Example: Call a function to process the coordinates
            # process_coordinates(marker1_lat, marker1_lng, marker2_lat, marker2_lng)
            coord1 = (marker1_lat, marker1_lng)
            coord2 = (marker2_lat, marker2_lng)
            helloCoordinates = say_hello_to_coordinates(coord1, coord2)
            return JsonResponse({"status": "success", "message": helloCoordinates})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
