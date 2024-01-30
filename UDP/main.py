import sys
import threading

from UDP.entities.utilities.logging_utils import LoggingUtils
from UDP.entities.vehicle.vehicle_data_manager import VehicleDataManager
from UDP.entities.vehicle.vehicle_manager import VehicleManager
import os

from dotenv import load_dotenv

from UDP.entities.google.firebase.firebase_admin_manager import FirebaseAdminManager
from UDP.entities.google.google_maps import GoogleMapsAPI
from UDP.entities.vehicle.vehicle_statistics import VehicleStatistics
from entities.udp_server import UDPServer
from UDP.entities.utilities.strings import Strings

if __name__ == "__main__":
    load_dotenv("entities/.env")
    firebase_credentials_path = os.getenv("CREDENTIALS_PATH")
    firebase_database_url = os.getenv("DATABASE_URL")

    host = '127.0.0.1' if len(sys.argv) == 1 else sys.argv[1]
    port = 50001
    udp_server = UDPServer(host, port)
    firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
    maps_api = GoogleMapsAPI()
    vehicle_statistics = VehicleStatistics()

    manager = VehicleManager(udp_server, firebase_manager, maps_api, vehicle_statistics)

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    try:
        while True:
            pass
    except Exception as e:
        LoggingUtils.log_exception()
        VehicleDataManager().store_all_vehicle_distance_data(manager)
        print(Strings.EXITING_PROGRAM.format(" ", e))
    except KeyboardInterrupt as k_e:
        LoggingUtils.log_exception()
        VehicleDataManager().store_all_vehicle_distance_data(manager)
        print(Strings.EXITING_PROGRAM.format("keyboard ", k_e))
