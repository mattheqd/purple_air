import math

def calculate_aqi(pm_concentration: float) -> int:
    'Converts a PM 2.5 concentration into AQI'
    if pm_concentration >= 0 and pm_concentration < 12.1:
        return _round_away_from_zero(pm_concentration*50/12)
    elif pm_concentration >= 12.1 and pm_concentration < 35.5:
        return _round_away_from_zero(51 + (pm_concentration-12.1)*49/23.3)
    elif pm_concentration >= 35.5 and pm_concentration < 55.5:
        return _round_away_from_zero(101 + (pm_concentration-35.5)*49/19.9)
    elif pm_concentration >= 55.5 and pm_concentration < 150.5:
        return _round_away_from_zero(151 + (pm_concentration-55.5)*49/94.9)
    elif pm_concentration >= 150.5 and pm_concentration < 250.5:
        return _round_away_from_zero(201 + (pm_concentration-150.5)*99/99.9)
    elif pm_concentration >= 250.5 and pm_concentration < 350.5:
        return _round_away_from_zero(301 + (pm_concentration-250.5)*99/99.9)
    elif pm_concentration >= 350.5 and pm_concentration < 500.5:
        return _round_away_from_zero(401 + (pm_concentration-350.5)*99/149.9)
    elif pm_concentration >= 500.5:
        return 501
    else:
        return -1

def equirectangular_approximation(center_coordinates: tuple, target_coordinates: tuple) -> float:
    'Calculates the distance between two coordiantes'
    dlat = math.radians(center_coordinates[0]) - math.radians(target_coordinates[0])
    dlon = math.radians(center_coordinates[1]) - math.radians(target_coordinates[1])
    alat = (math.radians(center_coordinates[0]) + math.radians(target_coordinates[0]))/2
    r = 3958.4
    x = dlon * math.cos(alat)
    d = math.sqrt(pow(x,2) + pow(dlat,2)) * r
    return d

def format_coordinate(coordinate: tuple) -> str:
    'Converts a coordinate in a tuple format into readable format'
    if coordinate[0] >= 0:
        lat = str(coordinate[0]) + '/N'
    else:
        lat = str(coordinate[0]*-1) + '/S'
    if coordinate[1] >= 0:
        lon = str(coordinate[1]) + '/E'
    else:
        lon = str(coordinate[1]*-1) + '/W'
    return lat + ' ' + lon

def _round_away_from_zero(number: float) -> int:
    'Rounds a rounded version of a floating point number'
    return math.floor(number + 0.5)


