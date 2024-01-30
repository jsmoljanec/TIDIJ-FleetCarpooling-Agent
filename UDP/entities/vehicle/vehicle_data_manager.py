class VehicleDataManager:
    @staticmethod
    def get_local_vehicle_data(state):
        distance_traveled_local = int(state.vehicle_data.distance_traveled)
        fuel_consumption_local = state.vehicle_data.combined_fuel_consumption
        return distance_traveled_local, fuel_consumption_local

    @staticmethod
    def get_firebase_vehicle_data(firebase_identification, vehicle_manager):
        distance_traveled_firebase = vehicle_manager.firebase_manager.vehicles_manager.get_vehicle_traveled_distance(
            firebase_identification.firebase_id)
        fuel_consumption_firebase = vehicle_manager.firebase_manager.reservations_manager.get_reservation_fuel_consumption(
            firebase_identification.reservation_id)
        return distance_traveled_firebase, fuel_consumption_firebase

    @staticmethod
    def update_firebase_data(firebase_identification, total_distance, total_fuel_consumption, vehicle_manager):
        vehicle_id = firebase_identification.firebase_id
        reservation_id = firebase_identification.reservation_id

        data_distance = {'distanceTraveled': total_distance}
        vehicle_manager.firebase_manager.vehicles_manager.update_vehicle_data(vehicle_id, data_distance)

        data_fuel = {'fuelConsumption': total_fuel_consumption}
        vehicle_manager.firebase_manager.reservations_manager.update_reservation_data(reservation_id, data_fuel)

    def store_all_vehicle_distance_data(self, vehicle_manager):
        for vehicle, value in self.get_all_vehicle_states(vehicle_manager).items():
            local_distance, local_fuel = self.get_local_vehicle_data(value)
            firebase_distance, firebase_fuel = self.get_firebase_vehicle_data(value.firebase_identification, vehicle_manager)

            total_distance = firebase_distance + local_distance
            total_fuel_consumption = round(firebase_fuel + local_fuel, 2)
            self.update_firebase_data(value.firebase_identification, total_distance, total_fuel_consumption, vehicle_manager)

            print(f"Vehicle: {vehicle}, Distance traveled: {local_distance}")

    @staticmethod
    def get_vehicle_state(vehicle_manager, vehicle_id):
        if vehicle_id not in vehicle_manager.vehicle_states:
            vehicle_manager.initialize(vehicle_id)
        return vehicle_manager.vehicle_states[vehicle_id]

    @staticmethod
    def get_all_vehicle_states(vehicle_manager):
        return vehicle_manager.vehicle_states
