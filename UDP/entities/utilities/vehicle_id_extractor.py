from UDP.entities.utilities.strings import Strings


class VehicleIdExtractor:
    @staticmethod
    def extract_vehicle_id(vehicle_id):
        input_string = vehicle_id
        parts = input_string.split('-')

        if len(parts) >= 3:
            first = parts[0]
            return first
        else:
            print(Strings.ERROR_STRING_FORMAT)
            return None
