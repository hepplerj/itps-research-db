from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from import_export.formats.base_formats import XLSX
from inventory.models import Credit, Item
from inventory.resources import FullDatasetResource
from inventory.tables import ItemFilter, ItemTable
from organizations.models import Organization
from people.models import Person
from places.models import Location, State


def index(request):
    """View function for home page."""

    # Generate counts of some of the main objects
    num_items = Item.objects.all().count()
    num_orgs = Organization.objects.all().count()
    num_people = Person.objects.all().count()
    num_places = Location.objects.all().count()

    # Get users and the number of records they have worked on
    users = []
    tasks = Credit._meta.get_field("task").choices
    for user in User.objects.all():
        ucredit = Credit.objects.filter(user=user)
        # Only include users who have done data work (aka have at least 1 credit record)
        if ucredit.count() > 0:
            credit = [
                user.first_name + " " + user.last_name,
            ]
            # Get credit counts for each type of task
            for task in tasks:
                credit.append(ucredit.filter(task=task[0]).count())
            users.append(credit)

    # mini dictionary to pass counts in the template
    by_the_nums = {
        "num_items": num_items,
        "num_people": num_people,
        "num_orgs": num_orgs,
        "num_places": num_places,
        "users": users,
        "tasks": tasks,
    }

    return render(request, "index.html", context=by_the_nums)


def make_items_by_status_json(request):
    """Small json file with data for treemap viz based on record status (complete/incomplete/review/reviewed)"""

    num_items = Item.objects.all().count()
    est_remaining = 1000 - num_items
    all_items = {
        "name": "Probable Items",
        "children": [
            {"name": "Cataloged", "children": []},
            {"name": "Estimated Remaining", "value": est_remaining},
        ],
    }

    items_by_status = []
    for choice in Item._meta.get_field("record_status").choices:
        num_status = {
            "name": choice[1],
            "value": Item.objects.filter(record_status=choice[0]).count(),
        }
        items_by_status.append(num_status)
    all_items["children"][0]["children"] = items_by_status

    return JsonResponse(all_items)


class ItemListView(SingleTableMixin, FilterView):
    model = Item
    table_class = ItemTable
    template_name = "inventory/item_list.html"
    filterset_class = ItemFilter
    table_pagination = {"per_page": 25}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_records"] = self.model.objects.count()
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "inventory/item_detail.html"

    def get(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            item = self.get_object()
            data = {
                "accession_number": item.accession_number,
                "title": item.title,
                "pub_date": str(item.pub_date),
                "tgm_genre": str(item.tgm_genre),
                "physical_description": item.physical_description,
                "condition_notes": item.condition_notes,
                "pub_places": [str(place) for place in item.pub_places.all()],
                "creators": [
                    f"{ic.person or ic.organization} ({ic.role})"
                    for ic in item.item_creator_set.all()
                ],
                "original_source": str(item.original_source),
                "record_status": item.record_status,
            }
            return JsonResponse(data)
        return super().get(request, *args, **kwargs)


@login_required
@user_passes_test(lambda u: u.is_staff)
def export_full_dataset(request):
    """
    Export all data from all models in a single XLSX file with multiple sheets.
    Only accessible to staff users.
    """
    resource = FullDatasetResource()

    # Create response with XLSX content
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="full_dataset_export.xlsx"'
        },
    )

    # Generate the export data directly
    export_data = resource.generate_full_export()
    response.write(export_data)

    return response
