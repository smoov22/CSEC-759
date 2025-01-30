import cmath
import numpy
import glob
import pandas as pd
import os

SENSITIVITY = 1
EPSILON = 0.5

def data_point(cartesianpile):
    csv_files = glob.glob('./csec_data/*.csv')
    for file in csv_files:
        # Read the CSV file
        df = pd.read_csv(file)
    # Convert each row to [longitude, latitude] and append to cartesianpile
        for index, row in df.iterrows():
            longitude = row.iloc[0]  # First column
            latitude = row.iloc[1]  # Second column
            cartesianpile.add((longitude, latitude))
    
        print(f"Processed {os.path.basename(file)}")

def cartesian_to_polar(coordinates, polars):
    for coordinate in coordinates:
        r, theta = cmath.polar(complex(coordinate[0], coordinate[1]))
        polars.append((r,theta))
    return polars

def polar_to_cartesian(polars):
    coordinates = []
    for polar in polars:
        r, theta = polar[0], polar[1]
        c = cmath.rect(r, theta)
        coordinates.append((c.real, c.imag))
    return coordinates

def noise(polars):
    b = SENSITIVITY/EPSILON
    n = len(polars)
    altered = []
    # replace with a real laplace function
    noise_values = numpy.random.laplace(0, b, n)
    for (r, theta), noise in zip(polars, noise_values):
        noisy_r = r + noise
        altered.append((noisy_r, theta))
    return altered


def main():
    cartesianpile = set()
    data_point(cartesianpile)
    coordinates = list(cartesianpile)
    print(coordinates[1738])
    polars = cartesian_to_polar(coordinates, polars=[])
    print(polars[1738])
    noise_polars = noise(polars)
    print(noise_polars[1738])
    noise_coordinates = polar_to_cartesian(polars)
    print(noise_coordinates[1738])


main()