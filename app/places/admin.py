# places/admin.py

from django.contrib import admin
from .models import Location, State, Empire, Region, Claim

admin.site.register(Location)
admin.site.register(State)
admin.site.register(Empire)
admin.site.register(Region)
admin.site.register(Claim)
