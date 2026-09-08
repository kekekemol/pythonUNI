"""Hospital lookup on the free public Overpass API (OpenStreetMap data)."""
import json
import math
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = "https://overpass-api.de/api/interpreter"


class PlacesUnavailable(Exception):
    """A provider failure whose details must not be sent to the browser."""


def distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance, not road/driving distance."""
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(min(1, max(0, a))))


def search_hospitals(latitude, longitude, radius):
    # Format numeric values only; never interpolate raw request text into QL.
    area = f"around:{float(radius):.0f},{float(latitude):.6f},{float(longitude):.6f}"
    query = (
        '[out:json][timeout:20];('
        f'nwr["amenity"="hospital"]({area});'
        f'nwr["healthcare"="hospital"]({area});'
        ');out center tags;'
    )
    request = Request(ENDPOINT, data=urlencode({"data": query}).encode(), method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "HeartSense-Coursework/1.0 (nearby hospital lookup)",
        "Accept": "application/json",
    })
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
        # Overpass can return HTTP 200 with a runtime error and partial data.
        if result.get("remark") or not isinstance(result.get("elements"), list):
            raise PlacesUnavailable
        hospitals = []
        seen = set()
        for place in result["elements"]:
            if not isinstance(place, dict):
                continue
            kind, osm_id = place.get("type"), place.get("id")
            if kind not in ("node", "way", "relation") or type(osm_id) is not int:
                continue
            if (kind, osm_id) in seen:
                continue
            seen.add((kind, osm_id))
            tags = place.get("tags") or {}
            point = place if kind == "node" else (place.get("center") or {})
            try:
                lat, lon = float(point["lat"]), float(point["lon"])
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue
                distance = distance_km(latitude, longitude, lat, lon)
            except (KeyError, TypeError, ValueError):
                continue
            if distance * 1000 > radius:
                continue
            street = " ".join(filter(None, [tags.get("addr:housenumber"), tags.get("addr:street")]))
            address = tags.get("addr:full") or ", ".join(filter(None, [
                street, tags.get("addr:suburb"), tags.get("addr:city"),
                tags.get("addr:postcode"), tags.get("addr:state"),
            ]))
            hospitals.append({
                "name": tags.get("name") or tags.get("name:en") or "Unnamed hospital",
                "address": address or "Address not listed in OpenStreetMap",
                "maps_url": f"https://www.openstreetmap.org/{kind}/{osm_id}",
                "distance_km": distance,
            })
        hospitals.sort(key=lambda hospital: hospital["distance_km"])
        for hospital in hospitals:
            hospital["distance_km"] = round(hospital["distance_km"], 2)
        return hospitals[:6]
    except (HTTPError, URLError, OSError, ValueError, TypeError, AttributeError) as exc:
        raise PlacesUnavailable from exc
