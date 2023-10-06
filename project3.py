import calculations
import input

def filter_dict_from_range_and_threshold(center: 'Center', d: dict, range: int, threshold: int) -> list[tuple]:
    '''
    Returns a list of coordiantes that are within a certain range from the center calculated via
    equirectangular approximation and that are greater than or equal to a certain AQI value denoted by threshold found by
    the the corresponding value of the coordiante found in the dictionary d. 
    '''
    possible_coords = []
    for coordinate in d.keys():
        if calculations.equirectangular_approximation(center.coordinates(), coordinate) <= range and d[coordinate] >= threshold:
            possible_coords.append(coordinate)
    return possible_coords

def top_coords(coords: list[tuple], d: dict, max: int) -> list[tuple]:
    '''
    Returns a list of the top n coordinates based on AQI value, with n being an integer denoted by max, in order from highest to lowest
    '''
    sorted_coords = sorted(coords, key=lambda x: d[x], reverse=True)
    top_coordinates = []
    for i in range(max):
        top_coordinates.append(sorted_coords[i])
    return top_coordinates

def generate_final_report():
    center = input.center_input()
    max_range = input.range_input()
    threshold = input.threshold_input()
    max = input.max_input()
    data = input.data_input()
    d = data.aqi_coordinate_dictionary()
    possible_coords = filter_dict_from_range_and_threshold(center,d,max_range,threshold)
    top_coordinates = top_coords(possible_coords, d, max)
    reverse = input.reverse_input(top_coordinates)
    descriptions = reverse.reverse_location_descriptions()

    print(center.pretty_coordinate())
    for location in range(len(top_coordinates)):
        print('AQI', d[top_coordinates[location]])
        print(calculations.format_coordinate(top_coordinates[location]))
        print(descriptions[location])

if __name__ == '__main__':
    generate_final_report()

