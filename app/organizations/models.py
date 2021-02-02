from django.db import models
from places.models import Location
from people.models import Person


class Organization(models.Model):
    name = models.CharField(max_length=100)
    start_year = models.PositiveSmallIntegerField(blank=True, null=True)
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    main_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    viaf = models.URLField(max_length=100, blank=True, null=True)
    wikipedia = models.URLField(max_length=100, blank=True, null=True)
    org_bio = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    year_joined = models.PositiveSmallIntegerField(blank=True, null=True)
    year_left = models.PositiveSmallIntegerField(blank=True, null=True)
    role = models.CharField(max_length=75, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.person, self.organization)
