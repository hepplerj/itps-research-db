from django.db import models

# This is a stub record based off the original inventory


class Region(models.Model):
    name = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class State(models.Model):
    CONTINENT_CHOICES = [
        ("North America", "North America"),
        ("South America", "South America"),
        ("Europe", "Europe"),
        ("Africa", "Africa"),
        ("Asia", "Asia")
    ]

    name = models.CharField(max_length=75)
    continent = models.CharField(max_length=25, choices=CONTINENT_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    geoname = models.URLField(max_length=100, blank=True, null=True)
    regions = models.ManyToManyField(Region, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Empire(models.Model):
    name = models.CharField(max_length=20)
    claims = models.ManyToManyField(State, through='Claim', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Claim(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    empire = models.ForeignKey(Empire, on_delete=models.CASCADE)
    start_year = models.PositiveSmallIntegerField(blank=True, null=True)
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s (%d - %d)' % (self.empire, self.state, self.start_year, self.end_year)
