from django.urls import path

from .views import ItemDetailView, ItemListView, export_full_dataset

app_name = "inventory"
urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("export/full/", export_full_dataset, name="export_full_dataset"),
]
