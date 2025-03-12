import django_filters
import django_tables2 as tables
from django import forms
from django.contrib.postgres.forms import DateRangeField as FormDateRangeField
from django.db.models import F, Func, Q
from django.urls import reverse
from psycopg2.extras import DateRange

from .models import Item, Item_Creator, TGM_Genre


class YearExtract(Func):
    function = "EXTRACT"
    template = "%(function)s(YEAR FROM %(expressions)s)"


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
    pub_date = tables.Column(
        verbose_name="Date Range",
        attrs={
            "td": {
                "class": "align-middle text-center whitespace-nowrap text-sm",
                "style": "min-width: 200px;",
            },
            "th": {"class": "text-sm", "style": "min-width: 200px;"},
        },
    )
    tgm_genre = tables.Column(verbose_name="Genre")

    def render_pub_date(self, value):
        if value and value.lower and value.upper:
            return (
                f"{value.lower.strftime('%Y-%m-%d')}—{value.upper.strftime('%Y-%m-%d')}"
            )
        return "—"  # None values

    class Meta:
        model = Item
        fields = (
            "title",
            "pub_date",
            "tgm_genre",
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
        queryset=TGM_Genre.objects.all().order_by("name"),
        label="Genre",
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    # creator = django_filters.ChoiceFilter(
    #     choices=Item_Creator.objects.all().order_by(
    #         "person__name",
    #     ),
    #     label="Creator",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
    #         }
    #     ),
    # )
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
        lookup_expr="contains",  # Changed from lower__gte
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
        lookup_expr="contains",  # Changed from upper__lte
        label="End Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
            }
        ),
    )
    # year = django_filters.ChoiceFilter(
    #     label="Year",
    #     method="filter_year",
    #     empty_label="All Years",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-iona-maroon focus:ring-iona-maroon",
    #         }
    #     ),
    # )

    class Meta:
        model = Item
        fields = [
            "search",
            "tgm_genre",
            "record_status",
            "date_start",
            "date_end",
        ]

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
                | Q(notes__icontains=keyword)
            )

        return queryset.filter(query).distinct()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # Get all dates and extract years manually
    #     dates = Item.objects.exclude(pub_date__isnull=True).values_list(
    #         "pub_date", flat=True
    #     )
    #     years = set()
    #     for daterange in dates:
    #         if daterange and daterange.lower:
    #             years.add(daterange.lower.year)
    #
    #     years = sorted(years)
    #     self.filters["year"].extra["choices"] = [
    #         (str(year), str(year)) for year in years
    #     ]
    #
    # def filter_year(self, queryset, name, value):
    #     if value:
    #         start_date = f"{value}-01-01"
    #         end_date = f"{value}-12-31"
    #         return queryset.filter(
    #             pub_date__isnull=False,  # Exclude null dates
    #             pub_date__overlap=(start_date, end_date),
    #         )
    #     return queryset
