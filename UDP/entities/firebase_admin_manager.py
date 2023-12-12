import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class FirebaseAdminManager:
    def __init__(self, credentials_path, database_url):
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})
        self.db_reference = db.reference()

    def get_all_vehicle_data(self):
        return self.db_reference.child('Vehicles').get()

    def update_vehicle_data(self, vehicle_id, data):
        self.db_reference.child(f'Vehicles/{vehicle_id}').update(data)
