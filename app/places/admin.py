# places/admin.py

from django.contrib import admin
from .models import Location, State, Empire, Region, Claim


# Register models
@admin.register(Region)
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass


# Make Claim an inline option
class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 1


# Register models with Claim inline
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = (ClaimInline,)
    search_fields = ['name', 'notes']


@admin.register(Empire)
class EmpireAdmin(admin.ModelAdmin):
    inlines = (ClaimInline,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'geoname', 'notes')
    list_filter = ('state',)
    search_fields = ['name', 'notes']
    fieldsets = (
        (None, {
            'fields': ('name', 'state')
        }),
        (None, {
            'fields': ('latitude', 'longitude'),
            'description': 'Use decimal values only. Make sure you only use values in the WSG84 reference system, which is the default on Geonames, Google, and Wikipedia.'
        }),
        (None, {
            'fields': ('geoname',),
            'description': 'Record full, permanent URL.'
        }),
        (None, {
            'fields': ('regions', 'notes')
        })
    )
