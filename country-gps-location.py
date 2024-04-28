def process_geonames_file(file_path):
    locations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split('\t')
            latitude = float(data[4])
            longitude = float(data[5])
            country = data[8]
            locations.append((latitude, longitude, country, line))  
    return locations

def find_location_with_pcli(locations, country):
    for loc in locations:
        if "pcli" in loc[-1].lower() and country.lower() in loc[-1].lower():
            return loc
    return None

if __name__ == "__main__":
    file_path = input('Txt file: ')
    locations = process_geonames_file(file_path)

    user_country = input("Enter the name of the country: ")

    found_location = find_location_with_pcli(locations, user_country)

    if found_location:
        loc_lat, loc_lon, country, line = found_location
        print("\r")
        print("\033[94mCoordinates found:\033[0m")
        print("Latitude:", loc_lat)
        print("Longitude:", loc_lon)
        print("Country:", country)
        print("Full line:", line)  
    else:
        print("No line contains 'pcli' for the provided country.")
