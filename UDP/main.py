import threading
from entities.google_maps import GoogleMapsAPI
from entities.vehicle_manager import VehicleManager

if __name__ == "__main__":
    maps_api = GoogleMapsAPI()

    origin_location = "Varaždin"
    destination_location = "Čakovec"
    mode_of_transport = "driving"

    coordinates = maps_api.get_directions(origin_location, destination_location, mode_of_transport)
    print(coordinates)

    manager = VehicleManager(coordinates)

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    while True:
        pass