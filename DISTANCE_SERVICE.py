from math import *

# Calculate the distance between two GPS coordinates using the Haversine Formula
def haversine_distance(latitude1, longitude1, latitude2, longitude2):
    
    # convert latitude and longitude from degrees to radians
    latitude_1 = radians(latitude1)
    longitude_1 = radians(longitude1)
    latitude_2 = radians(latitude2)
    longitude_2 = radians(longitude2)

    # calculate the difference between coordinates
    distance_latitude = latitude_2 - latitude_1
    distance_longitude = longitude_2 - longitude_1

    haversine_value = sin(distance_latitude / 2)**2 + cos(latitude_1) * cos(latitude_2) * sin(distance_longitude / 2)**2 # Haversine formula
    central_angle = 2 * atan2(sqrt(haversine_value), sqrt(1 - haversine_value))

    radius = 6371.0  # earth's radius in kilometers

    distance = radius * central_angle # calculate the distance

    return distance

