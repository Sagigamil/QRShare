import os
import pytest
import requests

from qrshare.QRView import QRView


@pytest.mark.parametrize("params, error_message", [
    ({"key": "value"}, 'not expect params, but params were given'),
]) 
def test_http_server_bad_params(params, error_message):
    try:
        QRView.validate_init_params(**params)
    except ValueError as ex:
        assert error_message in str(ex), f"params given: {params}"
    else:
        assert 0 
       

@pytest.mark.parametrize("params", [{}]) 
def test_http_server_good_params(params):
    QRView.validate_init_params(**params)

