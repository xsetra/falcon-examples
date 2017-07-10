# -*- coding: utf-8 -*-

import falcon
from falcon import testing
import msgpack
from .app import api


def test_list_images():
    expected_response = {
            'images':[
                {'href2':'/images/somethings'}
            ]
        }
    test_client = testing.TestClient(api)

    response = test_client.simulate_get('/images')
    response_result = msgpack.unpackb(response.content, encoding='utf-8')

    assert response_result == expected_response
    assert response.status == falcon.HTTP_OK
