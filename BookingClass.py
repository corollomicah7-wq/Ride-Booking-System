class Booking:
    def __init__(self, booking_id, user, vehicle, start_location, end_location, distance, passengers):
        self.booking_id = booking_id
        self.user = user
        self.vehicle = vehicle
        self.start_location = start_location
        self.end_location = end_location
        self.distance = float(distance)
        self.passengers = int(passengers)
        self.total_cost = self.vehicle.calculate_cost(self.distance)

    def to_file_string(self):
        """
        Returns a comma-separated string with exactly 8 fields.
        Matches what BookingManager.load_bookings() unpacks:
        booking_id, user, vehicle_type, start, end, distance, passengers, total_cost
        """
        return ",".join([
            str(self.booking_id),
            str(self.user),
            str(self.vehicle.get_type()),
            str(self.start_location),
            str(self.end_location),
            str(self.distance),
            str(self.passengers),
            str(self.total_cost)
        ])

    def __str__(self):
        return (
            f"Booking ID   : {self.booking_id}\n"
            f"User         : {self.user}\n"
            f"Vehicle      : {self.vehicle.get_type()}\n"
            f"From         : {self.start_location}\n"
            f"To           : {self.end_location}\n"
            f"Distance     : {self.distance} mi\n"
            f"Passengers   : {self.passengers}\n"
            f"Total Cost   : ₱{self.total_cost:.2f}"
        )