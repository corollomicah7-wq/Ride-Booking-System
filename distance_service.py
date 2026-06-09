import math

_COORDS = {
    # Quezon City
    "Quezon City": (14.6760, 121.0437),
    "Cubao": (14.6196, 121.0522),
    "Katipunan": (14.6551, 121.0763),
    "Commonwealth": (14.7059, 121.0614),
    "Fairview": (14.7208, 121.0508),
    "Eastwood": (14.6093, 121.0797),
    "UP Diliman": (14.6539, 121.0686),
    "Novaliches": (14.7299, 121.0196),

    # Manila
    "Manila": (14.5995, 120.9842),
    "Intramuros": (14.5924, 120.9741),
    "Divisoria": (14.6001, 120.9756),
    "Binondo": (14.5997, 120.9745),
    "Malate": (14.5696, 120.9895),
    "Ermita": (14.5772, 120.9847),
    "Tondo": (14.6192, 120.9693),

    # Makati / BGC
    "Makati": (14.5547, 121.0244),
    "BGC": (14.5491, 121.0495),
    "Ayala": (14.5564, 121.0233),
    "Rockwell": (14.5625, 121.0275),

    # Pasay
    "MOA": (14.5352, 120.9832),
    "Mall of Asia": (14.5352, 120.9832),
    "Pasay": (14.5378, 120.9981),
    "NAIA": (14.5086, 121.0194),
    "Airport": (14.5086, 121.0194),

    # Ortigas / Mandaluyong
    "Ortigas": (14.5875, 121.0603),
    "Mandaluyong": (14.5790, 121.0359),
    "SM Megamall": (14.5859, 121.0565),
    "EDSA Shrine": (14.5832, 121.0521),

    # Pasig / Taguig
    "Pasig": (14.5764, 121.0851),
    "Kapitolyo": (14.5736, 121.0647),
    "Taguig": (14.5176, 121.0509),
    "Market Market": (14.5497, 121.0500),

    # South
    "Paranaque": (14.4794, 121.0199),
    "Las Pinas": (14.4488, 120.9940),
    "Alabang": (14.4219, 121.0430),
    "Festival Mall": (14.4200, 121.0381),

    # North
    "Caloocan": (14.6499, 120.9660),
    "Monumento": (14.6574, 120.9840),

    # East
    "Marikina": (14.6507, 121.1029),
    "Antipolo": (14.5860, 121.1762),
    "Cainta": (14.5726, 121.1202),
    "Taytay": (14.5618, 121.1330),
}

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two GPS points, in kilometres."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a  = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _lookup(location: str) -> tuple[float, float] | None:
    if location in _COORDS:
        return _COORDS[location]
    low = location.strip().lower()
    for name, coords in _COORDS.items():
        if name.lower() == low:
            return coords
    for name, coords in _COORDS.items():
        if low in name.lower() or name.lower() in low:
            return coords
    return None

#Public API 

def distance_between_cities(start: str, end: str) -> float:
   
    c1 = _lookup(start)
    c2 = _lookup(end)
    if c1 is None:
        raise ValueError(f"Unknown location: '{start}'")
    if c2 is None:
        raise ValueError(f"Unknown location: '{end}'")
    return round(_haversine_km(c1[0], c1[1], c2[0], c2[1]), 2)

def distance_coordinates(start, end):

    start_coordinates = _lookup(start)
    end_coordinates = _lookup(end)

    if start_coordinates is None:
        raise ValueError(f"Unknown location: '{start}'")

    if end_coordinates is None:
        raise ValueError(f"Unknown location: '{end}'")

    distance = _haversine_km(start_coordinates[0], start_coordinates[1], end_coordinates[0], end_coordinates[1])

    return round(distance, 2)


def known_locations() -> list[str]:
  return sorted(_COORDS.keys())
