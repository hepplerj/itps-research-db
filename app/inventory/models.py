from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.urls import reverse

# Pull in central model from each of the following apps
from organizations.models import Organization
from people.models import Person
from places.models import Location

# User editable list of TGM Genres
# For definition of Genres in the TGM see https://www.loc.gov/rr/print/tgm2/


class TGM_GenreManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class TGM_Genre(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    objects = TGM_GenreManager()

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre (TGM)"
        verbose_name_plural = "Genres (TGM)"


# User editable list of all previous inventories/other sources of data for the inventory
class Original_Source(models.Model):
    name = models.CharField(max_length=765)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Earlier Inventory"
        verbose_name_plural = "Earlier Inventories"


# Fields pulled almost verbatim from most recent inventory, which was designed by Alexandra Montgomery
# Heavily based on MARC format
class Item(models.Model):
    # Choice lists used in fields below
    DATE_CERTAINTY_CHOICES = [
        (0, "undated"),
        (1, "cannot be verified"),
        (2, "uncertain"),
        (3, "possible"),
        (4, "likely"),
        (5, "verified"),
    ]
    DIGITIZATION_CHOICES = [("yes", "yes"), ("no", "no"), ("maybe", "maybe")]
    RECORD_STATUS_CHOICES = [
        ("complete", "Complete"),
        ("incomplete", "Incomplete"),
        ("review", "Review"),
        ("reviewed", "Reviewed"),
    ]
    IONA_HOLDINGS_CHOICES = [
        ("original", "original"),
        ("copy", "copy"),
        ("original_copy", "original and copy"),
    ]

    accession_number = models.CharField(max_length=100, blank=True, null=True)
    short_title = models.CharField(max_length=50)
    title = models.TextField(blank=True, null=True)
    pub_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Year",
        help_text="If only the year is known, record it here.",
    )  # For single years
    pub_year_start = models.IntegerField(blank=True, null=True)  # For year ranges
    pub_year_end = models.IntegerField(blank=True, null=True)  # For year ranges
    pub_date_descriptive = models.TextField(
        blank=True, null=True
    )  # For complex descriptions
    pub_date_decade = models.IntegerField(blank=True, null=True)
    pub_date = DateRangeField(blank=True, null=True)
    pub_date_certainty = models.SmallIntegerField(
        choices=DATE_CERTAINTY_CHOICES, default=0
    )
    size = models.CharField(max_length=100, blank=True, null=True)
    physical_description = models.TextField(blank=True, null=True)
    tgm_genre = models.ForeignKey(TGM_Genre, models.SET_NULL, blank=True, null=True)
    other_description = models.TextField(blank=True, null=True)
    condition_notes = models.CharField(max_length=765, blank=True, null=True)
    edition = models.CharField(max_length=200, blank=True, null=True)
    original_source = models.ForeignKey(
        Original_Source, models.SET_NULL, blank=True, null=True
    )
    digitization_recommendation = models.CharField(
        max_length=20, choices=DIGITIZATION_CHOICES, blank=True, null=True
    )
    volume = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=50, blank=True, null=True)
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS_CHOICES)
    iona_holdings = models.CharField(
        max_length=20, choices=IONA_HOLDINGS_CHOICES, blank=True, null=True
    )
    pub_places = models.ManyToManyField(Location, blank=True)
    oclc_permalink = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to="/images",
        blank=True,
        null=True,
        help_text="Optional. Upload an image of the item.",
    )
    image_alt_text = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    publisher = models.CharField(max_length=200, blank=True, null=True)
    single_date = models.DateField(blank=True, null=True)  # For precise single dates
    page_count = models.CharField(
        max_length=50, blank=True, null=True
    )  # For "1pg." style entries
    dimensions = models.CharField(
        max_length=50, blank=True, null=True
    )  # For "19.5x16cm" style entries

    def __str__(self):
        return self.short_title


# User editable list of Creator roles
# ex. author, editor, translator, printer, lithographer, etc


class Creator_Role(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Creator Role"


# Creators allows for an undeliminated number of people and organizations to be listed as creators
# with their associated roles.
class Item_Creator(models.Model):
    person = models.ForeignKey(Person, on_delete=models.RESTRICT, blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.RESTRICT, blank=True, null=True
    )
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    role = models.ForeignKey(Creator_Role, on_delete=models.RESTRICT)
    pseudonym = models.CharField(max_length=75, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s. %s, %s & %s" % (
            self.item,
            self.role,
            self.person,
            self.organization,
        )

    def get_absolute_url(self):
        return reverse("inventory:item_detail", args=[str(self.id)])

    class Meta:
        verbose_name = "Creator"


class Credit(models.Model):
    # Choice list used below
    TASK_CHOICES = [
        ("created", "created"),
        ("enhanced", "enhanced"),
        ("reviewed", "reviewed"),
    ]

    user = models.ForeignKey(User, models.PROTECT)
    item_record = models.ForeignKey(Item, models.PROTECT)
    task = models.CharField(max_length=20, choices=TASK_CHOICES)

    def __str__(self):
        return "%s %s %s" % (self.user, self.task, self.item_record)
