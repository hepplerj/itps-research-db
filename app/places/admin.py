# places/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from inventory.resources import (
    ClaimResource,
    EmpireResource,
    LocationResource,
    RegionResource,
    StateResource,
)

from .models import Claim, Empire, Location, Region, State


# Register models
@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource


@admin.register(Claim)
class ClaimAdmin(ImportExportModelAdmin):
    resource_class = ClaimResource


# Make Claim an inline option
class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 1


# Register models with Claim inline
@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource
    inlines = (ClaimInline,)
    search_fields = ["name", "notes"]


@admin.register(Empire)
class EmpireAdmin(ImportExportModelAdmin):
    resource_class = EmpireResource
    inlines = (ClaimInline,)


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ("name", "state", "geoname", "notes")
    list_filter = ("state",)
    search_fields = ["name", "notes"]
    fieldsets = (
        (None, {"fields": ("name", "state")}),
        (
            None,
            {
                "fields": ("latitude", "longitude"),
                "description": "Use decimal values only. Make sure you only use values in the WSG84 reference system, which is the default on Geonames, Google, and Wikipedia.",
            },
        ),
        (None, {"fields": ("geoname",), "description": "Record full, permanent URL."}),
        (None, {"fields": ("regions", "notes")}),
    )
