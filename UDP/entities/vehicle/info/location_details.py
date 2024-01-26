class LocationDetails:
    def __init__(self):
        self.coordinates = []
        self.location = None
        self.last_stopped_location = None
        self.last_index = 0

    def get_location(self):
        return self.location

    def set_route(self, coordinates):
        self.coordinates = coordinates

    def set_location(self, location):
        self.location = location

    def is_destination_set(self):
        return len(self.coordinates) > 0

    def check_index(self):
        if self.last_index > 0:
            self.last_index -= 1
