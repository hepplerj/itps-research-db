from django.db import models

#this is a stub record, based off the original inventory
class Person(models.Model):
	name = models.Charfield(max-length=200)
	notes = models.Textfild(blank=true, null=true)
