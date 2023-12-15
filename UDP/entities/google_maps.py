import googlemaps
import os
import polyline
from datetime import datetime
from dotenv import load_dotenv
from .strings import Strings


class GoogleMapsAPI:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if not self.api_key:
            raise ValueError(Strings.ERROR_GOOGLE_MAPS_API_KEY)

        self.gmaps = googlemaps.Client(key=self.api_key)

    def get_directions(self, origin, destination, mode="transit"):
        try:
            now = datetime.now()

            directions_result = self.gmaps.directions(origin, destination, mode=mode, departure_time=now)

            if not directions_result:
                raise Exception(Strings.ERROR_GOOGLE_MAPS_ROUTE)

            overview_polyline = directions_result[0]['overview_polyline']['points']
            decoded_coordinates = polyline.decode(overview_polyline)

            return decoded_coordinates

        except Exception as e:
            print(f"Error getting directions: {e}")
            return []
