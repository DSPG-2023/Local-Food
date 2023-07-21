import pandas as pd
from geopy.geocoders import GoogleV3

# Initialize the geocoder with API key
geolocator = GoogleV3(api_key='AIzaSyAulRtcIoabDRf5NoC0Ek45xKL8S30Qsak')

data = pd.read_csv("demand_supply_lat_long_data.csv")

rows = len(data["County Name"])

for i in range(rows):
    Name = data["County Name"][i] + ", Iowa, USA"
    location = geolocator.geocode(Name)
    print(location)
    data.at[i,"Lattitude"] = location[1][0]
    data.at[i,"Longitude"] = location[1][1]

data.to_csv("demand_supply_lat_long_data.csv", index=False)