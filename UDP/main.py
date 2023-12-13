import threading
from entities.vehicle_manager import VehicleManager

if __name__ == "__main__":
    manager = VehicleManager()

    command_thread = threading.Thread(target=manager.receive_commands)
    command_thread.start()

    while True:
        pass