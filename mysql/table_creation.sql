CREATE TABLE joined_df (
neighbourhood VARCHAR(1000) NOT NULL,
sum_responses INT NOT NULL,
avg_rating double NOT NULL,
sum_reviews INT NOT NULL, 
incubator_count INT NOT NULL, 
combined double NOT NULL);

CREATE TABLE yelp (
neighbourhood VARCHAR(1000) NOT NULL,
rating double NOT NULL,
review_count INT NOT NULL);

CREATE TABLE meetup_rsvp_table (
group_name VARCHAR(1000),
group_city VARCHAR(100),
group_lat double NOT NULL,
group_lon double NOT NULL,
response VARCHAR(10)
response_count INT NOT NULL,
batch_id INT NOT NULL);

CREATE TABLE meetup_rsvp_table_appended (
group_name VARCHAR(1000),
response_count INT NOT NULL,
neighbourhood VARCHAR(100) NOT NULL);

CREATE TABLE incubators (
organization VARCHAR(1000),
neighbourhood VARCHAR(100) NOT NULL);