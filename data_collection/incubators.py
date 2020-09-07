import pandas as pd
import geocoder
import pymysql
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim
import json
from shapely.geometry import shape
from shapely.geometry import Point


path = r'C:\Users\Raza\OneDrive\startup-where\data\Neighbourhoods.geojson'

def get_incubators():

    incubators_df = pd.read_csv(r'C:\Users\Raza\OneDrive\startup-where\data\business-incubation-csv.csv')

    return incubators_df

def get_geocoder(street_address):

    city = 'Toronto, Canada'
    address = street_address + ', ' + city
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    
    return latitude,longitude

def add_coordinates(incubators_df):

    incubators_df['Latitude'], incubators_df['Longitude'] = zip(*incubators_df['Street Address'].apply(get_geocoder))

    return incubators_df

def add_neighbourhood(incubators_df):

    neighs = []
    neighbourhood = None

    with open(path) as f:
            data = json.load(f)

    for index, row in incubators_df.iterrows():

        longitude = row['Longitude']
        latitude = row['Latitude']
        point = Point(longitude, latitude)
        
        neighbourhood = None

        for feature in data['features']:
            polygon = shape(feature['geometry'])

            if polygon.contains(point):
                neighbourhood = feature['properties']['AREA_NAME']

        if neighbourhood is None:
            neighbourhood = "NA"

        neighs.append(neighbourhood)
        
    incubators_df['Neighbourhood'] = neighs

    return incubators_df


incubators_df = get_incubators()
filtered_df = incubators_df[incubators_df['Street Address'].notnull()]
filtered_df = filtered_df[filtered_df['Postal Code'].notnull()]
incubators_df_appeneded = add_coordinates(filtered_df)
incubators_df_appeneded = add_neighbourhood(incubators_df_appeneded)
incubators_df_final = incubators_df_appeneded[['Organization', 'Neighbourhood']]

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/meetup_db")
con = engine.connect()

incubators_df_final.to_sql(name='incubators', con=engine, if_exists = 'append', index=False)