from typing import List
from datetime import datetime

from mbta import get_routes, get_stops, get_predictions


# Without an api key, all requests are limited to 20/min. With an api key that
#  limit is 1000/min or above
# TODO: Rate limit handling


def choose_route(routes):
    """ Print the available routes and prompts the user to select one

    :param list routes: A list of route dicts as returned by the /routes/
        endpoint
    :returns dict: An individual route dictionary from the list
    """
    print('Available Routes')
    for index, route in enumerate(routes):
        attributes = route.get('attributes', {})
        print('\n--- Route:', attributes.get('long_name'), '----')
        print('\tIndex:', index)

        destination_names = attributes.get('direction_destinations', [])
        for index, direction in enumerate(attributes.get('direction_names')):
            print(f'\t{direction}: {destination_names[index]}')

    prompt = 'Which route would you like? Type the route index:'
    choice = get_choice(prompt, routes)

    return routes[choice]


def choose_stop(stops):
    """ Print the available stops and prompts the user to select one

    :param list stops: A list of stop dicts as returned by the /stops/ endpoint
    :returns dict: An individual stop dictionary from the list
    """
    print('Available Stops')
    for index, stop in enumerate(stops):
        attributes = stop.get('attributes', {})
        print('\n--- Stop:', attributes.get('name'), '----')
        print('\tIndex:', index)
        print('\tAddress:', attributes.get('address'), '----')

    prompt = 'Which stop would you like? Type the stop index:'
    choice = get_choice(prompt, stops)
    return stops[choice]


def choose_direction(route):
    """ Prints the route directions and prompts the user to select one

    :param dict route: A route dictionary to pull the directions from
    :returns int: An index representing the chosen direction
    """
    print('Choose a direction:')

    destination_names = route['attributes'].get('direction_destinations', [])
    direction_names = route['attributes'].get('direction_names')
    for index, direction in enumerate(direction_names):
        print(f'{index}: {direction} - {destination_names[index]}')

    prompt = 'Which direction would you like to go? Type the index here:'
    return get_choice(prompt, destination_names)


def get_choice(prompt: str, items: List):
    """ Handle user input for selecting an item by its index

    :param str prompt: The text to present to the user before entering text
    :param list items: A list of options. The chosen index must be in this list
    :returns int: The index of the user chosen item
    """
    choice = None
    while True:
        choice = get_input(f'\n{prompt} ')

        try:
            choice = int(choice)
        except ValueError:
            print('You must enter the numerical index of the desired item. '
                  'Please try again.')
            continue

        if choice >= len(items):
            print('You must enter the index of one of the above items. '
                  'Please try again.')
            continue

        break

    return choice


def get_input(prompt):
    """Shallow wrapper around input() for unit testing

    :param str prompt: The text to present to the user before entering text
    :returns str: The text the user entered
    """
    return input(prompt)


def show_prediction(predictions):
    """Prints the first prediction to the console. These predictions are
    already sorted.

    :param list predictions: A list of predictions returned from the api
    """
    if not len(predictions):
        print('\nCould not find any predicted departure times for those '
              'choices.')

    attributes = predictions[0]['attributes']

    if not attributes['departure_time']:
        print('\nThere are no departures from this stop in that direction.')
        return

    departure_time = datetime.fromisoformat(attributes['departure_time'])
    print('\nNext predicted departure time:', departure_time)


def cli():
    """Main command line interface
    """
    # Get a list of routes for Light Rail (0) and Heavy Rail (1)
    routes = get_routes(['0', '1'])

    # User picks a route
    route = choose_route(routes)

    # Get a list of stops for the chosen route
    stops = get_stops(route)

    # User picks a stop
    stop = choose_stop(stops)

    # User picks a direction
    direction_id = choose_direction(route)

    # Pull predictions from the api
    predictions = get_predictions(route, stop, direction_id)

    show_prediction(predictions)


if __name__ == '__main__':
    cli()
