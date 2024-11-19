import django_filters
import django_tables2 as tables
from django.urls import reverse

from .models import Item


class ItemTable(tables.Table):
    title = tables.Column(
        linkify=lambda record: reverse("inventory:item_detail", args=[record.pk]),
        attrs={
            "a": {
                "class": "text-iona-maroon hover:text-iona-aqua-green transition-colors"
            }
        },
        verbose_name="Title",
    )
    tgm_genre = tables.Column(verbose_name="Genre")
    pub_date = tables.Column(verbose_name="Date Range")
    record_status = tables.Column(verbose_name="Status")

    class Meta:
        model = Item
        fields = (
            "title",
            "tgm_genre",
            "pub_date",
            "record_status",
        )
        attrs = {
            "class": "table-fixed min-w-full divide-y divide-gray-300",
            "th": {
                "class": "px-3 py-3.5 text-left text-sm font-semibold text-gray-900 bg-gray-50"
            },
            "td": {"class": "whitespace-nowrap px-3 py-4 text-sm text-gray-500"},
            "tr": {"class": "even:bg-gray-50"},
        }
        pagination_template = "django_tables2/pagination.html"


class ItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label="Title contains")
    tgm_genre = django_filters.ModelChoiceFilter(
        queryset=Item.objects.values_list("tgm_genre", flat=True).distinct()
    )
    record_status = django_filters.ChoiceFilter(choices=Item.RECORD_STATUS_CHOICES)

    class Meta:
        model = Item
        fields = ["title", "tgm_genre", "record_status"]
