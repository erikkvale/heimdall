"""
This module contains code relevant to the producer component
in the Kafka environment. Based on the project description's 
requirements, the producer will be responsible for:

1) Reading from an Apache log file in a file directory
2) Send each line to Kafka

Right now the producer is pretty dumb and the brains will be in the consumer
"""
from kafka import KafkaProducer
from config import settings

PRODUCER = KafkaProducer(bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVER])


def publish_log_record(topic, message):
    """
    Uses the global KafkaProducer obj to publish the given
    message to the specified topic
    """
    bytes_message = str.encode(message)
    return PRODUCER.send(topic, bytes_message)


def apache_log_reader(file_path):
    """Returns a generator on the file-like object"""
    with open(file_path, mode='r') as f:
        for line in f:
            yield line


if __name__ == "__main__":
    assert PRODUCER.bootstrap_connected()
    reader = apache_log_reader(settings.APACHE_ACCESS_LOG_FILE_PATH)
    for line in reader:
        publish_log_record(settings.KAFKA_TOPIC, line)
