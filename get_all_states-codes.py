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
    populated = None
    state_locations = []  
    
    for loc in locations:
        loc_lat, loc_lon, country, state, region, region_code, region_ori, city = loc
        distance = haversine(latitude, longitude, loc_lat, loc_lon)
        
        if region.lower() == "adm2" and distance < min_distance:
            min_distance = distance
            nearest_location = loc
            
        if region_ori.lower().startswith("ppl") and (nearest_ppl_location is None or distance < min_distance):
            nearest_ppl_location = loc  
            
        if region.lower() == "adm1":  
            state_locations.append(loc)
            
    if nearest_ppl_location:  
        loc_lat, loc_lon, country, state, region, region_code, region_ori, city = nearest_ppl_location
        populated = city
            
    return nearest_location, min_distance, populated, state_locations

if __name__ == "__main__":
    file_path = input('Txt file: ')
    locations = process_geonames_file(file_path)

    print("Please enter geographic coordinates in decimal format.")
    print("For latitude, positive numbers indicate north, and negative numbers indicate south.")
    print("For longitude, positive numbers indicate east, and negative numbers indicate west.")
    print("Example: Latitude 40.7128, Longitude -74.0060")
    print("\r")

    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    nearest_location, distance, populated, state_locations = find_nearest_location(locations, latitude, longitude)
    if nearest_location:
        loc_lat, loc_lon, country, state, region, region_code, region_ori, city = nearest_location
        print("Found coordinates:")
        print("Latitude:", loc_lat)
        print("Longitude:", loc_lon)
        print("Country:", country)
        print("State:", state_locations)
        print("Class:", region)

        if region.lower() == "adm2":
            print("City:", city)

        print("Nearest populated place:", populated)

        if region_code.lower() == "a":
            print("Country/State/Region/City:", city)
        elif region_code.lower() == "r":
            print("Road:", city)
        elif region_code.lower() == "t":
            print("Mountain:", city)
        elif region_code.lower() == "s":
            print("Building:", city)
        elif region_code.lower() == "l":
            print("Park/Area:", city)
        elif region_code.lower() == "h":
            print("Lake/Seaplane Base:", city)

        print("Distance:", round(distance, 2), "km")
        
        # Write the state_locations list to all_states_code.py
        with open('all_states_code.py', 'w') as file:
            file.write("all_states = " + str(state_locations))
    else:
        print("No location found.")
