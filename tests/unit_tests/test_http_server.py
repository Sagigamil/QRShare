import os
import pytest
import requests

from qrshare.HTTPServer import HTTPServer


@pytest.mark.parametrize("port", [9988, 9999, 9876]) 
def test_http_server_sanity(port):
    file_content = b'test file'
    file_name = 'file.txt' 
    server = HTTPServer("", port)
    
    with open(file_name, 'wb') as f:
        f.write(file_content)
    
    url = server.upload(file_name)
    assert requests.get(url).content == file_content

    
@pytest.mark.parametrize("params, error_message", [
    ({"ip": "127.0.0.1"}, 'params has no field \'port\''),
    ({"port": 1020}, 'params has no field \'ip\''),
    ({"ip": "127.0.0.1000", "port": 1020}, 'does not appear to be an IPv4 or IPv6 address'),
    ({"ip": 123, "port": "1020"}, 'param \'ip\' has to be a string'),
    ({"ip": "127.0.0.100", "port": 102000}, 'param \'port\' is invalid'),
]) 
def test_http_server_bad_params(params, error_message):
    try:
        HTTPServer.validate_init_params(**params)
    except ValueError as ex:
        assert error_message in str(ex), f"params given: {params}"
    else:
        assert 0 
       

@pytest.mark.parametrize("params", [
    {"ip": "127.0.0.1", "port" : 1020},
    {"ip": "", "port" : 1020},
]) 
def test_http_server_good_params(params):
    HTTPServer.validate_init_params(**params)

