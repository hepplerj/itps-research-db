from django.db import models

from places import Location

#For definition of Genres in the TGM see https://www.loc.gov/rr/print/tgm2/
class TGM_Genre(models.Model):
	name = models.Charfield(max_lenght=50)
	notes = models.Textfield(blank=True, null=True)

#List of all previous inventories
class Original_Source(models.model)
	name = models.Charfield(max_lenght=765)
	notes = models.Textfield(blank=True, null=True)

#Fields pulled almost verbatim from most recent inventory, which was design by Alexandra Montgomery
#Heavily based on MARC format a
class Item(models.Model):
	#Choice lists used in fields below
	DIGITIZATION_CHOICES = ['yes','no','maybe']
	RECORD_STATUS_CHOICES = ['complete','incomplete','review','reviewed']
	IONA_HOLDINGS_CHOICES = ['original', 'copy','original and copy']

	accession_number = models.Charfield(max_lenght=100, blank=True, null=True)
	short_title = models.Charfield(max_lenght=200)
	title = models.Textfield
	size = models.Charfield(max_length=100, blank=True, null=True)
	physical_description = models.Textfield(blank=True, null=True)
	tgm_genre = models.ForeignKey(TGM_Genre, blank=True, null=True)
	other_description = models.Textfield(blank=True, null=True)
	condition_notes = model.Charfield(max_lenght=765, blank=True, null=True)
	edition = model.Charfield(max_lenght=200, blank=True, null=True)
	original_source = models.ForeignKey(Original_Source, blank=True, null=True)
	digitization_recommendation = model.Charfield(choices=DIGITIZATION_CHOICES, blank=True, null=True)
	volume = models.Charfield(max_lenght=50, blank=True, null=True)
	number = models.Charfield(max_lenght=50, blank=True, null=True)
	record_status = models.Charfield(choices=RECORD_STATUS_CHOICES)
	iona_holdings = models.Charfield(choices=IONA_HOLDINGS_CHOICES, blank=True, null=True)
	pub_places = models.ManyToManyField(Location, blank=True, null=True)
	notes = models.Textfield(blank=True, null=True)
