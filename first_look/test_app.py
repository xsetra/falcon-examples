# -*- coding: utf-8 -*-

import falcon
from falcon import testing
import msgpack
from .app import api
from unittest.mock import mock_open, call
import pytest


@pytest.fixture
def client():
    return testing.TestClient(api)

test_client = client()

def test_list_images():
    expected_response = {
            'images':[
                {'href2':'/images/somethings'}
            ]
        }

    response = test_client.simulate_get('/images')
    response_result = msgpack.unpackb(response.content, encoding='utf-8')

    assert response_result == expected_response
    assert response.status == falcon.HTTP_OK


def test_posted_image_gets_saved(test_client, monkeypatch):
    mock_file_open = mock_open()
    monkeypatch.setattr('io.open', mock_file_open)

    fake_uuid = '123e4567-e89b-12d3-a456-426655440000'
    monkeypatch.setattr('uuid.uuid4', lambda: fake_uuid)

    fake_image_bytes = b'fake-image-bytes'
    response = test_client.simulate_post(
        '/images',
        body=fake_image_bytes,
        headers={'content-type': 'image/png'}
    )

    assert response.status == falcon.HTTP_CREATED
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
    assert response.headers['location'] == '/images/{}.png'.format(fake_uuid)