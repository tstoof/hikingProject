from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def routeplanner(request):
    return render(request, "hike/routeplanner.html")


# Create your views here.
def frontpage(request):
    return render(request, "hike/frontpage.html")