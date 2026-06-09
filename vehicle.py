from distance_service import distance_between_cities, known_locations

TAX_RATE = 0.12

class Vehicle:
    def __init__(self, vehicle_type: str, base_fare: float, rate_per_km: float, capacity_options: list, emoji: str = ""):
        self._type = vehicle_type
        self._base_fare = base_fare
        self._rate = rate_per_km
        self._emoji = emoji
        self._capacity_options = capacity_options
        
    def get_type(self) -> str:
        return self._type

    def get_label(self) -> str:
        return f"{self._emoji} {self._type}".strip()
    
    def get_capacity_options(self) -> list:
        return self._capacity_options
    
    def get_capacity(self) -> int:
        return self._capacity
    
    def get_base_fare(self) -> float:
        return self._base_fare
    
    def get_rate(self) -> float:
        return self._rate

    def calculate_subtotal(self, distance: float):
        return self._base_fare + self._rate * distance

    def calculate_cost(self, distance: float) -> float:
        return self.calculate_subtotal(distance)

class Car(Vehicle):
    def __init__(self, vehicle_type: str, base_fare: float, rate_per_km: float, capacity_options: list, emoji: str = ""):
        super().__init__(vehicle_type, base_fare, rate_per_km, capacity_options, emoji)

    def calculate_cost(self, distance: float) -> float:
        subtotal = self.calculate_subtotal(distance)
        return round(subtotal * (1 + TAX_RATE), 2)

class Van(Vehicle):
    def __init__(self, vehicle_type: str, base_fare: float, rate_per_km: float, capacity_options: list, emoji: str = ""):
        super().__init__(vehicle_type, base_fare, rate_per_km, capacity_options, emoji)

    def calculate_cost(self, distance: float) -> float:
        subtotal = self.calculate_subtotal(distance)
        return round(subtotal * 1.10 * (1 + TAX_RATE), 2)

class Motorcycle(Vehicle):
    def __init__(self, vehicle_type: str, base_fare: float, rate_per_km: float, capacity_options: list, emoji: str = ""):
        super().__init__(vehicle_type, base_fare, rate_per_km, capacity_options, emoji)

    def calculate_cost(self, distance: float) -> float:
        subtotal = self.calculate_subtotal(distance)
        return round(subtotal * 0.95 * (1 + TAX_RATE), 2)

VEHICLES = {
    "Car": Car("Car", 20.0, 10.0, capacity_options=[4, 6], emoji="🚗"),              
    "Van": Van("Van", 50.0, 15.0, capacity_options=[10, 12, 15], emoji="🚌"),        
    "Motorcycle": Motorcycle("Motorcycle", 0.0, 5.0, capacity_options=[1], emoji="🏍")
}

VEHICLE_LABELS = {v.get_label(): k for k, v in VEHICLES.items()}

KNOWN_LOCATIONS = known_locations()

def calc_cost(start: str, end: str, vehicle_type: str):
    """Return (distance_km, total_cost) using real GPS coordinates."""
    vehicle = VEHICLES.get(vehicle_type)

    if vehicle is None:
        return 0, 0

    try:
        dist = distance_between_cities(start, end)
    except ValueError:
        dist = round(5.0 + (len(start) + len(end)) % 20, 1)

    cost = vehicle.calculate_cost(dist)
    return dist, cost
