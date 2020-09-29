from django.db import models

#this is a stub record, based off the original inventory
class Person(models.Model):
	name = models.CharField(max_length=765)
	notes = models.TextField(blank=True, null=True)
