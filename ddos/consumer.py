"""
This module contains code relevant to the consumer component
in the Kafka environment. Based on the project description's
requirements, the consumer will be responsible for:

1) Consuming the relevant topic messages for DDOS monitoring
2) Parsing the important message bits for the DDOS detection algorithm
3) Implementing the DDOS detection algorithm
4) Storing DDOS candidate IPs for further analysis

The consumer hosts the brains of the DDOS monitoring app
"""
import re
from collections import namedtuple
from config import settings

ApacheLogRecord = namedtuple("ApacheLogRecord", [
    "ip_address",
    "client_id",
    "user_id",
    "timestamp",
    "request",
    "response_status_code",
    "response_size",
    "referer_request_header",
    "user_agent_request_header"
])


class ApacheParserException(ValueError):
    """A custom Exception class for Apache log parsing anomalies"""


def parse_apache_log_record(record):
    """
    Parses an apache access log record and returns a namedtuple

    Notes
    =====
    Assumes Apache's Combined Log Format for record:
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined

    https://httpd.apache.org/docs/current/logs.html#combined
    """
    REGEX_PATTERN = r'\"(.*?)\"|\[(.*?)\]|(\S+)'

    if isinstance(record, bytes):
        record = record.decode("utf-8")
    matches = re.findall(REGEX_PATTERN, record)
    parsed_record = ["".join(match) for match in matches]
    try:
        if len(parsed_record) != 9:
            raise ApacheParserException
        return ApacheLogRecord(*parsed_record)
    except ApacheParserException:
        print(f"Unexpected number of values when unpacking record iterable. Record: {parsed_record}")
        raise


def get_suspect_ips(counter_dict, request_threshold=30):
    """
    Returns a boolean if an ip address has met or exceeded the
    the threshold for occurrences
    """
    suspect_ips = []
    for ip, count in counter_dict.items():
        if count >= request_threshold:
            suspect_ips.append(ip)
    return suspect_ips


if __name__ == "__main__":
    from kafka import KafkaConsumer
    from collections import Counter

    topic = "ddos"
    consumer = KafkaConsumer("ddos", auto_offset_reset="earliest", bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVER])
    counter = Counter()
    for msg in consumer:
        apache_record = parse_apache_log_record(msg.value)
        print(apache_record)
        # counter[apache_record.ip_address] += 1
        # if check_requests_threshold(counter, request_threshold=30):
        #     print(counter[apache_record.ip_address])
