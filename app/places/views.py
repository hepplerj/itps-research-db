# import requests
from django.shortcuts import render
from django.http import JsonResponse

from .models import Location, State


def make_locations_geojson(request):
    locations_geojson = {"type": "FeatureCollection", "features": []}
    locations = []
    for location in Location.objects.all():
        loc = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location.longitude, location.latitude]
            },
            "properties": {
                "name": location.name + ", " + str(location.state)
            }
        }
        locations.append(loc)
    locations_geojson['features'] = locations
    return JsonResponse(locations_geojson)
