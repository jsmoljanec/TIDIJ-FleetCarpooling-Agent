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
            current_time = datetime.now()

            matching_reservations = []

            for reservation_id, reservation_data in reservations.items():
                car_vin = reservation_data.get("VinCar", "")
                start_datetime = datetime.strptime(
                    reservation_data.get("pickupDate") + " " + reservation_data.get("pickupTime"), "%Y-%m-%d %H:%M")
                end_datetime = datetime.strptime(
                    reservation_data.get("returnDate") + " " + reservation_data.get("returnTime"), "%Y-%m-%d %H:%M")

                if car_vin == vehicle_id and start_datetime <= current_time <= end_datetime:
                    matching_reservations.append({
                        "reservation_id": reservation_id,
                        "VinCar": car_vin,
                        "pickupDate": reservation_data.get("pickupDate", ""),
                        "pickupTime": reservation_data.get("pickupTime", ""),
                        "returnDate": reservation_data.get("returnDate", ""),
                        "returnTime": reservation_data.get("returnTime", ""),
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
