from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def routeplanner(request):
    return render(request, "hike/routeplanner.html")


names = ["Tamara", "Krijn"]
# Create your views here.
def frontpage(request):
    return render(request, "hike/frontpage.html", {
        "name1":names[0], "name2":names[1]
    })