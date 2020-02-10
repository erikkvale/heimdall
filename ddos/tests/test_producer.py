from unittest import mock
from ddos.producer import publish_log_record


@mock.patch("ddos.producer.KafkaProducer.send")
def test_publish_log_record(mock_producer):
    topic = "test"
    msg = "test message"
    publish_log_record(topic, msg)
    mock_producer.assert_called_with(topic, str.encode(msg))



if __name__ == "__main__":
    pass
