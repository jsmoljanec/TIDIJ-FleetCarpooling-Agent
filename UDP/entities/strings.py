class Strings:
    # Debugging utilities
    MESSAGE_SEPARATOR = "---------------------------"

    # Controller commands
    START_COMMAND = "start"
    STOP_COMMAND = "stop"
    RESTART_COMMAND = "restart"
    CURRENT_POSITION_COMMAND = "current-position"
    SET_DESTINATION_COMMAND = "set-destination"

    # Agent control messages
    AGENT_UP = "Agent up and listening on {}:{}"

    # Vehicle control messages
    VEHICLE_CURRENT_LOCATION = "Vehicle {} is currently at: {}."
    VEHICLE_STARTED = "Vehicle {} started ride."
    VEHICLE_STOPPED = "Vehicle {} stopped ride."
    VEHICLE_RESTARTED = "Restarting vehicle {} from the beginning."
    VEHICLE_ALREADY_RUNNING = "Vehicle {} is already running or has already received a start command. Cannot start again."
    VEHICLE_NOT_RUNNING = "Vehicle {} is not currently running or has already received a stop command. Cannot stop."
    VEHICLE_NO_DESTINATION = "There is no destination set for {}."
    VEHICLE_CANNOT_RESTART = "Vehicle {} cannot be to restarted."
    VEHICLE_ALREADY_RESTARTED = "Vehicle {} is already restarted!"
    VEHICLE_RESUMED = "Resuming ride from the last stopped location: {}."
    VEHICLE_DRIVING_LOCATION = "Vehicle {} is driving and currently at: {}."
    VEHICLE_ROUTE_SET = "Vehicle {} has set destination to {}."

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
