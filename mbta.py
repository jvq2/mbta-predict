from typing import List

import requests


def get_routes(route_types: List[str] = None):
    """ Query the api for a list of routes by route type

    Example curl:

        ```bash
            curl -X GET \
                "https://api-v3.mbta.com/routes?page%5Boffset%5D=0&page%5Blimit%5D=1&filter%5Btype%5D=0" \
                -H "accept: application/vnd.api+json"
        ```
    """
    params = {}

    if route_types is not None:
        params['filter[type]'] = ','.join(route_types)

    url = 'https://api-v3.mbta.com/routes'
    request = requests.get(url, params=params)

    # TODO: Error handling
    resp = request.json()
    return resp.get('data', [])


def get_stops(route):
    """ Query the api for a list of stops on a given route

    Exaple curl:

        ```bash
            curl -X GET \
                "https://api-v3.mbta.com/stops?page%5Boffset%5D=0&page%5Blimit%5D=2&sort=name&filter%5Broute%5D=Red" \
                -H "accept: application/vnd.api+json"
        ```
    """
    # TODO: Investigate: Can a stop have more than one type of route use it?
    params = {
        'filter[route]': route['id']
    }

    url = 'https://api-v3.mbta.com/stops'
    request = requests.get(url, params=params)

    # TODO: Error handling
    resp = request.json()
    return resp.get('data', [])


def get_predictions(route, stop, direction_id):
    """ Query the api for vehicle predictions at a given stop for a route and
    direction

    Example curl:

        ```bash
            curl -X GET \
                "https://api-v3.mbta.com/predictions?page%5Blimit%5D=5&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-alfcl&filter%5Broute%5D=Red" \
                -H "accept: application/vnd.api+json"
    """
    params = {
        'filter[route]': route['id'],
        'filter[stop]': stop['id'],
        'filter[direction_id]': direction_id,
        'sort': 'departure_time',
        'page[limit]': 1
    }

    url = 'https://api-v3.mbta.com/predictions'
    request = requests.get(url, params=params)

    # TODO: Error handling
    resp = request.json()
    return resp.get('data', [])
