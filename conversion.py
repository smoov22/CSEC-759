import cmath
import glob
import pandas as pd
import os

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

def noise(polar):
    return polar

def main():
    cartesianpile = set()
    data_point(cartesianpile)
    coordinates = list(cartesianpile)
    print(coordinates[1738])
    polars = cartesian_to_polar(coordinates, polars=[])
    print(polars[1738])


main()