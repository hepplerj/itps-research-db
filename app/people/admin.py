# people/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from inventory.models import Creator_Role, Item_Creator
from inventory.resources import PersonResource
from organizations.models import Membership

from .models import Person


# Make Item_Creator inline
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
            "Organization",
            {
                "classes": ("collapse",),
                "fields": ("organization",),
                "description": "Only add an organization to this record if the person was writing in a formal capacity. Ex. Benjamin Franklin writing <em><b>on behalf of</b></em> the Committee of Secret Correspondence.",
            },
        ),
    )


class Creator_RoleAdmin(admin.ModelAdmin):
    pass


# Make Membership inline
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


@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    inlines = (Item_CreatorInline, MembershipInline)
    list_display = (
        "name",
        "birth_date",
        "death_date",
        "gender",
        "home_state",
        "viaf",
        "wikipedia",
        "getty",
        "notes",
    )
    list_filter = ("gender", "home_state")
    search_fields = ["name", "notes"]
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            None,
            {
                "fields": ("display_name",),
                "description": "Use for a common nickname or shortening of name. Ex. Marquis de Lafayette, as opposed to his ENTIRE name.",
            },
        ),
        (
            None,
            {
                "fields": ("birth_date", "death_date"),
                "description": "All dates are recorded in the YYYY-MM-DD format. Each date is a range.</br>The first entry is for the first possible calendar day. The second entry is for the last possible calaendar day PLUS ONE.</br><b>Examples: Enter 1800 as 1800-01-01 & 1801-01-01. Enter July 1794 as 1794-07-01 & 1794-08-01. Enter October 30, 1735 as 1735-10-30 & 1735-10-31.</b>",
            },
        ),
        (None, {"fields": ("gender",)}),
        (
            None,
            {
                "fields": ("home_state",),
                "description": "The state the person is most associated with. Ex. Andrew Jackson home_state is Tennessee, for Lafayette it is France.",
            },
        ),
        (
            "Name Authority",
            {
                "fields": ("viaf", "wikipedia", "getty"),
                "description": "Enter full, <b>permanent URL</b>, not just the id",
            },
        ),
        (None, {"fields": ("notes",)}),
    )


class Item_CreatorAdmin(admin.ModelAdmin):
    pass


class MembershipAdmin(admin.ModelAdmin):
    pass
