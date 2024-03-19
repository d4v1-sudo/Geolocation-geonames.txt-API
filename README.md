# X,Y → 🗺️ - Geolocation-geonames.txt-API

This repository contains a set of Python scripts designed to facilitate the retrieval of geographic location information based on various parameters such as latitude and longitude coordinates, city names, country names, and state names.

## Scripts

### gps.py

This script provides a comprehensive functionality to locate the nearest geographic locations based on given latitude and longitude coordinates. It calculates distances to the closest populated place, road/railway, hill/mountain, lake, park, and building. Additionally, it can determine the nearest administrative location (e.g., city, state) based on the provided coordinates.

### get_all_states-codes.py

This utility script extracts state information from geonames data and generates a Python file named `all_states_code.py`. It is employed internally by `gps.py`, `city-gps-location.py` and `state-gps-location.py` to retrieve corresponding name of a state based on its code.

### city-gps-location.py

This script enables users to find the coordinates of a specific city based on its name. It leverages geonames data to perform the city search.

### state-gps-location.py

This script enables users to find the coordinates of a specific state based on its name.

### country-gps-location.py

Users can utilize this script to find the coordinates of a specific country (it makes more sense using allCountries.txt of Geonames).

### all.py

To search for anything in the database, use the following input format: `<x,y>` for coordinates or `<any-string>` for a string. If you search for a coordinate, the script will retrieve the nearest coordinate's location and its information. If the search is for a string, the script will retrieve all locations and their information from the database that contain this string.

## Usage

1. Ensure that you have Python installed on your system.
2. Download the geonames text files from [Geonames](https://www.geonames.org/export/dump) and place them in the repository directory, and change the .txt name file for your own country .txt database in each code you will use.
3. Run the desired Python script according to your location search requirements.

## Requirements

- Python 3.x
- Geonames text files (downloaded from the Geonames website)

## Contributors

- [d4v1-sudo]

Feel free to contribute to this project by adding new features, fixing bugs, improving documentation, or addressing issues. Your contributions are highly appreciated!

If you have any questions or suggestions, please don't hesitate to reach out. Thank you for using Geographic Location Finder!

<a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fd4v1-sudo%2FGeolocation-geonames.txt-API"><img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fd4v1-sudo%2FGeolocation-geonames.txt-API&label=Thanks%20for%20dropping%20in&countColor=%23d9e3f0" /></a>
