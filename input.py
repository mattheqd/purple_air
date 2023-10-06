from pathlib import Path
import urllib.parse
import data_classes

def center_input() -> 'ForwardGeocodingData':
    'Takes input specifying where to find infromation regarding the center coordinate, and returns a ForwardGeocodingData class from that input'
    center = input()
    if center.startswith('CENTER FILE'):
        return data_classes.LocalForwardGeocodingData(Path(center[12:]))
    elif center.startswith('CENTER NOMINATIM'):
        query_parameters = [('q', f'<{center[17:]}>'), ('format', 'jsonv2')]
        url = f'https://nominatim.openstreetmap.org/search.php?{urllib.parse.urlencode(query_parameters)}'
        return data_classes.OnlineForwardGeocodingData(url)
    else:
        quit()

def range_input() -> int:
    'Returns input regarding max distance from the center as an integer'
    return int(input()[6:])

def threshold_input() -> int:
    'Returns input regarding minimum AQI value as an integer'
    return int(input()[10:])

def max_input() -> int:
    'Returns input regarding max number of results as an integer'
    return int(input()[4:])

def data_input() -> 'AirData':
    'Takes input specifying where to find infromation regarding air quality infromation, and returns a AirData class from that input'
    source = input()
    if source == 'AQI PURPLEAIR':
        return data_classes.OnlineAirData('https://www.purpleair.com/data.json')
    elif source.startswith('AQI FILE'): 
        return data_classes.LocalAirData(Path(source[9:]))
    else:
        quit()

def reverse_input(coordinates: list) -> 'ReverseGeocodingData':
    '''
    Takes input specifying where to find infromation regarding reverse nominatim data, and returns a ReverseGeocodingData class from that input
    If data is to be taken via API requests, uses the coordinates of the locations to be found to find the infromation. 
    '''
    method = input()
    if method.startswith('REVERSE FILES'):
        paths = method[14:].split()
        for i in range(len(paths)):
            paths[i] = Path(paths[i])
        return data_classes.LocalReverseGeocodingData(paths)
    elif method == 'REVERSE NOMINATIM':
        urls = _create_reverse_url_list(coordinates)
        return data_classes.OnlineReverseGeocodingData(urls)
    else:
        quit()

def _create_reverse_url_list(coordinates: list[tuple]) -> list[str]:
    'Generates a list of urls based on coordinate tuples in reverse nominatim query format'
    reverse_base = f'https://nominatim.openstreetmap.org/reverse?'
    reverse_urls = []
    for coordinate in coordinates:
        query_parameters = [('format', 'jsonv2'), ('lat', coordinate[0]), ('lon', coordinate[1])]
        reverse_urls.append(f'{reverse_base}{urllib.parse.urlencode(query_parameters)}')
    return reverse_urls

