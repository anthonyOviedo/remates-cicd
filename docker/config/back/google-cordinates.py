from pyproj import Transformer
import os

# Define transformation from CRTM05 (EPSG:8908) to WGS 84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:8908", "EPSG:4326")

# Coordinates in CRTM05 (X, Y)
#x , y = 455417.0, 1130974.0

import sys

# Ensure correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <PROVINCIA> <MATRICULA>")
    sys.exit(1)

# Get the values from command-line arguments
x_east = sys.argv[1]  # First argument after the script name
y_north = sys.argv[2]  # Second argument

# Print values for verification
print(f"X: {x_east}")
print(f"Y: {y_north}")

# Convert to latitude and longitude
lat, lon = transformer.transform(x_east, y_north)

# Generate Google Maps link
google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"

print(f"Latitude: {lat}, Longitude: {lon}")
print(f"Google Maps: {google_maps_link}")
