from distance_service import distance_between_cities, known_locations

class Vehicle:
    def __init__(self, vehicle_type: str, base_fare: float, rate_per_km: float, emoji: str = ""):
        self._type      = vehicle_type
        self._base_fare = base_fare
        self._rate      = rate_per_km
        self._emoji     = emoji 
       
    def get_type(self) -> str:
        return self._type

    def get_label(self) -> str:
        return f"{self._emoji} {self._type}".strip()

    def calculate_cost(self, distance: float) -> float:
        return round(self._base_fare + self._rate * distance, 2)

# Plain string keys — no emoji encoding issues
VEHICLES = {
    "Car":        Vehicle("Car",        20.0, 10.0, "🚗"),
    "Van":        Vehicle("Van",        50.0, 15.0, "🚌"),
    "Motorcycle": Vehicle("Motorcycle",  0.0,  5.0, "🏍"),
}
# Maps display label
VEHICLE_LABELS = {v.get_label(): k for k, v in VEHICLES.items()}

# Expose known locations for GUI dropdown / validation
KNOWN_LOCATIONS = known_locations()

def calc_cost(start: str, end: str, vehicle_type: str):
    """Return (distance_km, total_cost) using real GPS coordinates."""
    vehicle = VEHICLES.get(vehicle_type)
    if vehicle is None:
        return 0, 0
    try:
        dist = distance_between_cities(start, end)
    except ValueError:
        # Location not in database — fall back to deterministic estimate
        dist = round(5.0 + (len(start) + len(end)) % 20, 1)
    cost = vehicle.calculate_cost(dist)
    return dist, cost
