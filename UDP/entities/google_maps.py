import googlemaps
from datetime import datetime
from dotenv import load_dotenv
import os
import polyline


class GoogleMapsAPI:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Valid Google Maps API key is not provided. Please set the GOOGLE_MAPS_API_KEY environment variable "
                "with valid API key.")

        self.gmaps = googlemaps.Client(key=self.api_key)

    def get_directions(self, origin, destination, mode="transit"):
        try:
            now = datetime.now()

            directions_result = self.gmaps.directions(origin, destination, mode=mode, departure_time=now)

            if not directions_result:
                raise Exception("No directions found")

            overview_polyline = directions_result[0]['overview_polyline']['points']
            decoded_coordinates = polyline.decode(overview_polyline)

            return decoded_coordinates

        except Exception as e:
            print(f"Error getting directions: {e}")
            return []
