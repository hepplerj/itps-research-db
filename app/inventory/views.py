from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse


from inventory.models import Item
from organizations.models import Organization
from people.models import Person
from places.models import Location, State

# Views for the Inventory Module, includes site homepage


def index(request):
    """View function for home page."""

    # Generate counts of some of the main objects
    num_items = Item.objects.all().count()
    num_orgs = Organization.objects.all().count()
    num_people = Person.objects.all().count()
    num_places = Location.objects.all().count()

    # mini dictionary to pass counts in the template
    by_the_nums = {
        'num_items': num_items,
        'num_people': num_people,
        'num_orgs': num_orgs,
        'num_places': num_places,
    }

    return render(request, 'index.html', context=by_the_nums)


def make_items_by_status_json(request):
    """Small json file with data for treemap viz based on record status (complete/incomplete/review/reviewed)"""

    num_items = Item.objects.all().count()
    est_remaining = 1000 - num_items
    all_items = {
        "name": "Probable Items",
        "children": [
            {
                "name": "Cataloged",
                "children": []
            },
            {
                "name": "Estimated Remaining",
                "value": est_remaining
            }
        ]
    }

    items_by_status = []
    for choice in Item._meta.get_field('record_status').choices:
        num_status = {
            "name": choice[1],
            "value": Item.objects.filter(record_status=choice[0]).count()
        }
        items_by_status.append(num_status)
    all_items['children'][0]['children'] = items_by_status

    return JsonResponse(all_items)
