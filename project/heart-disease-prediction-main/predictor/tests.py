import json
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .places import PlacesUnavailable, search_hospitals


class HospitalFinderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="hospital-test", password="test-password")
        self.client.force_login(self.user)
        self.url = reverse("nearby_hospitals")
        self.location = {"latitude": 3.139, "longitude": 101.6869, "radius": 10000}

    def search(self, values=None):
        return self.client.post(self.url, values or self.location, content_type="application/json")

    @patch("predictor.views.search_hospitals")
    def test_authentication_and_post_required(self, provider):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.search().status_code, 401)
        provider.assert_not_called()

    @patch("predictor.views.search_hospitals")
    def test_invalid_locations_never_call_provider(self, provider):
        for values in (
            {"latitude": 91, "longitude": 0},
            {"latitude": 0, "longitude": -181},
            {"latitude": "NaN", "longitude": 0},
            {"latitude": 0, "longitude": "Infinity"},
            {"latitude": True, "longitude": 0},
            {"latitude": 0, "longitude": 0, "radius": 50001},
            {"longitude": 0},
        ):
            with self.subTest(values=values):
                self.assertEqual(self.search(values).status_code, 400)
        for body in ("{", "null", "[]", '"text"', "x" * 1025):
            self.assertEqual(self.client.post(self.url, body, content_type="application/json").status_code, 400)
        provider.assert_not_called()

    @patch("predictor.views.search_hospitals", return_value=[])
    def test_search_available_without_credentials(self, provider):
        self.assertEqual(self.search().status_code, 200)
        page = self.client.get(reverse("home"))
        self.assertContains(page, "OpenStreetMap contributors")
        self.assertContains(page, 'id="hospital-search"')
        self.assertNotContains(page, "Google Maps")

    @patch("predictor.views.search_hospitals", return_value=[])
    def test_search_and_cooldown(self, provider):
        response = self.search()
        self.assertEqual(response.json(), {"hospitals": []})
        self.assertIn("no-store", response.headers["Cache-Control"])
        provider.assert_called_once_with(3.139, 101.6869, 10000)
        repeated = self.search()
        self.assertEqual(repeated.status_code, 429)
        self.assertEqual(repeated.headers["Retry-After"], "10")

    @patch("predictor.views.search_hospitals", side_effect=PlacesUnavailable("secret upstream error"))
    def test_provider_failure_is_safe(self, provider):
        response = self.search()
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("secret", response.content.decode())

    @patch("predictor.views.search_hospitals", return_value=[])
    def test_csrf_is_required(self, provider):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        page = client.get(reverse("home"))
        self.assertContains(page, 'id="hospital-search"')
        self.assertEqual(client.post(self.url, self.location, content_type="application/json").status_code, 403)
        response = client.post(self.url, self.location, content_type="application/json",
                               HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value)
        self.assertEqual(response.status_code, 200)

    @patch("predictor.places.urlopen")
    def test_overpass_query_mapping_distance_and_deduplication(self, opening):
        near = {"type": "node", "id": 1, "lat": 0.001, "lon": 0,
                "tags": {"name": "Near Hospital", "addr:housenumber": "12",
                         "addr:street": "Example Street", "addr:city": "Test City"}}
        far = {"type": "way", "id": 2, "center": {"lat": 0.02, "lon": 0},
               "tags": {"name:en": "Far Hospital"}}
        opening.return_value.__enter__.return_value.read.return_value = json.dumps({"elements": [
            far, near, near,
            {"type": "relation", "id": 3, "center": {"lat": 0.03, "lon": 0},
             "tags": {"addr:full": "Full address"}},
            {"type": "node", "id": 4, "lat": 2, "lon": 0},  # Outside radius
            {"type": "node", "id": 5},  # No coordinates
            {"type": "node", "id": 6, "lat": "NaN", "lon": 0},
            {"type": "bad-url", "id": 7, "lat": 0, "lon": 0},
        ]}).encode()
        hospitals = search_hospitals(0, 0, 5000)
        self.assertEqual(len(hospitals), 3)
        self.assertEqual(hospitals[0]["name"], "Near Hospital")
        self.assertEqual(hospitals[0]["address"], "12 Example Street, Test City")
        self.assertAlmostEqual(hospitals[0]["distance_km"], 0.11, places=2)
        self.assertEqual(hospitals[0]["maps_url"], "https://www.openstreetmap.org/node/1")
        self.assertEqual(hospitals[1]["name"], "Far Hospital")
        self.assertIn("not listed", hospitals[1]["address"])
        self.assertEqual(hospitals[2]["address"], "Full address")
        self.assertNotIn("rating", hospitals[0])
        request = opening.call_args.args[0]
        query = parse_qs(request.data.decode())["data"][0]
        self.assertIn('nwr["amenity"="hospital"]', query)
        self.assertIn('nwr["healthcare"="hospital"]', query)
        self.assertIn("around:5000,0.000000,0.000000", query)
        self.assertEqual(request.full_url, "https://overpass-api.de/api/interpreter")
        self.assertIsNone(request.get_header("X-goog-api-key"))
        self.assertEqual(opening.call_args.kwargs["timeout"], 30)

    @patch("predictor.places.urlopen")
    def test_only_six_nearest_results_and_empty_response(self, opening):
        opening.return_value.__enter__.return_value.read.return_value = json.dumps({"elements": [
            {"type": "node", "id": i, "lat": i / 1000, "lon": 0} for i in range(9, 0, -1)
        ]}).encode()
        hospitals = search_hospitals(0, 0, 5000)
        self.assertEqual(len(hospitals), 6)
        self.assertTrue(hospitals[-1]["maps_url"].endswith("/6"))
        opening.return_value.__enter__.return_value.read.return_value = b'{"elements": []}'
        self.assertEqual(search_hospitals(0, 0, 5000), [])

    @patch("predictor.places.urlopen")
    def test_provider_timeout_bad_json_and_http_error(self, opening):
        for error in (TimeoutError(), HTTPError("https://example.com", 403, "denied", {}, None)):
            opening.side_effect = error
            with self.assertRaises(PlacesUnavailable):
                search_hospitals(0, 0, 5000)
        opening.side_effect = None
        for payload in (b"not JSON", b"null", b"{}", b'{"elements": [], "remark": "runtime error"}'):
            opening.return_value.__enter__.return_value.read.return_value = payload
            with self.assertRaises(PlacesUnavailable):
                search_hospitals(0, 0, 5000)
