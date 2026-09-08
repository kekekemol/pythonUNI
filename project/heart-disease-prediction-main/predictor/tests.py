import json
from unittest.mock import patch
from urllib.error import HTTPError

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .places import PlacesUnavailable, search_hospitals


@override_settings(GOOGLE_PLACES_API_KEY="test-key")
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
    def test_invalid_locations_never_call_google(self, provider):
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

    @override_settings(GOOGLE_PLACES_API_KEY="")
    @patch("predictor.views.search_hospitals")
    def test_missing_key_has_fallback_and_no_external_call(self, provider):
        self.assertEqual(self.search().status_code, 503)
        page = self.client.get(reverse("home"))
        self.assertContains(page, "Search on Google Maps")
        self.assertNotContains(page, 'id="hospital-search"')
        provider.assert_not_called()

    @patch("predictor.views.search_hospitals", return_value=[])
    def test_search_and_cooldown(self, provider):
        response = self.search()
        self.assertEqual(response.json(), {"hospitals": []})
        self.assertIn("no-store", response.headers["Cache-Control"])
        provider.assert_called_once_with(3.139, 101.6869, 10000, "test-key")
        repeated = self.search()
        self.assertEqual(repeated.status_code, 429)
        self.assertEqual(repeated.headers["Retry-After"], "10")

    @patch("predictor.views.search_hospitals", side_effect=PlacesUnavailable("secret upstream error"))
    def test_provider_failure_is_safe(self, provider):
        response = self.search()
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("secret", response.content.decode())

    @patch("predictor.views.search_hospitals", return_value=[])
    def test_csrf_is_required_and_key_is_not_in_page(self, provider):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        page = client.get(reverse("home"))
        self.assertContains(page, 'id="hospital-search"')
        self.assertNotContains(page, "test-key")
        self.assertEqual(client.post(self.url, self.location, content_type="application/json").status_code, 403)
        response = client.post(self.url, self.location, content_type="application/json",
                               HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value)
        self.assertEqual(response.status_code, 200)

    @patch("predictor.places.urlopen")
    def test_google_request_and_response_mapping(self, opening):
        opening.return_value.__enter__.return_value.read.return_value = json.dumps({"places": [{
            "displayName": {"text": "Example Hospital"}, "formattedAddress": "Example address",
            "googleMapsUri": "https://maps.google.com/?cid=1", "rating": 4.4,
            "userRatingCount": 12,
            "attributions": [{"provider": "Example source", "providerUri": "https://example.com"}],
        }, {"googleMapsUri": "javascript:alert(1)"}]}).encode()
        hospitals = search_hospitals(3.139, 101.6869, 10000, "test-key")
        self.assertEqual(hospitals[0]["name"], "Example Hospital")
        self.assertEqual(hospitals[0]["rating"], 4.4)
        self.assertEqual(hospitals[0]["attributions"][0]["name"], "Example source")
        self.assertEqual(hospitals[1]["maps_url"], "")
        request = opening.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(body["includedTypes"], ["hospital"])
        self.assertEqual(body["rankPreference"], "DISTANCE")
        self.assertEqual(body["locationRestriction"]["circle"]["radius"], 10000)
        self.assertEqual(request.get_header("X-goog-api-key"), "test-key")
        self.assertEqual(opening.call_args.kwargs["timeout"], 10)

    @patch("predictor.places.urlopen")
    def test_provider_timeout_bad_json_and_http_error(self, opening):
        for error in (TimeoutError(), HTTPError("https://example.com", 403, "denied", {}, None)):
            opening.side_effect = error
            with self.assertRaises(PlacesUnavailable):
                search_hospitals(0, 0, 5000, "test-key")
        opening.side_effect = None
        opening.return_value.__enter__.return_value.read.return_value = b"not JSON"
        with self.assertRaises(PlacesUnavailable):
            search_hospitals(0, 0, 5000, "test-key")
