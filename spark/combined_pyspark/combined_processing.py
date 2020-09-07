from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession\
    .builder\
    .appName("CombinedProcessing")\
    .config("spark.driver.extraClassPath", "C:\mysql-connector-java-8.0.21\mysql-connector-java-8.0.21.jar")\
    .getOrCreate()

df_meetup = spark.read\
    .format("jdbc")\
    .option("url", "jdbc:mysql://localhost/meetup_db")\
    .option("driver", "com.mysql.jdbc.Driver")\
    .option("dbtable", "meetup_rsvp_table_appended").option("user", "root")\
    .option("password", "admin").load()

df_meetup.createOrReplaceTempView("meetup")

df_agg_meetup = spark.sql(" select neighbourhood, SUM(response_count) as sum_responses from meetup group by neighbourhood ")

df_yelp = spark.read\
    .format("jdbc")\
    .option("url", "jdbc:mysql://localhost/meetup_db")\
    .option("driver", "com.mysql.jdbc.Driver")\
    .option("dbtable", "yelp").option("user", "root")\
    .option("password", "admin").load()

df_yelp.createOrReplaceTempView("yelp")

df_agg_yelp = spark.sql(" select neighbourhood, AVG(rating) as avg_rating, SUM(review_count) as sum_reviews from yelp group by neighbourhood ")

df_incubator = spark.read\
    .format("jdbc")\
    .option("url", "jdbc:mysql://localhost/meetup_db")\
    .option("driver", "com.mysql.jdbc.Driver")\
    .option("dbtable", "incubators").option("user", "root")\
    .option("password", "admin").load()

df_incubator.createOrReplaceTempView("incubator")

df_agg_incubator = spark.sql(" select neighbourhood, COUNT(organization) as incubator_count from incubator group by neighbourhood ")

meetup = df_agg_meetup.alias('meetup')
yelp = df_agg_yelp.alias('yelp')
incubator = df_agg_incubator.alias('incubator')

from pyspark.sql.functions import col

joined_df = yelp.join(meetup, col('yelp.neighbourhood') == col('meetup.neighbourhood'), 'full') \
.join(incubator, col('yelp.neighbourhood') == col('incubator.neighbourhood'), 'full') \
.select('yelp.*', 'meetup.sum_responses', 'incubator.incubator_count')

filtered_df = joined_df.na.fill(0)

filtered_df.createOrReplaceTempView("filtered")

final_df = spark.sql(" select neighbourhood, (CASE WHEN sum_responses < 50 THEN sum_responses ELSE 50 END) as sum_responses, \
avg_rating, sum_reviews, \
incubator_count, (CASE WHEN sum_reviews <= 1000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*1) \
WHEN sum_reviews <= 1000 AND sum_responses >= 50 THEN (50*avg_rating*incubator_count*1) \
WHEN sum_reviews BETWEEN 1000 AND 2000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*2) \
WHEN sum_reviews BETWEEN 1000 AND 2000 AND sum_responses >= 50 THEN (50*avg_rating*incubator_count*2) \
WHEN sum_reviews BETWEEN 2000 AND 3000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*3) \
WHEN sum_reviews BETWEEN 2000 AND 3000 AND sum_responses >= 50 THEN (50*avg_rating*incubator_count*3) \
WHEN sum_reviews BETWEEN 3000 AND 4000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*4) \
WHEN sum_reviews BETWEEN 3000 AND 4000 AND sum_responses >= 50  THEN (50*avg_rating*incubator_count*4) \
WHEN sum_reviews BETWEEN 4000 AND 5000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*5) \
WHEN sum_reviews BETWEEN 4000 AND 5000 AND sum_responses >= 50 THEN (50*avg_rating*incubator_count*5) \
WHEN sum_reviews >= 5000 AND sum_responses < 50 THEN (sum_responses*avg_rating*incubator_count*5) \
WHEN sum_reviews >= 5000 AND sum_responses >= 50  THEN (50*avg_rating*incubator_count*5) \
END) as combined from filtered ")

final_df.write.format('jdbc').options(
      url='jdbc:mysql://localhost/meetup_db',
      driver='com.mysql.jdbc.Driver',
      dbtable='joined_df',
      user='root',
      password='admin').mode('append').save()
