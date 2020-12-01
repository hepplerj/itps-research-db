from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from inventory.models import Item

# Serializes controlled vocab and dates from Item for use in dashboard


def items_for_wp_dashboard(request):
    json_items = serialize('json', Item.objects.all(), fields=('pub_date_certainty', 'tgm_genre', 'record_status', 'iona_holdings'), indent=4, use_natural_foreign_keys=True)
    return HttpResponse(json_items)
