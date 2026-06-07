class Vehicle:
    def __init__(self, vehicle_type, cost_per_mile, capacity):
        self._vehicle_type = vehicle_type
        self._cost_per_mile = cost_per_mile
        self._capacity = capacity

    def calculate_cost(self, distance):
        return distance * self._cost_per_mile

    def get_type(self):
        return self._vehicle_type

    def get_capacity(self):
        return self._capacity

class Car(Vehicle):
    def __init__(self):
        super().__init__("Car", cost_per_mile=12, capacity=4)

    def calculate_cost(self, distance):
        base_cost = super().calculate_cost(distance)
        luxury_tax = 20
        return base_cost + luxury_tax

class Van(Vehicle):
    def __init__(self):
        super().__init__("Van", cost_per_mile=18, capacity=12)

    def calculate_cost(self, distance):
        base_cost = super().calculate_cost(distance)
        service_fee = 50
        return base_cost + service_fee

class Bike(Vehicle):
    def __init__(self):
        super().__init__("Bike", cost_per_mile=5, capacity=1)

    def calculate_cost(self, distance):
        return distance * self._cost_per_mile
