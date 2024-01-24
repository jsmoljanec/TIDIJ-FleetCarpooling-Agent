from UDP.entities.utilities.strings import Strings


class StatusControls:
    def __init__(self):
        self.is_running = False
        self.stop_requested = False
        self.restart_requested = False
        self.last_command = None
        self.locked = None

    def update_vehicle_lock_status(self, lock):
        self.locked = lock

    def is_vehicle_stopped(self):
        return not self.is_running or self.last_command == Strings.STOP_COMMAND

    def is_vehicle_restarted(self):
        return self.last_command == Strings.RESTART_COMMAND

    def is_vehicle_running(self):
        return self.is_running or self.last_command == Strings.START_COMMAND

    def is_vehicle_locked(self):
        return self.locked is True

    def remember_vehicle_last_command(self, command):
        self.last_command = command

    def change_vehicle_state(self, is_running, stop_requested, restart_requested):
        self.is_running = is_running
        self.stop_requested = stop_requested
        self.restart_requested = restart_requested
