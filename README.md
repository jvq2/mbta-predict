# Example Project: Predict the next departing train for MBTA
The following is an example project designed to be only 2 hours of work. The CLI code was completed in 2 hours. The tests and README were completed after that.

#### Project Instructions:
```
Write a program in a language of your choice (we prefer Python or Angular) that interacts with
the MBTA public API (https://api-v3.mbta.com) to achieve the following acceptance criteria:
1. Your program should prompt users to select from a list of routes that service only Light and Heavy Rail trains.
2. Your program should display a listing of stops related to the selected route and prompt the user to select a stop
3. Your program should display a list of route directions and prompt the user to select a direction
4. Your program should display the next predicted departure time for a train based on the previously selected inputs
```


## Setting up the virtual environmemt
The recommended way to run this is inside a virtual environment. You can setup the virtual environment by running the following commands.
```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Running the CLI
```bash
    python3 cli.py
```

## Running the tests
```bash
    pytest tests
```
If developing on the app, you can run pytest-watch to keep running the tests when changes are detected:
```bash
    pytest-watch tests
```