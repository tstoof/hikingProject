from django.shortcuts import render
names = ["Tamara", "Krijn"]
# Create your views here.
def index(request):
    return render(request, "frontpage/index.html", {
        "name1":names[0], "name2":names[1]
    })