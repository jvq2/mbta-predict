from unittest.mock import Mock

import pytest
import requests

import mbta


@pytest.fixture
def mock_request_json():
    return {'data': ['fooooo']}


@pytest.fixture
def mock_request_obj(mock_request_json):
    return Mock(json=Mock(return_value=mock_request_json))


@pytest.fixture
def mock_requests_get(monkeypatch, mock_request_obj):
    mock_get = Mock(return_value=mock_request_obj)
    monkeypatch.setattr(requests, 'get', mock_get)

    return mock_get


def test_get_routes_calls_request_get(mock_requests_get):
    mbta.get_routes()
    expected_url = 'https://api-v3.mbta.com/routes'
    expected_params = {}
    mock_requests_get.assert_called_once_with(
        expected_url,
        params=expected_params
    )


def test_get_routes_filters_by_route_type(mock_requests_get):
    mbta.get_routes(['2', '3'])
    expected_url = 'https://api-v3.mbta.com/routes'
    expected_params = {'filter[type]': '2,3'}
    mock_requests_get.assert_called_once_with(
        expected_url,
        params=expected_params
    )


def test_get_routes_returns_request_data_key(
    mock_requests_get, mock_request_json
):
    result = mbta.get_routes()
    assert result == mock_request_json['data']


def test_get_stops_calls_request_get(mock_requests_get):
    mbta.get_stops({'id': 'Admiral Ackbar'})
    expected_url = 'https://api-v3.mbta.com/stops'
    expected_params = {'filter[route]': 'Admiral Ackbar'}
    mock_requests_get.assert_called_once_with(
        expected_url,
        params=expected_params
    )


def test_get_stops_returns_request_data_key(
    mock_requests_get, mock_request_json
):
    result = mbta.get_stops({'id': 'Ackbar Ackbar'})
    assert result == mock_request_json['data']


def test_get_predictions_calls_request_get(mock_requests_get):
    mock_route = {'id': 'Admiral'}
    mock_stop = {'id': 'Ackbar'}
    mock_direction_id = 'Trap'
    mbta.get_predictions(mock_route, mock_stop, mock_direction_id)
    expected_url = 'https://api-v3.mbta.com/predictions'
    expected_params = {
        'filter[route]': mock_route['id'],
        'filter[stop]': mock_stop['id'],
        'filter[direction_id]': mock_direction_id,
        'sort': 'departure_time',
        'page[limit]': 1
    }
    mock_requests_get.assert_called_once_with(
        expected_url,
        params=expected_params
    )


def test_get_predictions_returns_request_data_key(
    mock_requests_get, mock_request_json
):
    mock_route = {'id': 'Admiral'}
    mock_stop = {'id': 'Ackbar'}
    mock_direction_id = 'Trap'
    result = mbta.get_predictions(mock_route, mock_stop, mock_direction_id)
    assert result == mock_request_json['data']
