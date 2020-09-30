#people/admin.py

from django.contrib import admin
from .models import Person
from inventory.models import Item_Creator

# class Item_CreatorInline(admin.StackedInline):
# 	model = Item_Creator.person.through

class PersonAdmin(admin.ModelAdmin):
	pass
	# inlines = (Item_CreatorInline,)

admin.site.register(Person, PersonAdmin)
