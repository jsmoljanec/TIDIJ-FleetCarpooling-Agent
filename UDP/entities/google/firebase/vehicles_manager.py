from UDP.entities.utilities.strings import Strings


class VehiclesManager:
    def __init__(self, db_reference):
        self.DISTANCE_TRAVELLED_KEY = "distanceTraveled"
        self.FUEL_CONSUMPTION = "fuelConsumption"

        self.db_reference = db_reference.child('Vehicles')

    def get_all_vehicle_data(self, vehicle_id):
        try:
            return self.db_reference.child(vehicle_id).get()
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_DATA.format(e))
            raise e

    def update_vehicle_data(self, vehicle_id, data):
        try:
            self.db_reference.child(vehicle_id).update(data)
        except Exception as e:
            print(Strings.ERROR_FIREBASE_UPDATE_VEHICLE_DATA.format(e))
            raise e

    def get_vehicle_traveled_distance(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(vehicle_id).get()
            return vehicle_data.get(self.DISTANCE_TRAVELLED_KEY, 0.0)

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_TRAVELED_DISTANCE.format(e))
            raise e

    def get_vehicle_nominal_fuel_consumption(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(vehicle_id).get()
            return vehicle_data.get(self.FUEL_CONSUMPTION, 0.0)

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_FUEL_CONSUMPTION.format(e))
            raise e
