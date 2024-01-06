import sys
import threading
from entities.vehicle_manager import VehicleManager
import atexit
import traceback
from datetime import datetime


def cleanup():
    print("Ovo će se izvršiti pri izlasku iz programa.")


atexit.register(cleanup)


def log_exception():
    exception_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("exceptions.log", "a") as log_file:
        log_file.write(f"Exception occurred at: {exception_time}\n")
        traceback.print_exc(file=log_file)


if __name__ == "__main__":
    host = '127.0.0.1' if len(sys.argv) == 1 else sys.argv[1]

    manager = VehicleManager(host)

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    try:
        while True:
            pass
    except Exception as e:
        log_exception()
        # manager.store_all_vehicle_distance_data()
        print(f"Izlaz iz programa zbog iznimke: {e}")
    except KeyboardInterrupt:
        log_exception()
        # manager.store_all_vehicle_distance_data()
        print("Izlaz iz programa zbog pritiska tipke za prekid.")
