# organizations/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from inventory.models import Item_Creator
from inventory.resources import MembershipResource, OrganizationResource
from places.models import Location

from .models import Membership, Organization


class Item_CreatorAdmin(admin.ModelAdmin):
    pass


class Item_CreatorInline(admin.StackedInline):
    model = Item_Creator
    extra = 1
    fieldsets = (
        (
            None,
            {
                "fields": ("item", ("role", "pseudonym"), "notes"),
                "description": "If the person had more than one role in creating this item then create a new record for each role.",
            },
        ),
        (
            "Person",
            {
                "classes": ("collapse",),
                "fields": ("person",),
                "description": "Only add an person to this record if the person was writing in a formal capacity. Ex. Benjamin Franklin writing <em><b>on behalf of</b></em> the Committee of Secret Correspondence.",
            },
        ),
    )


@admin.register(Membership)
class MembershipAdmin(ImportExportModelAdmin):
    resource_class = MembershipResource
    list_display = (
        "person",
        "organization",
        "role",
        "year_joined",
        "year_left",
        "notes",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "organization",
                    "role",
                    "year_joined",
                    "year_left",
                    "notes",
                ),
                "description": "If a person held more than 1 role in an organization, create a Membership record for each role they held.",
            },
        ),
    )


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 1
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "organization",
                    "role",
                    "year_joined",
                    "year_left",
                    "notes",
                ),
                "description": "If a person held more than 1 role in an organization, create a Membership record for each role they held.",
            },
        ),
    )


@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource
    inlines = (Item_CreatorInline, MembershipInline)
    list_display = (
        "name",
        "start_year",
        "end_year",
        "main_location",
        "org_bio",
        "notes",
    )
    search = ["name", "notes"]
    fieldsets = (
        (None, {"fields": ("name", "start_year", "end_year")}),
        (
            None,
            {
                "fields": ("main_location",),
                "description": "If the organization has multiple headquarters, record the others in the notes field.",
            },
        ),
        (
            None,
            {
                "fields": ("viaf", "wikipedia"),
                "description": "Enter the full, permanent URL.",
            },
        ),
        (
            None,
            {
                "fields": ("org_bio", "notes"),
                "description": "Short history of the organization. No more than a 2-3 paragraphs. Can include links to other resources.",
            },
        ),
    )
