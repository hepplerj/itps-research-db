# inventory/admin.py

from django.contrib import admin

from inventory.models import Item, TGM_Genre, Original_Source, Creator_Role, Item_Creator, Credit

from organizations.models import Organization
from people.models import Person
from places.models import Location


# Register Models that exist to be editable lists
admin.site.register(TGM_Genre)
admin.site.register(Original_Source)


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_filter = ('user', 'task')
    list_display = ('user', 'task', 'item_record')


# Make Credit inline
class CreditInline(admin.TabularInline):
    model = Credit
    extra = 1


@admin.register(Item_Creator)
class Item_CreatorAdmin(admin.ModelAdmin):
    pass


# Make Item_Creator inline
class Item_CreatorInline(admin.StackedInline):
    model = Item_Creator
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('person', 'organization', 'role', 'pseudonym', 'notes'),
            'description': 'If a person or organization had more than one role in creating this item then create a new record for each role.</br>Only add an organization and a person to <b>the same record</b> if the person was writing in a formal capacity.</br>Ex. Benjamin Franklin writing <em><b>on behalf of</b></em> the Committee of Secret Correspondence.'
        }),
    )


@admin.register(Creator_Role)
class Creator_RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = (Item_CreatorInline, CreditInline,)
    list_filter = ('tgm_genre', 'digitization_recommendation', 'pub_date_certainty')
    search_fields = ['title', 'other_description', 'notes']
    fieldsets = (
        (None, {
            'fields': ('accession_number', 'record_status')
        }),
        (None, {
            'fields': ('short_title', 'title'),
            'description': 'Short Title is limited to 50 characters.'
        }),
        (None, {
            'fields': ('pub_date', 'pub_date_certainty'),
            'description': 'All dates are recorded in the YYYY-MM-DD format. Each date is a range.</br>The first entry is for the first possible calendar day. The second entry is for the last possible calaendar day PLUS ONE.</br><b>Examples: Enter 1800 as 1800-01-01 & 1801-01-01. Enter July 1794 as 1794-07-01 & 1794-08-01. Enter October 30, 1735 as 1735-10-30 & 1735-10-31.</b>'
        }),
        (None, {
            'fields': ('pub_places', 'edition', 'volume', 'number')
        }),
        (None, {
            'fields': ('other_description', 'original_source', 'notes'),
            'description': 'Other Description is where you describe the content of the item. The notes field is for anything related to the record that does not fit in one of the fields above.'
        }),
        ('Physical Object', {
            'classes': ('collapse',),
            'fields': ('tgm_genre', 'size', 'physical_description', 'condition_notes', 'digitization_recommendation', 'iona_holdings')
        })
    )
    # leaving off physical descriptions for now, since all work is being done online and offsite
    list_display = ('accession_number', 'short_title', 'pub_date', 'edition', 'volume', 'number', 'other_description', 'notes')
