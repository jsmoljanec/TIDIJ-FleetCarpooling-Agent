import threading

from UDP.entities.utilities.strings import Strings


class VehicleCommandProcessor:
    @staticmethod
    def start_command(vehicle_manager, address, vehicle_id):
        state = vehicle_manager.vehicle_data_manager.get_vehicle_state(vehicle_manager, vehicle_id)

        if state.status_and_controls.is_vehicle_locked() is not True:
            if state.location_details.is_destination_set():
                if state.status_and_controls.is_vehicle_running():
                    print(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id))
                    vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id), address)
                else:
                    print(Strings.VEHICLE_STARTED.format(vehicle_id))
                    vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_STARTED.format(vehicle_id), address)
                    state.status_and_controls.remember_vehicle_last_command(Strings.START_COMMAND)
                    vehicle_thread = threading.Thread(target=vehicle_manager.start, args=(address, state))
                    vehicle_thread.start()
            else:
                print(Strings.VEHICLE_NO_DESTINATION.format(state.vehicle_id))
                vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_NO_DESTINATION.format(state.vehicle_id), address)
        else:
            print(Strings.VEHICLE_CANT_START_LOCKED.format(state.vehicle_id))
            vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_CANT_START_LOCKED.format(state.vehicle_id), address)

    @staticmethod
    def stop_command(vehicle_manager, address, vehicle_id):
        state = vehicle_manager.vehicle_data_manager.get_vehicle_state(vehicle_manager, vehicle_id)

        if state.status_and_controls.is_vehicle_stopped():
            print(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id))
            vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id), address)
        else:
            print(Strings.VEHICLE_STOPPED.format(vehicle_id))
            state.status_and_controls.remember_vehicle_last_command(Strings.STOP_COMMAND)
            vehicle_manager.stop(address, state)
            vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_STOPPED.format(vehicle_id), address)

    @staticmethod
    def restart_command(vehicle_manager, address, vehicle_id):
        state = vehicle_manager.vehicle_data_manager.get_vehicle_state(vehicle_manager, vehicle_id)

        if not state.location_details.is_destination_set():
            print(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id))
            vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id), address)
            return

        if not state.status_and_controls.is_vehicle_locked():
            if state.status_and_controls.is_vehicle_restarted():
                print(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id))
                vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id), address)
            else:
                state.status_and_controls.remember_vehicle_last_command(Strings.RESTART_COMMAND)
                if state.status_and_controls.stop_requested:
                    print(Strings.VEHICLE_RESTARTED.format(vehicle_id))
                    vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_RESTARTED.format(vehicle_id), address)
                    state.location_details.last_stopped_location = None
                    state.location_details.last_index = 0

                vehicle_manager.restart(address, state)
        else:
            print(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id))
            vehicle_manager.udp_server.send_udp_message(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id), address)

    @staticmethod
    def lock_status_command(vehicle_manager, address, vehicle_id):
        state = vehicle_manager.vehicle_data_manager.get_vehicle_state(vehicle_manager, vehicle_id)

        is_locked = state.status_and_controls.is_vehicle_locked()
        state.status_and_controls.update_vehicle_lock_status(not is_locked)
        data = {'locked': not is_locked}

        vehicle_manager.lock(state, vehicle_id, address, data)

    @staticmethod
    def current_location_command(vehicle_manager, address, vehicle_id):
        state = vehicle_manager.vehicle_data_manager.get_vehicle_state(vehicle_manager, vehicle_id)
        vehicle_manager.udp_server.send_udp_message(
            Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location_details.location), address)
        print(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location_details.location))