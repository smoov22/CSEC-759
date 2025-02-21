import cmath
import random
import glob
import pandas as pd
import os
import math

SENSITIVITY = 10
EPSILON = 0.05
EARTH_RADIUS_METERS = 111320  # Approximate length of one degree of latitude in meters

def laplace_noise(scale):
    """Generate Laplace noise using inverse transform sampling."""
    u = random.uniform(-0.5, 0.5)
    return -scale * math.copysign(math.log(1 - 2 * abs(u)), u)

def sample_2d_laplace():
    """Sample (r, theta) from a 2D Laplace distribution."""
    b = SENSITIVITY / EPSILON
    r = abs(laplace_noise(b))  # Ensure radius is non-negative
    theta = random.uniform(0, 2 * math.pi)  # Uniformly distributed angle
    return r, theta

def apply_planar_laplace(lat, lon):
    """Apply the Planar Laplace Mechanism to a latitude/longitude coordinate."""
    r, theta = sample_2d_laplace()
    lat_noisy = lat + (r * math.cos(theta)) / EARTH_RADIUS_METERS
    lon_noisy = lon + (r * math.sin(theta)) / (EARTH_RADIUS_METERS * math.cos(math.radians(lat)))
    return lat_noisy, lon_noisy, r, theta

def cartesian_to_polar(lon, lat):
    """Convert Cartesian coordinates (longitude, latitude) to polar (r, theta)."""
    r = math.sqrt(lon**2 + lat**2)
    theta = math.atan2(lat, lon)
    return r, theta

def data_point(cartesianpile, original_coords):
    csv_files = glob.glob('./csec_data/*.csv')
    for file in csv_files:
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            longitude = row.iloc[0]  # First column
            latitude = row.iloc[1]  # Second column
            r_orig, theta_orig = cartesian_to_polar(longitude, latitude)
            noisy_lat, noisy_lon, r, theta = apply_planar_laplace(latitude, longitude)
            cartesianpile.add((noisy_lon, noisy_lat))
            original_coords.append((longitude, latitude, r_orig, theta_orig, r, theta, noisy_lon, noisy_lat))
        print(f"Processed {os.path.basename(file)}")

def main():
    cartesianpile = set()
    original_coords = []
    data_point(cartesianpile, original_coords)
    coordinates = list(cartesianpile)
    print("Original and Transformed Coordinate Sample (Index 1738):")
    print(f"Original (lon, lat): {original_coords[1738][0]}, {original_coords[1738][1]}")
    print(f"Original Polar (r, theta): {original_coords[1738][2]}, {original_coords[1738][3]}")
    print(f"Noisy (r, theta): {original_coords[1738][4]}, {original_coords[1738][5]}")
    print(f"Noisy (lon, lat): {original_coords[1738][6]}, {original_coords[1738][7]}")

    df_output = pd.DataFrame(original_coords, columns=["Longitude", "Latitude", "Original r", "Original Theta", "Noise r", "Noise Theta", "Perturbed Longitude", "Perturbed Latitude"])
    df_output.to_csv("perturbed_data.csv", index=False)
    print("CSV file 'perturbed_data.csv' created with transformed data.")

    df_output_filtered = df_output[["Longitude", "Latitude", "Perturbed Longitude", "Perturbed Latitude"]]
    df_output_filtered.to_csv("perturbed_data_filtered.csv", index=False)
    print("CSV file 'perturbed_data_filtered.csv' created without polar columns.")

main()
