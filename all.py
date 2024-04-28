import math

def process_geonames_file(search_input, file_path):
    locations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split('\t')
            latitude = float(data[4])
            longitude = float(data[5])
            country = data[8]
            state_code = data[10]
            if "," in search_input:
                name = data[1]
            else:
                name = data[1] + ", " + data[2] + ", " + data[3]
            region = data[6]
            sub_region = data[7]
            approximate_population = data[14]
            approximate_elevation = data[15]
            locations.append((latitude, longitude, country, state_code, sub_region, region, approximate_elevation, approximate_population, name))  
    return locations

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest_location(locations, search_input):
    if "," in search_input:
        latitude, longitude = map(float, search_input.split(","))
        is_coordinate = True
    else:
        place_name = search_input.lower()
        is_coordinate = False
        distance = None
    
    min_distance = float('inf')
    nearest_location = None
    nearest_ppl_location = None
    nearest_road_location = None
    nearest_mountain_location = None
    nearest_lake_location = None
    nearest_park_location = None
    nearest_building_location = None

    ppl_distance = float('inf')
    road_distance = float('inf')
    mountain_distance = float('inf')
    lake_distance = float('inf')
    park_distance = float('inf')
    building_distance = float('inf')

    try:
        from all_states_code import all_states
    except:
        print("\033[91mError finding all_states_code.py, run get_all_states-codes.py\033[0m")

    for loc in locations:
        loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = loc

        if is_coordinate:
            distance = haversine(latitude, longitude, loc_lat, loc_lon)
        else:
            if (place_name in country.lower() or
                place_name in state_code.lower() or
                place_name in sub_region.lower() or
                place_name in region.lower() or
                place_name in name.lower()):
                distance = 0
            else:
                distance = None

        if distance is not None:
            if sub_region.lower() == "adm2":
                if distance < min_distance:
                    min_distance = distance
                    nearest_location = loc
            elif sub_region.lower().startswith("ppl") and distance < ppl_distance:
                ppl_distance = distance
                nearest_ppl_location = loc
            elif region.lower() == "r" and distance < road_distance:
                road_distance = distance
                nearest_road_location = loc
            elif region.lower() == "t" and distance < mountain_distance:
                mountain_distance = distance
                nearest_mountain_location = loc
            elif region.lower() == "h" and distance < lake_distance:
                lake_distance = distance
                nearest_lake_location = loc
            elif region.lower() == "l" and distance < park_distance:
                park_distance = distance
                nearest_park_location = loc
            elif region.lower() == "s" and distance < building_distance:
                building_distance = distance
                nearest_building_location = loc
                
    if nearest_ppl_location:
        loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = nearest_ppl_location
        populated = name
        
    state_name = None
    for state_info in all_states:
        if state_info == state_code:
            state_name = state_info[-1]
            break

    return (nearest_location, min_distance), (nearest_ppl_location, ppl_distance), (nearest_road_location, road_distance), (nearest_mountain_location, mountain_distance), (nearest_lake_location, lake_distance), (nearest_park_location, park_distance), (nearest_building_location, building_distance), state_name, is_coordinate


if __name__ == "__main__":
    file_path = input("Txt file: ")

    print("Please enter the geographic coordinates in decimal format or the name of a place.")
    print("For latitude, positive numbers indicate north, and negative numbers indicate south.")
    print("For longitude, positive numbers indicate east, and negative numbers indicate west.")
    print("Example: Latitude 40.7128, Longitude -74.0060")
    print("\r")

    search_input = input("\033[92mEnter latitude and longitude separated by comma or the name of a place: \033[0m")
    locations = process_geonames_file(search_input, file_path)

    nearest_location, nearest_ppl_location, nearest_road_location, nearest_mountain_location, nearest_lake_location, nearest_park_location, nearest_building_location, state_name, is_coordinate = find_nearest_location(locations, search_input)

    if is_coordinate:
        loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = nearest_location[0]
        print("\r")
        print("\033[94mClosest coordinates found:\033[0m")
        print("Latitude:", loc_lat)
        print("Longitude:", loc_lon)
        print("Country:", country)
        print("State:", state_name)
        print("City:", name)
        print("Approximate elevation:", approximate_elevation + "m")
        print("Approximate population:", approximate_population)
        print("\r")
        print("\033[94mClosest points found from your provided point:\033[0m")
        print("Nearest populated place:", nearest_ppl_location[0][-1])
        print("Nearest road/railway:", nearest_road_location[0][-1])
        print("Nearest hill/mountain/rock:", nearest_mountain_location[0][-1])
        print("Nearest lake:", nearest_lake_location[0][-1])
        print("Nearest park:", nearest_park_location[0][-1])
        print("Nearest building:", nearest_building_location[0][-1])
        print("\r")
        print("\033[94mDistances between your provided point and places:\033[0m")
        print("Distance to found coordinates:", round(nearest_location[1], 2), "km")
        print("Distance to nearest populated place:", round(nearest_ppl_location[1], 2), "km")
        print("Distance to nearest road/railway:", round(nearest_road_location[1], 2), "km")
        print("Distance to nearest hill/mountain/rock:", round(nearest_mountain_location[1], 2), "km")
        print("Distance to nearest lake:", round(nearest_lake_location[1], 2), "km")
        print("Distance to nearest park:", round(nearest_park_location[1], 2), "km")
        print("Distance to nearest building:", round(nearest_building_location[1], 2), "km")
    else:
        def new_find_nearest_location(locations, search_input):
            matching_locations = []
            process_geonames_file(search_input, file_path)
            
            for loc in locations:
                loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = loc
        
                if (search_input.lower() in country.lower() or
                    search_input.lower() in state_code.lower() or
                    search_input.lower() in sub_region.lower() or
                    search_input.lower() in region.lower() or
                    search_input.lower() in name.lower()):
                    matching_locations.append(loc)
        
            return matching_locations

        matching_locations = new_find_nearest_location(locations, search_input)
    
        if matching_locations:
            from all_states_code import all_states
            print("\r")
            print("Found coordinates:")
            for loc in matching_locations:
                loc_lat, loc_lon, country, state, sub_region, region, approximate_elevation, approximate_population, name = loc
                state_name = None
                for state_info in all_states:
                    if state_info[3] == state:
                        state_name = state_info[-1]
                        break

                try:
                    location_var = ""
                    if region.lower() == "a":
                        location_var = "Country, state, region:"
                    elif region.lower() == "h":
                        location_var = "Stream, lake, river:"
                    elif region.lower() == "l":
                        location_var = "Park, area:"
                    elif region.lower() == "p":
                        location_var = "City, village:"
                    elif region.lower() == "r":
                        location_var = "Road, railway:"
                    elif region.lower() == "s":
                        location_var = "Point, building, farm:"
                    elif region.lower() == "t":
                        location_var = "Mountain, hill, rock:"
                    elif region.lower() == "u":
                        location_var = "Sea: "
                    elif region.lower() == "v":
                        location_var = "Forest:"
                    else:
                        location_var = None
                
                    print("Latitude:", loc_lat)
                    print("Longitude:", loc_lon)
                    print("Country:", country)
                    print("State:", state_name)
                    print(location_var , name)
                    print("Approximate elevation:", approximate_elevation + "m")
                    print("Approximate population:", approximate_population)
                    print("\r")
                except:
                    print("Error finding information for this location.")
        else:
            print("No locations found.")
