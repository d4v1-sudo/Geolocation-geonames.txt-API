import math

def process_geonames_file(file_path):
    locations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split('\t')
            latitude = float(data[4])
            longitude = float(data[5])
            country = data[8]
            state = data[10]
            city = data[1]
            region = data[7]
            region_code = data[6]
            region_ori = data[7]
            locations.append((latitude, longitude, country, state, region, region_code, region_ori, city))  
    return locations

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
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

def find_nearest_location(locations, latitude, longitude):
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

    # Load the list of states from the file all_states_code.py
    try:
        from all_states_code import all_states
    except:
        print("\033[91mError finding all_states_code.py, run get_all_states-codes.py\033[0m")

    for loc in locations:
        loc_lat, loc_lon, country, state_code, region, region_code, region_ori, city = loc
        distance = haversine(latitude, longitude, loc_lat, loc_lon)
        
        if region.lower() == "adm2":
            if distance < min_distance:
                min_distance = distance
                nearest_location = loc
        elif region_ori.lower().startswith("ppl") and distance < ppl_distance:
            ppl_distance = distance
            nearest_ppl_location = loc
        elif region_code.lower() == "r" and distance < road_distance:
            road_distance = distance
            nearest_road_location = loc
        elif region_code.lower() == "t" and distance < mountain_distance:
            mountain_distance = distance
            nearest_mountain_location = loc
        elif region_code.lower() == "h" and distance < lake_distance:
            lake_distance = distance
            nearest_lake_location = loc
        elif region_code.lower() == "l" and distance < park_distance:
            park_distance = distance
            nearest_park_location = loc
        elif region_code.lower() == "s" and distance < building_distance:
            building_distance = distance
            nearest_building_location = loc
            
    if nearest_ppl_location:
        loc_lat, loc_lon, country, state_code, region, region_code, region_ori, city = nearest_ppl_location
        populated = city
        
    # Find the state name from the code
    state_name = None
    for state_info in all_states:
        if state_info[3] == state_code:
            state_name = state_info[-1]
            break
            
    return (nearest_location, min_distance), (nearest_ppl_location, ppl_distance), (nearest_road_location, road_distance), (nearest_mountain_location, mountain_distance), (nearest_lake_location, lake_distance), (nearest_park_location, park_distance), (nearest_building_location, building_distance), state_name

if __name__ == "__main__":
    file_path = input('Txt file: ')
    locations = process_geonames_file(file_path)

    print("Please enter geographic coordinates in decimal format.")
    print("For latitude, positive numbers indicate north, and negative numbers indicate south.")
    print("For longitude, positive numbers indicate east, and negative numbers indicate west.")
    print("Example: Latitude 40.7128, Longitude -74.0060")
    print("\r")

    latitude = float(input("\033[92mEnter latitude: \033[0m"))
    longitude = float(input("\033[92mEnter longitude: \033[0m"))

    nearest_location, nearest_ppl_location, nearest_road_location, nearest_mountain_location, nearest_lake_location, nearest_park_location, nearest_building_location, state_name = find_nearest_location(locations, latitude, longitude)

    if nearest_location[0]:
        loc_lat, loc_lon, country, state, region, region_code, region_ori, city = nearest_location[0]
        print("\r")
        print("\033[94mClosest coordinates found:\033[0m")
        print("Latitude:", loc_lat)
        print("Longitude:", loc_lon)
        print("Country:", country)
        print("State:", state_name)
        print("City:", city)
        print("\r")
        print("\033[94mClosest points found from your provided point:\033[0m")
        print("Nearest populated place:", nearest_ppl_location[0][-1])
        print("Nearest road/railway:", nearest_road_location[0][-1])
        print("Nearest hill/rock/mountain:", nearest_mountain_location[0][-1])
        print("Nearest lake:", nearest_lake_location[0][-1])
        print("Nearest park:", nearest_park_location[0][-1])
        print("Nearest building:", nearest_building_location[0][-1])
        print("\r")
        print("\033[94mDistances between your provided point and places:\033[0m")
        print("Distance to found coordinate:", round(nearest_location[1], 2), "km")
        print("Distance to nearest populated place:", round(nearest_ppl_location[1], 2), "km")
        print("Distance to nearest road/railway:", round(nearest_road_location[1], 2), "km")
        print("Distance to nearest hill/rock/mountain:", round(nearest_mountain_location[1], 2), "km")
        print("Distance to nearest lake:", round(nearest_lake_location[1], 2), "km")
        print("Distance to nearest park:", round(nearest_park_location[1], 2), "km")
        print("Distance to nearest building:", round(nearest_building_location[1], 2), "km")
    else:
        print("No location found.")
