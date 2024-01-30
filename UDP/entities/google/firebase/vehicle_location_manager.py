from UDP.entities.utilities.strings import Strings


class VehicleLocationsManager:
    def __init__(self, db_reference):
        self.LATITUDE_KEY = "latitude"
        self.LONGITUDE_KEY = "longitude"
        self.LOCKED_KEY = "locked"

        self.db_reference = db_reference.child('VehicleLocations')

    def get_vehicle_current_position(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(vehicle_id).get()
            return {
                self.LATITUDE_KEY: vehicle_data.get(self.LATITUDE_KEY, 0.0),
                self.LONGITUDE_KEY: vehicle_data.get(self.LONGITUDE_KEY, 0.0)
            }
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_LOCATION.format(e))
            raise e

    def get_vehicle_lock_status(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(vehicle_id).get()
            return {
                self.LOCKED_KEY: vehicle_data.get(self.LOCKED_KEY, 0.0)
            }
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_LOCK_STATUS.format(e))
            raise e

    def update_vehicle_location_data(self, vehicle_id, data):
        try:
            self.db_reference.child(vehicle_id).update(data)
        except Exception as e:
            print(Strings.ERROR_FIREBASE_UPDATE_VEHICLE_LOCATION_DATA.format(e))
            raise e

    def get_all_vehicle_location_data(self, vehicle_id):
        try:
            return self.db_reference.child(vehicle_id).get()
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_LOCATION_DATA.format(e))
            raise e
