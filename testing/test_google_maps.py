import unittest

from UDP.entities.google.google_maps import GoogleMapsAPI


class GoogleMapsAPITest(unittest.TestCase):
    google_maps_api = GoogleMapsAPI()

    def test_get_directions_with_valid_directions_returns_list_of_coordinates(self):
        origin = "Varaždin"
        destination = "Čakovec"
        result = self.google_maps_api.get_directions(origin, destination)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_directions_with_invalid_directions_returns_empty_list(self):
        origin = "Njinjinjinjinjini"
        destination = "Mkimkimkimki"
        result = self.google_maps_api.get_directions(origin, destination)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) == 0)
