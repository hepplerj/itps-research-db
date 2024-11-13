# places/utils.py
from time import sleep
from typing import Optional, Tuple

from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim


class LocationProcessor:
    def __init__(self):
        self.geocoder = Nominatim(user_agent="itps_research_db")

    def parse_location_string(self, location_str: str) -> Tuple[str, Optional[str]]:
        """Parse a location string into city and state."""
        if "," not in location_str:
            return location_str.strip(), None

        city, state = [part.strip() for part in location_str.split(",", 1)]
        return city, state

    def get_location_details(
        self, city: str, state: str = None, max_retries: int = 3
    ) -> Optional[dict]:
        """Get location details using Nominatim."""
        query = f"{city}, {state}" if state else city

        for attempt in range(max_retries):
            try:
                location = self.geocoder.geocode(
                    query, exactly_one=True, addressdetails=True
                )

                if location:
                    # Extract state from address components if not provided
                    address = location.raw.get("address", {})
                    derived_state = (
                        address.get("state")
                        or address.get("territory")
                        or address.get("province")
                    )

                    return {
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "state": state or derived_state,
                        "geoname_url": f"https://www.geonames.org/search.html?q={city}+{derived_state or state}",
                        "found_city": address.get("city")
                        or address.get("town")
                        or address.get("village")
                        or city,
                    }

            except (GeocoderTimedOut, GeocoderUnavailable):
                if attempt == max_retries - 1:
                    return None
                sleep(1)  # Wait before retrying

        return None

    def standardize_state_name(self, state_name: str) -> str:
        """Convert state abbreviations to full names and standardize format."""
        STATE_MAPPING = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
        }

        state_name = state_name.strip()
        if state_name.upper() in STATE_MAPPING:
            return STATE_MAPPING[state_name.upper()]
        return state_name
