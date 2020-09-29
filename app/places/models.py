from django.db import models

#This is a stub record based off the original inventory
class Location(models.Model):
	name = models.Charfield(max-length=200)
	notes = models.Textfild(blank=true, null=true)
