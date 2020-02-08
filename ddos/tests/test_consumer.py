import pytest
from ..consumer import ApacheParserException, ApacheLogRecord, parse_apache_log_record


bytes_apache_record = b'200.4.91.190 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"'


def test_parse_apache_log_record_returns_namedtuple_of_nine_elements():
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


if __name__ == "__main__":
    pass