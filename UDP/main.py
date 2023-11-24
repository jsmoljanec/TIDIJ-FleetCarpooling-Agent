import threading


from entities.GoogleMaps import GoogleMapsAPI
from entities.VehicleManager import VehicleManager

if __name__ == "__main__":
    maps_api = GoogleMapsAPI()

    origin_location = "Varaždin"
    destination_location = "Čakovec"
    mode_of_transport = "transit"

    coordinates = maps_api.get_directions(origin_location, destination_location, mode_of_transport)
    print(coordinates)

    location = {"latitude": 46.305339, "longitude": 16.336864}
    manager = VehicleManager(location, coordinates)

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    while True:
        pass