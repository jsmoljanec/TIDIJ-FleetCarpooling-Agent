from datetime import datetime


class ReservationUtils:
    def __init__(self, firebase_manager):
        self.firebase_manager = firebase_manager

    def create_vehicle_id_from_reservation_dates(self, vehicle_id):
        reservation = self.firebase_manager.reservations_manager.get_current_reservation_for_vin_car(vehicle_id)

        pickup_date_time_raw = datetime.strptime(f"{reservation[0]['pickupDate']} {reservation[0]['pickupTime']}",
                                                 "%Y-%m-%d %H:%M")
        pickup_date_time_number = int((pickup_date_time_raw - datetime(1970, 1, 1)).total_seconds() / 60)
        return_date_time_raw = datetime.strptime(f"{reservation[0]['returnDate']} {reservation[0]['returnTime']}",
                                                 "%Y-%m-%d %H:%M")
        return_date_time_number = int((return_date_time_raw - datetime(1970, 1, 1)).total_seconds() / 60)

        return f"{vehicle_id}-{pickup_date_time_number}-{return_date_time_number}"

    def check_if_there_is_initiated_reservation_ongoing(self, vehicle_id, manager):
        current_datetime = datetime.now()
        current_datetime_number = (current_datetime - datetime(1970, 1, 1)).total_seconds() / 60

        all_vehicles = manager.get_all_vehicle_states()
        for key, value in all_vehicles.items():
            if key.startswith(vehicle_id):
                input_string = key
                parts = input_string.split('-')

                if len(parts) >= 3:
                    pickup_date_time_number = int(parts[1])
                    return_date_time_number = int(parts[2])
                    if pickup_date_time_number <= current_datetime_number <= return_date_time_number:
                        return key

        return self.create_vehicle_id_from_reservation_dates(vehicle_id)
