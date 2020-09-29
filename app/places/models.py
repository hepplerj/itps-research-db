from django.db import models

#This is a stub record based off the original inventory
class Location(models.Model):
	name = models.CharField(max_length=765)
	notes = models.TextField(blank=True, null=True)
