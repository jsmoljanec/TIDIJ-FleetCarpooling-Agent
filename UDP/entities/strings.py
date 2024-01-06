class Strings:
    # Debugging utilities
    MESSAGE_SEPARATOR = "---------------------------"

    # Controller commands
    START_COMMAND = "start"
    STOP_COMMAND = "stop"
    RESTART_COMMAND = "restart"
    CURRENT_POSITION_COMMAND = "current-position"
    SET_DESTINATION_COMMAND = "set-destination"
    LOCK_COMMAND = "lock"

    # Agent control messages
    AGENT_UP = "Agent up and listening on {}:{}"

    # Vehicle control messages
    VEHICLE_CURRENT_LOCATION = "[0000] Vehicle [{}] is currently at: {}."
    VEHICLE_STARTED = "[0001] Vehicle [{}] started ride."
    VEHICLE_STOPPED = "[0010] Vehicle [{}] stopped ride."
    VEHICLE_RESTARTED = "[0011] Restarting vehicle [{}] from the beginning."
    VEHICLE_ALREADY_RUNNING = "[0100] Vehicle [{}] is already running or has already received a start command. Cannot start again."
    VEHICLE_NOT_RUNNING = "[0101] Vehicle [{}] is not currently running or has already received a stop command. Cannot stop."
    VEHICLE_NO_DESTINATION = "[0110] There is no destination set for [{}]."
    VEHICLE_CANNOT_RESTART = "[0111] Vehicle [{}] cannot be to restarted."
    VEHICLE_ALREADY_RESTARTED = "[1000] Vehicle [{}] is already restarted!"
    VEHICLE_RESUMED = "[1001] Vehicle [{}] resumes ride from the last stopped location: {}."
    VEHICLE_DRIVING_LOCATION = "[1010] Vehicle [{}] is driving and currently at: {}."
    VEHICLE_ROUTE_SET = "[1011] Vehicle [{}] has set destination to {}."
    VEHICLE_LOCKED = "[1100] Vehicle [{}] is locked."
    VEHICLE_UNLOCKED = "[1101] Vehicle [{}] is unlocked."
    VEHICLE_CANT_START_LOCKED = "[1110] Vehicle [{}] cant start because it is locked."

    # Error handling messages
    ERROR_UDP_BINDING = "Error binding UDP socket: {}."
    ERROR_LOCATION_FIND = "Cant find destination: {} as requested by: {}."
    ERROR_GOOGLE_MAPS_API_KEY = "Valid Google Maps API key is not provided. Please set the GOOGLE_MAPS_API_KEY environment variable with valid API key."
    ERROR_GOOGLE_MAPS_ROUTE = "No directions found."
    ERROR_GOOGLE_DIRECTIONS = "Error getting directions: {}."
    ERROR_FIREBASE = "Error initializing Firebase app: {}."
    ERROR_FIREBASE_GET_VEHICLE_DATA = "Error getting all vehicle data: {}."
    ERROR_FIREBASE_UPDATE_VEHICLE_DATA = "Error updating vehicle data: {}."
    ERROR_FIREBASE_GET_VEHICLE_LOCATION = "Error getting vehicle current position: {}."
    ERROR_FIREBASE_GET_VEHICLE_LOCK_STATUS = "Error getting vehicle lock status: {}."
    ERROR_FIREBASE_GET_VEHICLE_TRAVELED_DISTANCE = "Error getting vehicle traveled distance: {}."
    ERROR_FIREBASE_GET_VEHICLE_FUEL_CONSUMPTION = "Error getting nominal vehicle fuel consumption: {}."
    ERROR_FIREBASE_GET_CURRENT_RESERVATION = "Error getting current reservation: {}."
