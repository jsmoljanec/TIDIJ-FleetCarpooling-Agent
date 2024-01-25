from UDP.entities.utilities.date_time_utils import DateTimeUtils
from UDP.entities.vehicle.vehicle_data_manager import VehicleDataManager


class ReservationUtils:
    def __init__(self, firebase_manager):
        self.firebase_manager = firebase_manager

    def create_vehicle_id_from_reservation_dates(self, vehicle_id):
        reservation = self.firebase_manager.reservations_manager.get_current_reservation_for_vin_car(vehicle_id)
        date_time_format = "%Y-%m-%d %H:%M"

        pickup_date = reservation[0]['pickupDate']
        pickup_time = reservation[0]['pickupTime']
        return_date = reservation[0]['returnDate']
        return_time = reservation[0]['returnTime']

        pickup_date_time_raw = DateTimeUtils.convert_date_time_from_string(pickup_date, pickup_time, date_time_format)
        pickup_date_time_number = DateTimeUtils.convert_date_time_to_number(pickup_date_time_raw)
        return_date_time_raw = DateTimeUtils.convert_date_time_from_string(return_date, return_time, date_time_format)
        return_date_time_number = DateTimeUtils.convert_date_time_to_number(return_date_time_raw)

        return f"{vehicle_id}-{pickup_date_time_number}-{return_date_time_number}"

    def check_if_there_is_initiated_reservation_ongoing(self, vehicle_id, manager):
        all_vehicles = VehicleDataManager.get_all_vehicle_states(manager)
        for key, value in all_vehicles.items():
            if key.startswith(vehicle_id):
                input_string = key
                parts = input_string.split('-')

                if len(parts) >= 3:
                    pickup_date_time_number = int(parts[1])
                    return_date_time_number = int(parts[2])
                    if DateTimeUtils.is_current_time_between_dates__num(pickup_date_time_number, return_date_time_number):
                        return key

        return self.create_vehicle_id_from_reservation_dates(vehicle_id)
