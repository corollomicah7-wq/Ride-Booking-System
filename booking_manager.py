from booking import Booking

class Booking_Manager:
    def __init__(self, filename = "bookings.txt"):
        self.bookings = []
        self.filename = filename
        self.load_bookings()

    def add_booking(self, booking):
        self.bookings.append(booking)
        self.save_bookings()

    def cancel_booking(self, booking_id):
        self.bookings = [b for b in self.bookings if b.booking_id != booking_id]
        self.save_bookings()

    def save_bookings(self):
        with open(self.filename, "w") as f:
            for b in self.bookings:
                f.write(b.to_file_string() + "\n")

    def load_bookings(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    data = line.strip().split(",")
                    booking_id, user, vehicle_type, start, end, distance, passengers, total_cost = data
                    booking = Booking(booking_id, user, vehicle_type, start, end, float(distance), int(passengers))
                    self.bookings.append(booking)
        except File_Not_Found_Error:
            pass
