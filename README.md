# Startup Where 

## Demo

The dash app's user interface is shown below:

![alt text](https://github.com/MRazaKazmi/Startup-Where/blob/master/startup-where-ui.png)
## Introduction

Startup Where is an end to end data product comprising of one batch data pipeline and a streaming one. In the batch data pipeline data is extracted from Yelp and contains information about businesses in different Toronto neighbouroods including ratings and review counts. The data is stored in MySQL and then transformed in Spark to be loaded once again into MySQL. In the streaming data pipeline real-time data is ingested from Meetup and stored in Kafka from where it is processed using Spark Structured Streaming and stored in MySQL. The data stored in the MYSQL database is visualzied in a Dash app which displays the Yelp, Meetup and Incubators metrics for each neighbourhood in Toronto. The aim of this visualization is to provide users information on the number of Meetups in each neighbourhood and the ratings and review counts of neighbouring businesses as well as the incubators and accelerators. These metrics may serve as one of the many indicators of where to locate your new startup in Toronto. 

## Explanation of Startup Where View Metrics

There are two main metrics for businesses in each neighborhood. Yelp Average Ratings is the average rating which reviewers attribute to businesses in each neighborhood and Yelp Sum Reviews is the total review count of businesses in each neighborhood. There is one metric for the Meetups in each neighborhood and is the sum of responses to meetups in that neighborhood. For incubators and accelerators, the count of these organizations in each neighbourhood is profiled. A combined view metric is calculated by multiplying the three metrics, binning the Yelp Sum Reviews metric and capping the Meetup Responses metric (please see discussion in Engineering Challenges for more detail).

## Architecture

The architecture of the data pipelines is shown below:

![alt text](https://github.com/MRazaKazmi/Startup-Where/blob/master/pipeline-architecture.png)

### Data Sources 

The data for this project is sourced from four main sources. Profiles of different Toronto neighborhoods are collected from the open data portal on City of Toronto’s website. Data on businesses in each neighborhood is then gathered from the Yelp API. Data for incubators and accelerators in each neighborhood is also collected from the open data portal on City of Toronto’s website. And data is collected in real-time from the Meetup API for responses to meetups in each neighborhood. 

## Repository Structure
```
data
```
This folder contains data for Toronto neighbourhood profiles and Toronto neighbourhood incubators and accelerators.
```
data-collection
```
This folder contains code to extract data for (A) Toronto neighbourhood profiles (B) Toronto neighbourhood businesses and (C) Toronto neighbourhood incubators and accelerators.
```
kafka
```
This folder contains code for producing real-time data in the Kafka broker using the Meetup API and also for consuming this real-time data.
```
spark
```
This folder contains three sub-folders. Streaming contains code for stream processing the meetup data using Spark Structured Streaming in Scala for improving processing speed. Streaming_pyspark enriches the processed meetup stream with additional neighbourhood column using Python library. Combined_pyspark transforms the different data sources into an analytical data file which is stored in MySQL.
```
mysql
```
It conatins table creation sql statements.
```
dash
```
It contains code for visualizing the neighbourhood profiles on a choropleth map of Toronto and using color scale to indicate the strength of Startup Where metrics in each neighbourhood.

## Improvements

This application can be improved by adding more metrics of factors which are important for startup success. One such factor is the number of coworking spaces in each neighbourhood. This can be determined from data from the Coworker API. However, since there is a charge for gathering data from the API, it is not used in this project. Another limitation encountered in the project was limited data on meetup responses in some neighbourhoods and a surge of responses in others. This may be due to a meetup becoming live when data was gathered and hence attracting more responses to that meetup. It is therefore recommended to gather data in the Kafka producer for atleast two weeks to remove effect of such outliers and produce better visualization results.

## Engineering Challenges

When calculating the Meetup responses in each neighborhood, some neighborhoods show a dramatically high number of responses as discussed previously. To reduce this effect, the number of meetup responses for each neighborhood is capped at 50. Another challenge was encountered when calculating the combined metric representing data from all three sources. Since the sum of Yelp reviews is a large number, with a maximum value of 5000, it is divided into 6 equal width bins and a value of 1 assigned to the smallest bin and a value of 6 to the largest bin. This way the combined metric is kept from reaching extremely large values. 

