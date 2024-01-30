from UDP.entities.vehicle.info.firebase_identification import FirebaseIdentification
from UDP.entities.vehicle.info.location_details import LocationDetails
from UDP.entities.vehicle.info.status_controls import StatusControls
from UDP.entities.vehicle.info.vehicle_data import VehicleData


class VehicleState:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.location_details = LocationDetails()
        self.status_and_controls = StatusControls()
        self.vehicle_data = VehicleData()
        self.firebase_identification = FirebaseIdentification()
