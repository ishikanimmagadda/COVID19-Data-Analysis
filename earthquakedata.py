
import pandas as pd
import requests
import matplotlib.pyplot as plt

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2023-05-01",
    "endtime": "2023-05-31",
    "minmagnitude": 4.5
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

if response.status_code == 200: 
    features = data["features"]
    # creating a list of property dictionaries 
    properties = [] 
    for feature in features: 
        properties.append(feature["properties"])

    df = pd.DataFrame(properties)
    #converting data frame to .csv stored in earthquakedata.csv
    df.to_csv("earthquakedata.csv", index=False)

    #allowing pandas to read into the csv
    df = pd.read_csv("earthquakedata.csv")

    # seperating time and date 
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['date'] = df['time'].dt.date

    # grouping by date and getting frequency of each date 
    earthquakesPerDay = df.groupby('date').size()

    #line graph 
    plt.figure(figsize=(10, 5))
    plt.plot(earthquakesPerDay.index, earthquakesPerDay.values, marker='o')
    plt.title('Number of Earthquakes per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Earthquakes')
    plt.show()

    #magnitude series, index = magnitude number, values = count 
    magnitudeFrequency = df.groupby('mag').size()

    #bar graph 
    plt.figure(figsize=(10, 5))
    plt.bar(magnitudeFrequency.index, magnitudeFrequency.values, width=0.1)
    plt.title('Frequency of Earthquake Magnitudes')
    plt.xlabel('Magnitude')
    plt.ylabel('Frequency')
    plt.show()

else: 
    print(response.status_code)


