import math

coordinates = {
    "Quezon City": {
    "Quezon City": (14.6760, 121.0437),
    "Cubao": (14.6196, 121.0522),
    "Katipunan": (14.6551, 121.0763),
    "Commonwealth": (14.7059, 121.0614),
    "Fairview": (14.7208, 121.0508),
    "Eastwood": (14.6093, 121.0797),
    "UP Diliman": (14.6539, 121.0686),
    "Novaliches": (14.7299, 121.0196)},

    "Manila": {
    "Manila": (14.5995, 120.9842),
    "Intramuros": (14.5924, 120.9741),
    "Divisoria": (14.6001, 120.9756),
    "Binondo": (14.5997, 120.9745),
    "Malate": (14.5696, 120.9895),
    "Ermita": (14.5772, 120.9847),
    "Tondo": (14.6192, 120.9693)},

    "Makati": {
    "Makati": (14.5547, 121.0244),
    "Ayala": (14.5564, 121.0233),
    "Rockwell": (14.5625, 121.0275)},

    "Taguig": {
    "Taguig": (14.5176, 121.0509),
    "BGC": (14.5491, 121.0495),
    "Market Market": (14.5497, 121.0500)},

    "Pasay": {
    "MOA": (14.5352, 120.9832),
    "Mall of Asia": (14.5352, 120.9832),
    "Pasay": (14.5378, 120.9981),
    "NAIA": (14.5086, 121.0194),
    "Airport": (14.5086, 121.0194)},

    "Mandaluyong": {
    "Mandaluyong": (14.5790, 121.0359),
    "SM Megamall": (14.5859, 121.0565),
    "EDSA Shrine": (14.5832, 121.0521)},

    "Pasig": {
    "Pasig": (14.5764, 121.0851),
    "Kapitolyo": (14.5736, 121.0647),
    "Ortigas": (14.5875, 121.0603),
    "Market Market": (14.5497, 121.0500)},

    "Southern Metro Manila": {
    "Paranaque": (14.4794, 121.0199),
    "Las Pinas": (14.4488, 120.9940),
    "Alabang": (14.4219, 121.0430),
    "Festival Mall": (14.4200, 121.0381)},

    "Northern Metro Manila": {
    "Caloocan": (14.6499, 120.9660),
    "Monumento": (14.6574, 120.9840)},

    "Rizal Province": {
    "Marikina": (14.6507, 121.1029),
    "Antipolo": (14.5860, 121.1762),
    "Cainta": (14.5726, 121.1202),
    "Taytay": (14.5618, 121.1330)}
}

# Calculate distance using the Haversine Formula
def haversine_distance(latitude1, longitude1, latitude2, longitude2):

    latitude_1 = math.radians(latitude1)
    longitude_1 = math.radians(longitude1)
    latitude_2 = math.radians(latitude2)
    longitude_2 = math.radians(longitude2)

    distance_latitude = latitude_2 - latitude_1
    distance_longitude = longitude_2 - longitude_1

    haversine_value = (math.sin(distance_latitude / 2) ** 2 + math.cos(latitude_1) * math.cos(latitude_2)
        * math.sin(distance_longitude / 2) ** 2)

    central_angle = 2 * math.atan2(math.sqrt(haversine_value), math.sqrt(1 - haversine_value))

    radius = 6371.0  # Earth's radius in kilometers

    return radius * central_angle

# Get coordinates of a location (case-insensitive)
def get_coordinates(location):
    location = location.strip().lower()

    for category in coordinates.values():
        for name, coords in category.items():
            if name.lower() == location:
                return coords

    return None

# Calculate distance between two cities/locations
def distance_between_cities(start, end):

    start_coordinates = get_coordinates(start)
    end_coordinates = get_coordinates(end)

    if start_coordinates is None:
        raise ValueError(f"Unknown location: '{start}'")

    if end_coordinates is None:
        raise ValueError(f"Unknown location: '{end}'")

    distance = haversine_distance(
        start_coordinates[0], 
        start_coordinates[1],
        end_coordinates[0],
        end_coordinates[1]
    )

    return round(distance, 2)

# Alternative function name (same behavior)
def distance_coordinates(start, end):
    return distance_between_cities(start, end)

# Return all available locations
def known_locations():
    locations = []

    for category in coordinates.values():
        locations.extend(category.keys())
    return sorted(locations)