"""Small server-side client for Google Places Nearby Search (New)."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ENDPOINT = "https://places.googleapis.com/v1/places:searchNearby"
FIELD_MASK = (
    "places.displayName,places.formattedAddress,places.googleMapsUri,"
    "places.rating,places.userRatingCount,places.attributions"
)


class PlacesUnavailable(Exception):
    """A provider failure whose details must not be sent to the browser."""


def https_url(value):
    if not isinstance(value, str):
        return ""
    try:
        parsed = urlsplit(value)
        return value if parsed.scheme == "https" and parsed.netloc else ""
    except ValueError:
        return ""


def search_hospitals(latitude, longitude, radius, api_key):
    payload = {
        "includedTypes": ["hospital"],
        "maxResultCount": 6,
        "rankPreference": "DISTANCE",
        "languageCode": "en",
        "locationRestriction": {"circle": {
            "center": {"latitude": latitude, "longitude": longitude},
            "radius": radius,
        }},
    }
    request = Request(ENDPOINT, data=json.dumps(payload).encode(), method="POST", headers={
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    })
    try:
        with urlopen(request, timeout=10) as response:
            result = json.load(response)
        hospitals = []
        for place in result.get("places", []):
            hospitals.append({
                "name": place.get("displayName", {}).get("text", "Hospital"),
                "address": place.get("formattedAddress", "Address unavailable"),
                "maps_url": https_url(place.get("googleMapsUri")),
                "rating": place.get("rating"),
                "rating_count": place.get("userRatingCount", 0),
                "attributions": [{
                    "name": item.get("provider", ""),
                    "url": https_url(item.get("providerUri")),
                } for item in place.get("attributions", [])],
            })
        return hospitals
    except (HTTPError, URLError, OSError, ValueError, TypeError, AttributeError) as exc:
        raise PlacesUnavailable from exc
