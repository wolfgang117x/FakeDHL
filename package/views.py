from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.

def home (request):
    return render(request, 'package/home.html')

def team(request):
	return render(request, 'package/team.html')

def project(request):
    return render(request, 'package/project.html')

def signup(request):
    if (request.method == 'POST'):
        name = request.POST.get("name")
        address = request.POST.get('address')
        phone = request.POST.get('zipcode')
        models.connect(name, address, phone)
        return render(request, 'package/home.html')

def track(request):
    return render(request, 'package/track.html')



def ship(request):
    return render(request, 'package/ship.html')