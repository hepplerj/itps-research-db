from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import LocationProcessor


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
        ("Asia", "Asia"),
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
    regions = models.ManyToManyField(Region, blank=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, skip_geocoding=False, **kwargs):
        if not skip_geocoding and (
            not self.latitude or not self.longitude or not self.state
        ):
            try:
                processor = LocationProcessor()
                city, state_name = processor.parse_location_string(self.name)

                if state_name:
                    state_name = processor.standardize_state_name(state_name)

                details = processor.get_location_details(city, state_name)

                if details:
                    self.latitude = details["latitude"]
                    self.longitude = details["longitude"]
                    self.geoname = details["geoname_url"]

                    if details["state"]:
                        state_name = processor.standardize_state_name(details["state"])
                        state, _ = State.objects.get_or_create(
                            name=state_name, defaults={"continent": "North America"}
                        )
                        self.state = state
            except Exception as e:
                print(f"Geocoding failed for {self.name}: {str(e)}")
                # Continue without geocoding
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        if self.state:
            return f"{self.name}, {self.state.name}"
        return self.name


class Empire(models.Model):
    name = models.CharField(max_length=75)
    claims = models.ManyToManyField(State, through="Claim", blank=True)
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
        return "%s %s (%s - %s)" % (
            self.empire,
            self.state,
            str(self.start_year),
            str(self.end_year),
        )
