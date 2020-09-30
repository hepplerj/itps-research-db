from django.db import models

#This is a stub record based off the initial inventory
class Organization(models.Model):
	name = models.CharField(max_length=765)
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name
