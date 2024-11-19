from django.contrib import admin
from django.urls import include, path
from inventory import views as inventory_views
from places import views as place_views

urlpatterns = [
    path("", inventory_views.index, name="index"),
    path(
        "data/locations.geojson",
        place_views.make_locations_geojson,
        name="locations_geojson",
    ),
    path(
        "data/items-by-status.json",
        inventory_views.make_items_by_status_json,
        name="items_by_status",
    ),
    path("inventory/", include("inventory.urls")),
    # Enables the entire admin
    path("admin/", admin.site.urls),
]
