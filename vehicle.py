from distance_service import distance_between_cities
VEHICLES = {"Car 🚗":12, "Van 🚌":18, "Motorcycle 🏍":5}

def calc_cost(start, end, vehicle_type):
    try:
        dist = distance_between_cities(start, end)
        if vehicle_type == "Car 🚗":
            cost = 20 + (dist * 10)
        elif vehicle_type == "Van 🚌":
            cost = 50 + (dist * 15)
        elif vehicle_type == "Motorcycle 🏍":
            cost = dist * 5
        else:
            raise ValueError("Invalid vehicle type.")
        return dist, cost
    except Exception as e:
        print(f"Could not calculate distance/cost: {e}")
        return 0, 0
