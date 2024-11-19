from django.urls import path

from .views import ItemDetailView, ItemListView

app_name = "inventory"
urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
]
