import pytest
from unittest import mock
from ddos.producer import publish_log_record, apache_log_reader


@mock.patch("ddos.producer.KafkaProducer.send")
def test_publish_log_record(mock_producer):
    topic = "test"
    msg = '200.4.91.190 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"'
    publish_log_record(topic, msg)
    mock_producer.assert_called_with(topic, str.encode(msg))


def test_apache_log_reader(tmp_path):
    dir = tmp_path / "test_apache_log_dir"
    dir.mkdir()
    file_path = dir / "access_log_a"
    test_record_a = '200.4.91.190 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"\n'
    test_record_b = '200.4.91.191 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"\n'
    file_path.write_text("".join([record for record in [test_record_a, test_record_b]]))
    reader = apache_log_reader(file_path)
    results = [line for line in reader]
    assert results[0] == test_record_a
    assert results[1] == test_record_b


if __name__ == "__main__":
    pass
