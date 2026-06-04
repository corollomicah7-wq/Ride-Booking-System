class Vehicle:
    def __init__(self, vehicle_type, cost_per_mile, capacity):
        self.vehicle_type = vehicle_type
        self.cost_per_mile = cost_per_mile
        self.capacity = capacity

    def calculate_cost(self, distance):
        return self.cost_per_mile * distance
    
    def get_type(self):
        return self.vehicle_type
    
    def get_capacity(self):
        return self.capacity
    
class Car(Vehicle):
    def __init__(self, cost_per_mile, capacity):
        super().__init__('Car', 10, 4)

    def calculate_cost(self, distance):
        return 20 + (distance * 10)
    
class Van(Vehicle):
    def __init__(self, cost_per_mile, capacity):
        super().__init__('Van', 15, 12)

    def calculate_cost(self, distance):
        return 50 + (distance * 15)
    
class Bike(Vehicle):
    def __init__(self, cost_per_mile, capacity):
        super().__init__('Bike', 5, 1)

    def calculate_cost(self, distance):
        return distance * 5