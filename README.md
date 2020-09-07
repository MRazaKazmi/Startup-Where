# Startup Where 

Startup Where is an end to end data pipeline comprising of one batch data component and a streaming one. In the batch data pipeline data is extracted from Yelp and contains information about businesses in different Toronto neighbouroods including ratings and review counts. The data is stored in MongoDB and then transformed in Spark to be loaded once again into MongoDB. In the streaming data pipeline real time data is ingested from Meetup and stored in Kafka from where it is processed using Spark Structured Streaming and stored in MongoDB. The data stored in the databases is visualzied in a Dash web app which displays the Yelp and Meetup views for each neighbourhood in Toronto. The aim of this visualization is to provide users information on the number of Meetups in each neighbourhood and the ratings and review counts of neighbouring businesses. These metrics may serve as one of the many indicators of where to locate your new startup in Toronto. 


![alt text](https://github.com/MRazaKazmi/Startup-Where/blob/master/startup-where-ui.png)


### Architecture of Data Pipelines 

The architecture of the data pipelines is shown below.

![alt text](https://github.com/MRazaKazmi/Startup-Where/blob/master/pipeline-architecture.png)


### Technologies Used and Reasons 

MySQL,
Kafka,
Spark, 
Spark structured Streaming, 
Dash,

### Batch Data Pipeline



### Streaming Data Pipeline
