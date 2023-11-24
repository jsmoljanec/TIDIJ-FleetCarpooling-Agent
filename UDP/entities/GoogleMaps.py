import googlemaps
from datetime import datetime
from dotenv import load_dotenv
import os
import polyline


class GoogleMapsAPI:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        self.gmaps = googlemaps.Client(key=self.api_key)

    def get_directions(self, origin, destination, mode="transit"):
        now = datetime.now()

        directions_result = self.gmaps.directions(origin, destination, mode=mode, departure_time=now)

        overview_polyline = directions_result[0]['overview_polyline']['points']
        decoded_coordinates = polyline.decode(overview_polyline)

        return decoded_coordinates


# maps_api = GoogleMapsAPI()
#
# origin_location = "Varaždin"
# destination_location = "Čakovec"
# mode_of_transport = "transit"
#
# coordinates = maps_api.get_directions(origin_location, destination_location, mode_of_transport)
# print(coordinates)
