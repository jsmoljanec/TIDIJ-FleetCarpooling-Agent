import sys
import threading
from entities.vehicle_manager import VehicleManager


if __name__ == "__main__":
    host = '127.0.0.1' if len(sys.argv) == 1 else sys.argv[1]

    manager = VehicleManager(host)

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    while True:
        pass
