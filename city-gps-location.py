def process_geonames_file(file_path):
    locations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split('\t')
            latitude = float(data[4])
            longitude = float(data[5])
            country = data[8]
            state_code = data[10]
            city = data[1]
            region = data[7]
            region_code = data[6]
            locations.append((latitude, longitude, country, state_code, region, region_code, city))
    return locations

try:
    from all_states_code import all_states
except:
    print("Run get_all_states-codes.py")

def find_location_by_city(locations, city):
    for loc in locations:
        loc_lat, loc_lon, country, state_code, region, _, city_name = loc
        if city_name.lower() == city.lower() and region.lower() == "adm2":
            state_name = next((state_info[-1] for state_info in all_states if state_info[3] == state_code), None)
            return loc[:3] + (state_name,) + loc[4:]
    return None

if __name__ == "__main__":
    file_path = input('Txt file: ')
    locations = process_geonames_file(file_path)

    city = input("\033[92mEnter the city name: \033[0m")

    found_location = find_location_by_city(locations, city)

    if found_location:
        loc_lat, loc_lon, country, state, region, region_code, _ = found_location
        print("\r")
        print("\033[94mCoordinates found for the city of", city, ":\033[0m")
        print("Latitude:", loc_lat)
        print("Longitude:", loc_lon)
        print("Country:", country)
        print("State:", state)
        print("Region:", region)
        print("Region Code:", region_code)
    else:
        print("Location for the city of", city, "not found.")
