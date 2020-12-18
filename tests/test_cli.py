from unittest.mock import Mock

import pytest

import cli


@pytest.fixture
def mock_get_choice(monkeypatch):
    mock = Mock(return_value=0)
    monkeypatch.setattr(cli, 'get_choice', mock)
    return mock


@pytest.fixture
def mock_routes():
    return [{
        'id': 'Red',
        'attributes': {
            'long_name': 'foo',
            'direction_destinations': ['north pole', 'south pole'],
            'direction_names': ['north', 'south']
        }
    }]


@pytest.fixture
def mock_stops():
    return [{
        'id': 'middle',
        'attributes': {
            'name': 'foo',
            'address': 'north pole'
        }
    }]


@pytest.fixture
def mock_predictions():
    return [{
        'attributes': {
            'departure_time': '2020-12-17T18:41:05-05:00',
        }
    }]


@pytest.fixture
def mock_get_input(monkeypatch):
    mock = Mock(return_value=0)
    monkeypatch.setattr(cli, 'get_input', mock)
    return mock


@pytest.fixture
def mock_mbta(monkeypatch, mock_routes, mock_stops, mock_predictions):
    mocks = {
        'get_routes': Mock(return_value=mock_routes),
        'get_stops': Mock(return_value=mock_stops),
        'get_predictions': Mock(return_value=mock_predictions)
    }

    monkeypatch.setattr(cli, 'get_routes', mocks['get_routes'])
    monkeypatch.setattr(cli, 'get_stops', mocks['get_stops'])
    monkeypatch.setattr(cli, 'get_predictions', mocks['get_predictions'])

    return mocks


@pytest.fixture
def mock_cli_funcs(monkeypatch, mock_routes, mock_stops, mock_predictions):
    mocks = {
        'choose_route': Mock(return_value=mock_routes[0]),
        'choose_stop': Mock(return_value=mock_stops[0]),
        'choose_direction': Mock(return_value=0),
        'show_prediction': Mock(),
    }

    monkeypatch.setattr(cli, 'choose_route', mocks['choose_route'])
    monkeypatch.setattr(cli, 'choose_stop', mocks['choose_stop'])
    monkeypatch.setattr(cli, 'choose_direction', mocks['choose_direction'])
    monkeypatch.setattr(cli, 'show_prediction', mocks['show_prediction'])

    return mocks


def test_choose_route_calls_get_choice(mock_get_choice, mock_routes):
    cli.choose_route(mock_routes)

    msg = 'Which route would you like? Type the route index:'
    mock_get_choice.assert_called_once_with(msg, mock_routes)


def test_choose_stop_calls_get_choice(mock_get_choice, mock_stops):
    cli.choose_stop(mock_stops)

    msg = 'Which stop would you like? Type the stop index:'
    mock_get_choice.assert_called_once_with(msg, mock_stops)


def test_choose_direction_calls_get_choice(mock_get_choice, mock_routes):
    cli.choose_direction(mock_routes[0])

    msg = 'Which direction would you like to go? Type the index here:'
    destination_names = mock_routes[0]['attributes']['direction_destinations']
    mock_get_choice.assert_called_once_with(msg, destination_names)


def test_get_choice_calls_input_wrapper(mock_get_input):
    mock_get_input.side_effect = ['0', '0']
    cli.get_choice('foo', ['a', 'b', 'c'])
    mock_get_input.assert_called_once_with('\nfoo ')


def test_get_choice_doesnt_accept_non_ints(mock_get_input):
    mock_get_input.side_effect = ['nope', '0']
    cli.get_choice('foo', ['a', 'b', 'c'])
    assert mock_get_input.call_count == 2


def test_get_choice_only_accepts_range(mock_get_input):
    mock_get_input.side_effect = ['42', '0']
    cli.get_choice('foo', ['a', 'b', 'c'])
    assert mock_get_input.call_count == 2


def test_get_choice_returns_input(mock_get_input):
    mock_get_input.side_effect = ['0']
    result = cli.get_choice('foo', ['a', 'b', 'c'])
    assert result == 0


def test_cli_calls_get_routes(mock_cli_funcs, mock_mbta):
    cli.cli()
    mock_mbta['get_routes'].assert_called_once_with(['0', '1'])


def test_cli_calls_choose_route(mock_cli_funcs, mock_mbta, mock_routes):
    cli.cli()
    mock_cli_funcs['choose_route'].assert_called_once_with(mock_routes)


def test_cli_calls_get_stops(mock_cli_funcs, mock_mbta, mock_routes):
    cli.cli()
    mock_mbta['get_stops'].assert_called_once_with(mock_routes[0])


def test_cli_calls_choose_stop(mock_cli_funcs, mock_mbta, mock_stops):
    cli.cli()
    mock_cli_funcs['choose_stop'].assert_called_once_with(mock_stops)


def test_cli_calls_choose_direction(mock_cli_funcs, mock_mbta, mock_routes):
    cli.cli()
    mock_cli_funcs['choose_direction'].assert_called_once_with(mock_routes[0])


def test_cli_calls_get_predictions(
    mock_cli_funcs, mock_mbta, mock_routes, mock_stops
):
    cli.cli()
    mock_mbta['get_predictions'].assert_called_once_with(
        mock_routes[0],
        mock_stops[0],
        0
    )


def test_cli_calls_show_prediction(
    mock_cli_funcs, mock_mbta, mock_predictions
):
    cli.cli()
    mock_cli_funcs['show_prediction'].assert_called_once_with(mock_predictions)
