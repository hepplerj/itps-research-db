#import requests
from django.shortcuts import render
from django.http import JsonResponse

from .models import Location, State

def make_locations_geojson(request):
	locations_geojson = {"type": "FeatureCollection", "features": []}
	locations = []
	for l in Location.objects.all():
		loc = {
		"type": "Feature",
		"geometry": {
		    "type": "Point",
		    "coordinates": [l.longitude, l.latitude]
		    },
		"properties": {
		    "name": l.name + ", " + str(l.state)
		    }
		}
		locations.append(loc)
	locations_geojson['features'] = locations
	return JsonResponse(locations_geojson)