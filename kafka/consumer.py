from kafka import KafkaConsumer

kafka_topic_name = "meetuprsvptopic"
kafka_bootstrap_servers = 'localhost:9092'

consumer = KafkaConsumer(bootstrap_servers=[kafka_bootstrap_servers])
consumer.subscribe([kafka_topic_name])

for message in consumer:
 	print (message)