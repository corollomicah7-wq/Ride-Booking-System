from Booking import Booking


class BookingManager:
    def __init__(self, filename="Bookings.txt"):
        self.bookings = []
        self.filename = filename
        self.load_bookings()

    def add_booking(self, booking: Booking):
        self.bookings.append(booking)
        self.save_bookings()

    def cancel_booking(self, booking_id):
        self.bookings = [b for b in self.bookings if str(b.booking_id) != str(booking_id)]
        self.save_bookings()

    def save_bookings(self):
        with open(self.filename, "w") as f:
            for b in self.bookings:
                f.write(b.to_file_string() + "\n")

    def load_bookings(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) < 7:
                        continue
                    booking_id, user, vehicle_type, start, end, distance = parts[:6]
                    passengers = parts[6] if len(parts) > 6 else "1"
                    b = Booking(booking_id, user, vehicle_type, start, end,
                                float(distance), int(passengers))
                    self.bookings.append(b)
        except FileNotFoundError:
            pass
