import json
import urllib.parse
import urllib.request
from pathlib import Path
import calculations
import time

class LocalAirData:
    def __init__(self, path: Path) -> dict:
        '''
        Reads and stores the data section of the json information of a previous purpleair api request
        Also saves the path where the information was gotten from
        '''
        try:
            self._data = _read_local_json(path)['data']
        except (KeyError, TypeError):
            _format_error(path)
        self._path = path

    def aqi_coordinate_dictionary(self) -> dict:
        '''
        Creates a dictionary of all coordinates found within a purpleair data file in correspondence to AQI. AQI
        is calculated by converting the pm values found within the data file associated with each coordinate. 
        '''
        pairs = dict()
        for sublist in _filter_data(self._data):
            try:
                coordinate = (sublist[27], sublist[28])
                pairs[coordinate] = calculations.calculate_aqi(sublist[1])
            except:
                _format_error(self._path)
        return pairs

class OnlineAirData:
    def __init__(self, url: str):
        '''
        Reads and stores the data section of the json information of a purpleair api request
        Also saves the url where the information was gotten from
        '''
        try:
            self._data = _read_api_json(url)['data']
        except (KeyError, TypeError):
            _format_error(url)
        self._url = url

    def aqi_coordinate_dictionary(self) -> dict:
        '''
        Creates a dictionary of all coordinates based on data found via the purpleair API in correspondence to AQI. AQI
        is calculated by converting the pm values found within the purpleair API data associated with each coordinate. 
        '''
        pairs = dict()
        for sublist in _filter_data(self._data):
            try:
                coordinate = (sublist[27], sublist[28])
                pairs[coordinate] = calculations.calculate_aqi(sublist[1])
            except:
                _format_error(self._url)
        return pairs

class LocalForwardGeocodingData:
    def __init__(self, center: Path):
        '''
        Reads and stores the json information of a previous forward geocoding api request
        Also saves the path where the information was gotten from
        '''
        try:
            self._information = _read_local_json(center)[0]
        except (KeyError, IndexError, TypeError):
            _format_error(center)
        self._path = center

    def coordinates(self) -> tuple[float]:
        'Returns a the coordinates of a reverse nominatim result in tuple format.'
        try:
            lat = float(self._information['lat'])
            lon = float(self._information['lon'])
            return lat, lon
        except:
            _format_error(self._path)

    def pretty_coordinate(self) -> str:
        'Retunrs the coordinate of a reverse nominatim result in a readable string fromat'
        return 'CENTER ' + calculations.format_coordinate(LocalForwardGeocodingData.coordinates(self))

class LocalReverseGeocodingData:
    def __init__(self, reverse_files: list[Path]):
        self._reverse_files = reverse_files

    def reverse_location_descriptions(self) -> list[str]:
        'Generates a list of descriptions of a series of reverse nominatim results'
        descriptions = []
        for path in self._reverse_files:
            try:
                result = _read_local_json(path)
                name = result['display_name']
            except:
                _format_error(path)
            descriptions.append(name)
        return descriptions

class OnlineForwardGeocodingData:
    def __init__(self, center: str):
        '''
        Reads and stores the json information of a forward geocoding api request
        Also saves the url where the information was gotten from
        '''
        try:
            self._information = _read_api_json(center)[0]
        except (KeyError, IndexError, TypeError):
            _format_error(center)
        self._url = center

    def coordinates(self) -> tuple[float]:
        'Returns a the coordinates of a reverse nominatim result in tuple format.'
        try:
            lat = float(self._information['lat'])
            lon = float(self._information['lon'])
            return lat, lon
        except:
            _format_error(self._url)

    def pretty_coordinate(self) -> str:
        'Retunrs the coordinate of a reverse nominatim result in a readable string fromat'
        return 'CENTER ' + calculations.format_coordinate(LocalForwardGeocodingData.coordinates(self))

class OnlineReverseGeocodingData:
    def __init__(self, reverse_urls: list[str]):
        self._reverse_urls = reverse_urls

    def reverse_location_descriptions(self) -> list[str]:
        'Generates a list of descriptions of a series of reverse nominatim results'
        descriptions = []
        for url in self._reverse_urls:
            try:
                result = _read_api_json(url)
                time.sleep(1)
                name = result['display_name']
            except:
                _format_error(url)
            descriptions.append(name)
        return descriptions

def _read_local_json(path: Path) -> dict:
    'Reads json text from a file and returns it as a Python dictionary.'
    json_text = None
    try:
        json_text = path.open(encoding='utf-8')
        result = json.load(json_text)
        return result
    except json.decoder.JSONDecodeError:
        _format_error(path)
    except FileNotFoundError:
        print('FAILED')
        print(path)
        print('MISSING')
        quit()
    finally:
        if json_text != None:
            json_text.close()

def _read_api_json(url: str) -> dict:
    'Reads json text from an API request and returns it as a Python dictionary.'
    response = None
    try:
        request = urllib.request.Request(url, headers={'Referer':'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/mattheqd'})
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    except urllib.error.HTTPError as e:
        print('FAILED')
        print(e.status, url)
        print('Not 200')
        quit()
    except json.decoder.JSONDecodeError:
        _format_error(url)
    except urllib.error.URLError:
        print('FAILED')
        print(url)
        print('NETWORK')
        quit()
    finally:
        if response != None:
            response.close()

def _format_error(source) -> None:
    'Returns a format error'
    if type(source) == str:
        print('FAILED')
        print(200, source)
        print('FORMAT')
        quit()
    else:
        print('FAILED')
        print(source)
        print('FORMAT')
        quit()
    
def _filter_data(data: dict) -> dict:
    'Filters purpleair data to exclude those with no pm value, outdated infromation, indoor sensors, no latitude, and/or no longitude'
    filtered_list = []
    for sublist in data:
        if sublist[1] == None:
            pass
        elif sublist[4] == None or sublist[4] > 3600:
            pass
        elif sublist[25] != 0:
            pass
        elif sublist[27] == None:
            pass
        elif sublist[28] == None:
            pass
        else:
            filtered_list.append(sublist)
    return filtered_list

