# organizations/admin.py

from django.contrib import admin

from .models import Organization
from inventory.models import Item_Creator

# class Item_CreatorInline(admin.StackedInline):
#     model = Item_Creator.organization.through


class OrganizationAdmin(admin.ModelAdmin):
    # inlines = (Item_CreatorInline,)
    pass


admin.site.register(Organization, OrganizationAdmin)
