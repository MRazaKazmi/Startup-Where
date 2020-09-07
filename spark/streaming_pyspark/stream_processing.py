from pyspark.sql import SparkSession
import pandas as pd
import json
from shapely.geometry import shape
from shapely.geometry import Point
from pyspark.sql.functions import udf
from pyspark.sql.types import *

spark = SparkSession\
    .builder\
    .appName("StreamProcessing")\
    .config("spark.driver.extraClassPath", "C:\mysql-connector-java-8.0.21\mysql-connector-java-8.0.21.jar")\
    .getOrCreate()

df_mysql = spark.read\
    .format("jdbc")\
    .option("url", "jdbc:mysql://localhost/meetup_db")\
    .option("driver", "com.mysql.jdbc.Driver")\
    .option("dbtable", "meetup_rsvp_table").option("user", "root")\
    .option("password", "admin").load()

def get_neighbourhood(lon, lat):
        path = r'C:\Users\Raza\OneDrive\startup-where\data\Neighbourhoods.geojson'

        with open(path) as f:
                data = json.load(f)

        point = Point(lon, lat)

        for feature in data['features']:

                polygon = shape(feature['geometry'])

                if polygon.contains(point):
                        neighbourhood = feature['properties']['AREA_NAME']

        if neighbourhood is None:
                neighbourhood = "NA"

        else:
                neighbourhood = neighbourhood

        return neighbourhood

udfGetNeighbourhood = udf(get_neighbourhood, StringType())

df_with_neighbourhood = df_mysql.withColumn("neighbourhood", udfGetNeighbourhood("group_lon", "group_lat"))

cols = ['group_name','response_count','neighbourhood']

df_final = df_with_neighbourhood.select(*cols)

df_final.write.format('jdbc').options(
      url='jdbc:mysql://localhost/meetup_db',
      driver='com.mysql.jdbc.Driver',
      dbtable='meetup_rsvp_table_appended',
      user='root',
      password='admin').mode('append').save()