from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse


from inventory.models import Item, Credit
from organizations.models import Organization
from people.models import Person
from places.models import Location, State
from django.contrib.auth.models import User

# Views for the Inventory Module, includes site homepage


def index(request):
    """View function for home page."""

    # Generate counts of some of the main objects
    num_items = Item.objects.all().count()
    num_orgs = Organization.objects.all().count()
    num_people = Person.objects.all().count()
    num_places = Location.objects.all().count()

    # Get users and the number of records they have worked on
    users = []
    tasks = Credit._meta.get_field('task').choices
    for user in User.objects.all():
        ucredit = Credit.objects.filter(user=user)
        # Only include users who have done data work (aka have at least 1 credit record)
        if ucredit.count() > 0:
            credit = [user.first_name + " " + user.last_name, ]
            # Get credit counts for each type of task
            for task in tasks:
                credit.append(ucredit.filter(task=task[0]).count())
            users.append(credit)

    # mini dictionary to pass counts in the template
    by_the_nums = {
        'num_items': num_items,
        'num_people': num_people,
        'num_orgs': num_orgs,
        'num_places': num_places,
        'users': users,
        'tasks': tasks,
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


# def make_credits_by_user_json(request):
#     """Small json file with data showing which users have worked on which records"""

#     user_credits = []
#     for user in User.objects.all():
#         if Credit.objects.filter(user=user).count() > 0:
#             user_credit = {
#                 "name": user.first_name + " " + user.last_name,
#                 "item records": []
#             }
#             records = []
#             for choice in Credit._meta.get_field('task').choices:
#                 credits = {
#                     "task": choice[1],
#                     "value": Credit.objects.filter(user=user).filter(task=choice[0]).count()
#                 }
#                 records.append(credits)
#             user_credit['records'] = records
#             user_credits.append(user_credit)

#     return JsonResponse(user_credits, safe=False)
