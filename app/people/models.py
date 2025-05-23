from django.contrib.postgres.fields import DateRangeField
from django.db import models

from places.models import State


class Person(models.Model):
    # this is awkward, use the notes field!
    GENDER_CHOICES = [
        ("man", "man"),
        ("woman", "woman"),
        ("non-binary", "non-binary"),
        ("other", "other - describe in notes field"),
        ("unknown", "unknown"),
    ]

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = DateRangeField(blank=True, null=True)
    death_date = DateRangeField(blank=True, null=True)
    gender = models.CharField(
        max_length=15, choices=GENDER_CHOICES, blank=True, null=True
    )
    home_state = models.ForeignKey(State, models.SET_NULL, blank=True, null=True)
    viaf = models.URLField(max_length=100, blank=True, null=True)
    wikipedia = models.URLField(max_length=100, blank=True, null=True)
    getty = models.URLField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
