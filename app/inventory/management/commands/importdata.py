import csv
from datetime import datetime
from typing import Optional

from django.core.management.base import BaseCommand
from django.db import connections, transaction
from psycopg2.extras import DateRange

from inventory.models import (
    Creator_Role,
    Item,
    Item_Creator,
    Original_Source,
    TGM_Genre,
)
from people.models import Person
from places.models import Location


class Command(BaseCommand):
    help = "Import inventory items from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the import without saving to database",
        )

    def parse_date_info(self, date_str):
        """Parse date string into appropriate fields."""
        if not date_str:
            return {"pub_date_certainty": 0}  # undated

        date_str = date_str.strip()
        result = {}

        # Set initial certainty based on presence of question mark
        if "?" in date_str:
            result["pub_date_certainty"] = 2  # uncertain
            date_str = date_str.replace("?", "").strip()
        else:
            result["pub_date_certainty"] = 4  # likely

        # Handle "N.D." and similar
        if date_str.upper().startswith("N.D.") or date_str.upper().startswith("N "):
            result["pub_date_certainty"] = 1  # cannot be verified
            result["pub_date_descriptive"] = date_str
            return result

        # Handle single years (most common case)
        if date_str.isdigit() and len(date_str) == 4:
            return {
                "pub_year": int(date_str),
                "pub_date_certainty": result.get("pub_date_certainty", 4),
            }

        # Handle decade references
        if date_str.endswith("s"):
            decade_str = date_str.replace("s", "").strip()
            if decade_str.isdigit() and len(decade_str) == 4:
                return {
                    "pub_date_decade": int(decade_str),
                    "pub_date_certainty": result.get(
                        "pub_date_certainty", 3
                    ),  # possible
                }

        # Handle year ranges with various separators
        for separator in ["/", "-"]:
            if separator in date_str:
                parts = date_str.split(separator)
                if len(parts) == 2:
                    try:
                        start = int("".join(c for c in parts[0] if c.isdigit()))
                        end = int("".join(c for c in parts[1] if c.isdigit()))
                        if 1000 <= start <= 9999 and 1000 <= end <= 9999:
                            return {
                                "pub_year_start": start,
                                "pub_year_end": end,
                                "pub_date_certainty": result.get(
                                    "pub_date_certainty", 3
                                ),  # possible
                            }
                    except ValueError:
                        pass

        # Handle full dates
        try:
            # Try different date formats for precise dates
            for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%B %Y"]:
                try:
                    date = datetime.strptime(date_str, fmt).date()
                    result["pub_date_range"] = DateRange(lower=date, upper=date)
                    result["pub_date_certainty"] = (
                        5  # verified (since we have a specific date)
                    )
                    return result
                except ValueError:
                    continue
        except Exception:
            pass

        # If nothing else matches, store as descriptive text with lower certainty
        result["pub_date_descriptive"] = date_str
        if "pub_date_certainty" not in result:
            result["pub_date_certainty"] = 1  # cannot be verified

        return result

    def process_location(self, place_name: str) -> Optional[Location]:
        """Process a location string and create or update Location record."""
        if not place_name:
            return None

        # Create location (save method will handle enrichment)
        location, created = Location.objects.get_or_create(name=place_name)

        if created:
            self.stdout.write(f"Created new location: {location}")

        return location

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.stats = {"processed": 0, "created": 0, "errors": 0, "skipped": 0}

        try:
            # Verify database is empty or has existing records
            initial_count = Item.objects.count()
            self.stdout.write(f"Initial item count: {initial_count}")

            with open(options["csv_file"], "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                # Process all rows in a single transaction
                with transaction.atomic():
                    for row in reader:
                        try:
                            self.process_row(row)
                        except Exception as e:
                            self.stats["errors"] += 1
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Error processing row {self.stats['processed'] + 1}: {str(e)}"
                                )
                            )
                            raise  # Re-raise to roll back the transaction

            # Verify final count
            final_count = Item.objects.count()
            self.stdout.write(f"Final item count: {final_count}")
            self.stdout.write(f"Items added: {final_count - initial_count}")

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"File not found: {options['csv_file']}")
            )
            return

        # Print summary
        self.print_summary()

    def process_row(self, row):
        """Process a single row from the CSV."""
        self.stats["processed"] += 1

        if self.dry_run:
            self.stdout.write(f"Would process: {row['Accession Number']}")
            return

        # Get or create Genre
        genre = None
        if row["Genre"]:
            genre, genre_created = TGM_Genre.objects.get_or_create(name=row["Genre"])
            if genre_created:
                self.stdout.write(f"Created new genre: {genre.name}")

        # Get or create Original Source
        original_source = None
        if row.get("Original source"):
            original_source, source_created = Original_Source.objects.get_or_create(
                name=row["Original source"]
            )
            if source_created:
                self.stdout.write(f"Created new source: {original_source.name}")

        # Parse date
        date_info = self.parse_date_info(row["Date"])

        # Create Item
        item = Item.objects.create(
            accession_number=row["Accession Number"],
            short_title=row["Title"][:50],
            title=row["Title"],
            pub_date=date_info.get("pub_date_range"),
            pub_date_certainty=date_info.get("pub_date_certainty", 0),
            size=row.get("Size"),
            physical_description=row.get("Physical Description"),
            tgm_genre=genre,
            other_description=row.get("Other Description"),
            condition_notes=row.get("Condition notes"),
            original_source=original_source,
            digitization_recommendation=(
                row.get("Digitization Recommendation", "").lower()
                if row.get("Digitization Recommendation")
                else None
            ),
            volume=row.get("Volume"),
            number=row.get("Number"),
            record_status="incomplete",
            iona_holdings=(
                row.get("Iona Holdings", "").lower()
                if row.get("Iona Holdings")
                else None
            ),
            notes=row.get("Notes"),
        )

        self.stdout.write(f"Created item: {item.accession_number}")

        # Process publication places
        if row.get("Place of Publication"):
            places = [place.strip() for place in row["Place of Publication"].split(";")]
            for place_name in places:
                if place_name:
                    location = self.process_location(place_name)
                    if location:
                        item.pub_places.add(location)

        # Process creators
        if row.get("Creator"):
            creators = [creator.strip() for creator in row["Creator"].split(";")]
            for creator_name in creators:
                if creator_name:
                    person, _ = Person.objects.get_or_create(name=creator_name)
                    role, _ = Creator_Role.objects.get_or_create(name="author")
                    Item_Creator.objects.create(item=item, person=person, role=role)

        self.stats["created"] += 1

        if self.stats["processed"] % 100 == 0:
            self.stdout.write(f"Processed {self.stats['processed']} rows...")

    def print_summary(self):
        """Print import summary statistics."""
        self.stdout.write("\nImport Summary:")
        self.stdout.write(f"Total rows processed: {self.stats['processed']}")
        self.stdout.write(f"Items created: {self.stats['created']}")
        self.stdout.write(f"Errors encountered: {self.stats['errors']}")
        self.stdout.write(f"Rows skipped: {self.stats['skipped']}")

        if self.dry_run:
            self.stdout.write("\nThis was a dry run - no data was actually imported.")
