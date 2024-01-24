from UDP.entities.utilities.date_time_utils import DateTimeUtils
from UDP.entities.utilities.strings import Strings
from datetime import datetime


class ReservationsManager:
    def __init__(self, db_reference):
        self.FUEL_CONSUMPTION = "fuelConsumption"

        self.db_reference = db_reference.child('Reservation')

    def get_reservation_fuel_consumption(self, reservation_id):
        try:
            vehicle_data = self.db_reference.child(reservation_id).get()
            return vehicle_data.get(self.FUEL_CONSUMPTION, 0.0)

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_RESERVATION_FUEL_CONSUMPTION.format(e))
            raise e

    def get_current_reservation_for_vin_car(self, vehicle_id):
        try:
            reservations = self.db_reference.get()
            date_time_format = "%Y-%m-%d %H:%M"

            matching_reservations = []

            for reservation_id, reservation_data in reservations.items():
                car_vin = reservation_data.get("VinCar", "")
                pickup_date = reservation_data.get("pickupDate")
                pickup_time = reservation_data.get("pickupTime")
                return_date = reservation_data.get("returnDate")
                return_time = reservation_data.get("returnTime")
                start_datetime = datetime.strptime(pickup_date + " " + pickup_time, date_time_format)
                end_datetime = datetime.strptime(return_date + " " + return_time, date_time_format)

                if car_vin == vehicle_id and DateTimeUtils.is_current_time_between_dates__string(start_datetime, end_datetime):
                    matching_reservations.append({
                        "reservation_id": reservation_id,
                        "VinCar": car_vin,
                        "pickupDate": pickup_date,
                        "pickupTime": pickup_time,
                        "returnDate": return_date,
                        "returnTime": return_time,
                    })

            return matching_reservations

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_CURRENT_RESERVATION.format(e))
            raise e

    def update_reservation_data(self, reservation_id, data):
        try:
            self.db_reference.child(reservation_id).update(data)
        except Exception as e:
            print(Strings.ERROR_FIREBASE_UPDATE_RESERVATION_DATA.format(e))
            raise e
