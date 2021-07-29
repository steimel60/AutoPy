import pandas as pd

location = r'Z:\J8288 McLamb & Sons Construction\GPS\GCP.csv'

df = pd.read_csv(location)
columns = df.columns

for column in columns:
    if 'latitude' in column.lower():
        lat = df[column]
        print(lat)
#df2 = df[['OBJECTID', 'Latitude', 'Longitude', 'Altitude']].copy().dropna()
print(df.columns)
