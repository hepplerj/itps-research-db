import django_filters
import django_tables2 as tables
from django import forms
from django.contrib.postgres.forms import DateRangeField as FormDateRangeField
from django.db.models import Q
from django.urls import reverse
from psycopg2.extras import DateRange

from .models import Item


class DateRangeFilter(django_filters.Filter):
    field_class = FormDateRangeField

    def filter(self, qs, value):
        if value:
            return qs.filter(pub_date__overlap=DateRange(value.lower, value.upper))
        return qs


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
    record_status = tables.Column(verbose_name="Status")

    class Meta:
        model = Item
        fields = (
            "title",
            "tgm_genre",
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
    search = django_filters.CharFilter(
        method="search_fields",
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    tgm_genre = django_filters.ModelChoiceFilter(
        queryset=Item.objects.values_list("tgm_genre", flat=True).distinct(),
        label="Genre",
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    record_status = django_filters.ChoiceFilter(
        choices=Item.RECORD_STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    date_start = django_filters.DateFilter(
        field_name="pub_date",
        lookup_expr="lower__gte",
        label="Start Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    date_end = django_filters.DateFilter(
        field_name="pub_date",
        lookup_expr="upper__lte",
        label="End Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )

    class Meta:
        model = Item
        fields = ["search", "tgm_genre", "record_status", "date_start", "date_end"]

    def filter_start_date(self, queryset, name, value):
        if value:
            return queryset.filter(
                pub_date__contained_by=("[{},)".format(value.isoformat()))
            )
        return queryset

    def filter_end_date(self, queryset, name, value):
        if value:
            return queryset.filter(
                pub_date__contained_by=("(,{}]".format(value.isoformat()))
            )
        return queryset

    def search_fields(self, queryset, name, value):
        if not value:
            return queryset

        keywords = value.split()
        query = Q()
        for keyword in keywords:
            query |= (
                Q(title__icontains=keyword)
                | Q(physical_description__icontains=keyword)
                | Q(other_description__icontains=keyword)
                | Q(condition_notes__icontains=keyword)
                | Q(notes__icontains=keyword)
            )

        return queryset.filter(query).distinct()
