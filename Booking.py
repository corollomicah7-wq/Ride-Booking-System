from vehicle import VEHICLES


class Booking:
    def __init__(self, booking_id, user, vehicle_type, start_location, end_location, distance, passengers=1):
        self.booking_id     = booking_id
        self.user           = user
        self.vehicle_type   = vehicle_type
        self.vehicle        = VEHICLES.get(vehicle_type)
        self.start_location = start_location
        self.end_location   = end_location
        self.distance       = float(distance)
        self.passengers     = int(passengers)

        if self.vehicle is None:
            raise ValueError(f"Unknown vehicle type: '{vehicle_type}'. Valid: {list(VEHICLES.keys())}")

        self.total_cost = self.vehicle.calculate_cost(self.distance)

    def to_file_string(self) -> str:
        return ",".join([
            str(self.booking_id),
            str(self.user),
            self.vehicle_type,
            str(self.start_location),
            str(self.end_location),
            str(self.distance),
            str(self.passengers),
            str(self.total_cost),
        ])

    def __str__(self) -> str:
        return (
            f"Booking ID   : {self.booking_id}\n"
            f"User         : {self.user}\n"
            f"Vehicle      : {self.vehicle.get_label()}\n"
            f"From         : {self.start_location}\n"
            f"To           : {self.end_location}\n"
            f"Distance     : {self.distance} km\n"
            f"Passengers   : {self.passengers}\n"
            f"Total Cost   : ₱{self.total_cost:.2f}"
        )
    
