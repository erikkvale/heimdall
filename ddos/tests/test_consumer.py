import pytest
from collections import Counter
from ..consumer import ApacheParserException, ApacheLogRecord, parse_apache_log_record, check_request_threshold


def test_parse_apache_log_record_returns_namedtuple_of_nine_elements():
    bytes_apache_record = b'200.4.91.190 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"'
    expected_response = ApacheLogRecord(
        ip_address="200.4.91.190", 
        client_id="-", 
        user_id="-", 
        timestamp="25/May/2015:23:11:15 +0000", 
        request="GET / HTTP/1.0", 
        response_status_code="200", 
        response_size="3557",
        referer_request_header="-", 
        user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"
    )
    assert parse_apache_log_record(bytes_apache_record) == expected_response


def test_parse_apache_log_record_raises_exception_if_tuple_unpacking_fails():
    with pytest.raises(ApacheParserException):
        parse_apache_log_record(b'200.4.91.190 - - [25/May/2015:23:11:15 +0000]')


def test_check_request_threshold():
    apache_log_records = [
        ApacheLogRecord(ip_address="200.4.91.190", client_id="-", user_id="-", timestamp="25/May/2015:23:11:15 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
        ApacheLogRecord(ip_address="200.4.91.190", client_id="-", user_id="-", timestamp="25/May/2015:23:11:16 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
        ApacheLogRecord(ip_address="200.4.91.190", client_id="-", user_id="-", timestamp="25/May/2015:23:11:17 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
        ApacheLogRecord(ip_address="198.4.91.180", client_id="-", user_id="-", timestamp="25/May/2015:23:11:17 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
        ApacheLogRecord(ip_address="198.4.91.180", client_id="-", user_id="-", timestamp="25/May/2015:23:11:17 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
        ApacheLogRecord(ip_address="200.4.91.194", client_id="-", user_id="-", timestamp="25/May/2015:23:11:18 +0000", request="GET / HTTP/1.0", response_status_code="200", response_size="3557", referer_request_header="-", user_agent_request_header="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"),
    ]
    counter = Counter()
    suspect_ips = []
    for record in apache_log_records:
        counter[record.ip_address] += 1
        if check_request_threshold(counter, record.ip_address, request_threshold=3):
            suspect_ips.append(record.ip_address)
    assert suspect_ips == ["200.4.91.190"]


if __name__ == "__main__":
    pass