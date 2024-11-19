import django_filters
import django_tables2 as tables
from django.urls import reverse

from .models import Item


class ItemTable(tables.Table):
    accession_number = tables.Column(
        linkify=lambda record: reverse("inventory:item_detail", args=[record.pk])
    )
    title = tables.Column()
    tgm_genre = tables.Column()
    pub_date = tables.Column()
    record_status = tables.Column()
    actions = tables.TemplateColumn(
        template_code="""
            <button type="button" 
                    class="btn btn-sm btn-primary" 
                    data-bs-toggle="modal" 
                    data-bs-target="#itemModal" 
                    data-item-id="{{ record.id }}">
                View Details
            </button>
        """,
        orderable=False,
    )

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "accession_number",
            "short_title",
            "tgm_genre",
            "pub_date",
            "record_status",
            "actions",
        )
        attrs = {"class": "table table-striped table-hover"}


class ItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label="Title contains")
    tgm_genre = django_filters.ModelChoiceFilter(
        queryset=Item.objects.values_list("tgm_genre", flat=True).distinct()
    )
    record_status = django_filters.ChoiceFilter(choices=Item.RECORD_STATUS_CHOICES)

    class Meta:
        model = Item
        fields = ["title", "tgm_genre", "record_status"]
