from kafka import KafkaConsumer
import json
from influx_writer import InfluxWriter
from dotenv import load_dotenv

load_dotenv()

TOPICS = ["drone.stats"]
BOOTSTRAP_SERVERS = ["localhost:9092"]

def handle_stats(data, influx):
    influx.write_stats(data)

TOPIC_HANDLERS = {"drone.stats":handle_stats}

def start_consumer():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None
    )

    influx = InfluxWriter()

    for msg in consumer:
        topic = msg.topic
        print(f'Current topic:{topic}')
        data = msg.value
        handler = TOPIC_HANDLERS.get(topic)

        if handler:
            handler(data, influx)
            print(f"Received: {data}")
        else:
            print(f"No handler for topic: {topic}")


if __name__ == "__main__":
    start_consumer()
