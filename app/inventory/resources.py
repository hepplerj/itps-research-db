from django.contrib.auth.models import User
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from organizations.models import Membership, Organization
from people.models import Person
from places.models import Claim, Empire, Location, Region, State

from .models import Creator_Role, Credit, Item, Item_Creator, Original_Source, TGM_Genre


class TGMGenreResource(resources.ModelResource):
    class Meta:
        model = TGM_Genre
        fields = ("id", "name", "notes")
        export_order = ("id", "name", "notes")


class OriginalSourceResource(resources.ModelResource):
    class Meta:
        model = Original_Source
        fields = ("id", "name", "notes")
        export_order = ("id", "name", "notes")


class CreatorRoleResource(resources.ModelResource):
    class Meta:
        model = Creator_Role
        fields = ("id", "name", "notes")
        export_order = ("id", "name", "notes")


class StateResource(resources.ModelResource):
    class Meta:
        model = State
        fields = ("id", "name", "continent", "notes")
        export_order = ("id", "name", "continent", "notes")


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = ("id", "name", "notes")
        export_order = ("id", "name", "notes")


class LocationResource(resources.ModelResource):
    state = fields.Field(
        column_name="state", attribute="state", widget=ForeignKeyWidget(State, "name")
    )
    regions = fields.Field(
        column_name="regions",
        attribute="regions",
        widget=ManyToManyWidget(Region, field="name", separator=", "),
    )

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "state",
            "latitude",
            "longitude",
            "geoname",
            "regions",
            "notes",
        )
        export_order = (
            "id",
            "name",
            "state",
            "latitude",
            "longitude",
            "geoname",
            "regions",
            "notes",
        )


class EmpireResource(resources.ModelResource):
    class Meta:
        model = Empire
        fields = ("id", "name", "notes")
        export_order = ("id", "name", "notes")


class ClaimResource(resources.ModelResource):
    state = fields.Field(
        column_name="state", attribute="state", widget=ForeignKeyWidget(State, "name")
    )
    empire = fields.Field(
        column_name="empire",
        attribute="empire",
        widget=ForeignKeyWidget(Empire, "name"),
    )

    class Meta:
        model = Claim
        fields = ("id", "state", "empire", "start_year", "end_year", "notes")
        export_order = ("id", "state", "empire", "start_year", "end_year", "notes")


class PersonResource(resources.ModelResource):
    home_state = fields.Field(
        column_name="home_state",
        attribute="home_state",
        widget=ForeignKeyWidget(State, "name"),
    )

    class Meta:
        model = Person
        fields = (
            "id",
            "name",
            "display_name",
            "birth_date",
            "death_date",
            "gender",
            "home_state",
            "viaf",
            "wikipedia",
            "getty",
            "notes",
        )
        export_order = (
            "id",
            "name",
            "display_name",
            "birth_date",
            "death_date",
            "gender",
            "home_state",
            "viaf",
            "wikipedia",
            "getty",
            "notes",
        )


class OrganizationResource(resources.ModelResource):
    main_location = fields.Field(
        column_name="main_location",
        attribute="main_location",
        widget=ForeignKeyWidget(Location, "name"),
    )

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "start_year",
            "end_year",
            "main_location",
            "viaf",
            "wikipedia",
            "org_bio",
            "notes",
        )
        export_order = (
            "id",
            "name",
            "start_year",
            "end_year",
            "main_location",
            "viaf",
            "wikipedia",
            "org_bio",
            "notes",
        )


class MembershipResource(resources.ModelResource):
    person = fields.Field(
        column_name="person",
        attribute="person",
        widget=ForeignKeyWidget(Person, "name"),
    )
    organization = fields.Field(
        column_name="organization",
        attribute="organization",
        widget=ForeignKeyWidget(Organization, "name"),
    )

    class Meta:
        model = Membership
        fields = (
            "id",
            "person",
            "organization",
            "year_joined",
            "year_left",
            "role",
            "notes",
        )
        export_order = (
            "id",
            "person",
            "organization",
            "year_joined",
            "year_left",
            "role",
            "notes",
        )


class ItemResource(resources.ModelResource):
    tgm_genre = fields.Field(
        column_name="tgm_genre",
        attribute="tgm_genre",
        widget=ForeignKeyWidget(TGM_Genre, "name"),
    )
    original_source = fields.Field(
        column_name="original_source",
        attribute="original_source",
        widget=ForeignKeyWidget(Original_Source, "name"),
    )
    pub_places = fields.Field(
        column_name="pub_places",
        attribute="pub_places",
        widget=ManyToManyWidget(Location, field="name", separator=", "),
    )

    class Meta:
        model = Item
        fields = (
            "id",
            "accession_number",
            "short_title",
            "title",
            "pub_year",
            "pub_year_start",
            "pub_year_end",
            "pub_date_descriptive",
            "pub_date_decade",
            "pub_date",
            "pub_date_certainty",
            "size",
            "physical_description",
            "tgm_genre",
            "other_description",
            "condition_notes",
            "edition",
            "original_source",
            "digitization_recommendation",
            "volume",
            "number",
            "record_status",
            "iona_holdings",
            "pub_places",
            "oclc_permalink",
            "image",
            "image_alt_text",
            "notes",
            "publisher",
            "single_date",
            "page_count",
            "dimensions",
        )
        export_order = (
            "id",
            "accession_number",
            "short_title",
            "title",
            "pub_date",
            "pub_date_certainty",
            "pub_year",
            "pub_year_start",
            "pub_year_end",
            "pub_date_descriptive",
            "pub_date_decade",
            "tgm_genre",
            "size",
            "physical_description",
            "other_description",
            "condition_notes",
            "edition",
            "volume",
            "number",
            "publisher",
            "pub_places",
            "oclc_permalink",
            "original_source",
            "digitization_recommendation",
            "iona_holdings",
            "record_status",
            "notes",
            "single_date",
            "page_count",
            "dimensions",
            "image",
            "image_alt_text",
        )


class ItemCreatorResource(resources.ModelResource):
    person = fields.Field(
        column_name="person",
        attribute="person",
        widget=ForeignKeyWidget(Person, "name"),
    )
    organization = fields.Field(
        column_name="organization",
        attribute="organization",
        widget=ForeignKeyWidget(Organization, "name"),
    )
    item = fields.Field(
        column_name="item",
        attribute="item",
        widget=ForeignKeyWidget(Item, "short_title"),
    )
    role = fields.Field(
        column_name="role",
        attribute="role",
        widget=ForeignKeyWidget(Creator_Role, "name"),
    )

    class Meta:
        model = Item_Creator
        fields = ("id", "person", "organization", "item", "role", "pseudonym", "notes")
        export_order = (
            "id",
            "item",
            "person",
            "organization",
            "role",
            "pseudonym",
            "notes",
        )


class CreditResource(resources.ModelResource):
    user = fields.Field(
        column_name="user", attribute="user", widget=ForeignKeyWidget(User, "username")
    )
    item_record = fields.Field(
        column_name="item_record",
        attribute="item_record",
        widget=ForeignKeyWidget(Item, "short_title"),
    )

    class Meta:
        model = Credit
        fields = ("id", "user", "item_record", "task")
        export_order = ("id", "user", "item_record", "task")


# Combined dataset for exporting all related data
class FullDatasetResource(resources.Resource):
    """
    A resource for exporting all data from all models in a single workbook with multiple sheets.
    This is not tied to a specific model, but rather creates a workbook with one sheet per model.
    """

    class Meta:
        title = "Full Dataset Export"

    def generate_full_export(self):
        """
        Method to generate a complete export of all models as an Excel file.
        """
        from io import BytesIO

        import xlsxwriter

        # Create a workbook
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Define header format
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#D3D3D3", "border": 1}
        )

        # Define all resources to export
        resources_to_export = [
            ("Items", ItemResource()),
            ("Item_Creators", ItemCreatorResource()),
            ("Credits", CreditResource()),
            ("TGM_Genres", TGMGenreResource()),
            ("Creator_Roles", CreatorRoleResource()),
            ("Original_Sources", OriginalSourceResource()),
            ("People", PersonResource()),
            ("Organizations", OrganizationResource()),
            ("Memberships", MembershipResource()),
            ("Locations", LocationResource()),
            ("States", StateResource()),
            ("Regions", RegionResource()),
            ("Empires", EmpireResource()),
            ("Claims", ClaimResource()),
        ]

        # Create a sheet for each resource
        for sheet_name, resource in resources_to_export:
            try:
                # Get all objects for this resource
                qs = resource._meta.model.objects.all()
                if not qs.exists():
                    continue  # Skip empty models

                # Get export data
                dataset = resource.export(qs)

                # Clean sheet name (max 31 chars for Excel)
                sheet_name = sheet_name[:31]

                # Create sheet and write headers
                worksheet = workbook.add_worksheet(sheet_name)
                for col_idx, header in enumerate(dataset.headers):
                    worksheet.write(0, col_idx, header, header_format)
                    worksheet.set_column(col_idx, col_idx, max(len(header) * 1.2, 10))

                # Write data rows
                for row_idx, row in enumerate(dataset):
                    for col_idx, cell_value in enumerate(row):
                        # Format the cell value for display
                        if cell_value is None:
                            cell_value = ""
                        worksheet.write(row_idx + 1, col_idx, cell_value)
            except Exception as e:
                # If there's an error with one model, log it and continue with others
                print(f"Error exporting {sheet_name}: {str(e)}")
                error_sheet = workbook.add_worksheet(f"{sheet_name}_ERROR")
                error_sheet.write(0, 0, f"Error exporting: {str(e)}")

        # Close the workbook and return the data
        workbook.close()
        output.seek(0)
        return output.read()
