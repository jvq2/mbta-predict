# from pprint import pprint
from typing import List
from datetime import datetime

from mbta import get_routes, get_stops, get_predictions

# AC
#
# 1. Your program should prompt users to select from a list of routes that
#    service only Light and Heavy Rail trains.
#
# 2. Your program should display a listing of stops related to the selected
#    route and prompt the user to select a stop
#
# 3. Your program should display a list of route directions and prompt the
#    user to select a direction
#
# 4. Your program should display the next predicted departure time for a train
#    based on the previously selected inputs


# Without an api key, all requests are limited to 20/min. With an api key that
#  limit is 1000/min or above
# TODO: Rate limit handling


def cli_choose_route(routes):
    """ Print the available routes and prompts the user to select one
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
    choice = cli_get_choice(prompt, routes)

    return routes[choice]


def cli_choose_stop(stops):
    """ Print the available stops and prompts the user to select one
    """
    print('Available Stops')
    for index, stop in enumerate(stops):
        attributes = stop.get('attributes', {})
        print('\n--- Stop:', attributes.get('name'), '----')
        print('\tIndex:', index)
        print('\tAddress:', attributes.get('address'), '----')

    prompt = 'Which stop would you like? Type the stop index:'
    choice = cli_get_choice(prompt, stops)
    return stops[choice]


def cli_choose_direction(route):
    """ Prints the route directions and prompts the user to select one
    """
    print('Choose a direction:')

    destination_names = route['attributes'].get('direction_destinations', [])
    direction_names = route['attributes'].get('direction_names')
    for index, direction in enumerate(direction_names):
        print(f'{index}: {direction} - {destination_names[index]}')

    prompt = 'Which direction would you like to go? Type the index here:'
    return cli_get_choice(prompt, destination_names)


def cli_get_choice(prompt: str, items: List):
    """ Handle user input for selecting an item by its index
    """
    choice = None
    while True:
        # choice = input('Which one would you like? Type the index: ')
        choice = input(f'\n{prompt} ')

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


def cli_show_prediction(predictions):
    if not len(predictions):
        print('Could not find any predicted departure times for those '
              'choices.')

    attributes = predictions[0]['attributes']
    departure_time = datetime.fromisoformat(attributes['departure_time'])
    print('Next predicted departure time:', departure_time)


def cli():
    # Get a list of routes for Light Rail (0) and Heavy Rail (1)
    routes = get_routes(['0', '1'])

    route = cli_choose_route(routes)
    # print('route', route)

    stops = get_stops(route)

    stop = cli_choose_stop(stops)
    # print('stop', stop)

    direction_id = cli_choose_direction(route)
    # print('direction_id', direction_id)

    predictions = get_predictions(route, stop, direction_id)

    cli_show_prediction(predictions)


if __name__ == '__main__':
    cli()
