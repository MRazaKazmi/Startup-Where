import json
import pandas as pd
import time
import requests
from shapely.geometry import shape
from shapely.geometry import Point
from sqlalchemy import create_engine


path = r'C:\Users\Raza\OneDrive\startup-where\data\Neighbourhoods.geojson'

yelp_api_key = 'inHyZ-C1fBiuRyJ9_8W2ymrKKcN9zu5T-VnuwY6FY7etIjCQawWGEnPpdlTopB99qziU4wT_kcygWGXUYqokWfrHAyTrwMNRNFLlioEfGEGTF1zp8No3WCybEGgBXnYx'



def get_neighbourhoods(path):
    '''For each neighbourhood zone, return neighbourhood name, longitude and latitude'''

    with open(path) as f:
        data = json.load(f)


    cols = ['area name', 'longitude', 'latitude']
    lst = []

    for feature in data['features']:
        area_name = feature['properties']['AREA_NAME']
        longitude = feature['properties']['LONGITUDE']
        latitude = feature['properties']['LATITUDE']
        lst.append([area_name, longitude, latitude])

    neighbourhoods_df = pd.DataFrame(lst, columns=cols)

    return neighbourhoods_df


def get_businesses(neighbourhoods_df):
    '''For each neighbourhood zone, query Yelp API for businesses closest to longitude and latitude'''

    api_key = 'Bearer ' + yelp_api_key
    head = {'Authorization': api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    businesses_df = pd.DataFrame()

    for _, row in neighbourhoods_df.iterrows():
        query = {
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'radius': 2000,
            'limit': 50,
            'sort_by': 'distance'
        }
        response = requests.get(url, headers=head, params=query)
        json = response.json()

        retries = 0
        while retries <= 10 and 'error' in json:
            retries += 1
            time.sleep(1)
            response = requests.get(url, headers=head, params=query)
            json = response.json()
        matches = json['businesses']
        businesses_df = businesses_df.append(matches, ignore_index=True)

    return businesses_df

def add_neighbourhoods(path, businesses_df):
    businesses_df_appended = businesses_df
    neighs = []
    
    with open(path) as f:
            data = json.load(f)

    for coordinates in businesses_df['coordinates']:

        longitude = coordinates['longitude']
        latitude = coordinates['latitude']

        point = Point(longitude, latitude)

        for feature in data['features']:

            polygon = shape(feature['geometry'])

            if polygon.contains(point):

                neighbourhood = feature['properties']['AREA_NAME']

        if neighbourhood is None:

            neighbourhood = "NA"

        neighs.append(neighbourhood)
        
        
    businesses_df_appended['neighbourhood'] = neighs

    return businesses_df_appended


neighbourhoods_df = get_neighbourhoods(path)
businesses_df = get_businesses(neighbourhoods_df)
businesses_df_appended = add_neighbourhoods(path, businesses_df)
businesses_df_final = businesses_df_appended[['name', 'rating', 'review_count', 'neighbourhood']]


engine = create_engine("mysql+pymysql://root:admin@localhost:3306/meetup_db")
con = engine.connect()

businesses_df_final.to_sql(name='yelp', con=engine, if_exists = 'append', index=False)