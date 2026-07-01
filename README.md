# F1 Stats

F1 Stats is a small desktop app for browsing Formula 1 driver data, standings, and historical race results. It was built with Python, Kivy, and KivyMD as a CS50 project and now uses the Ergast-compatible Jolpica F1 API.

Video demo: https://youtu.be/dl8w-OQIhxg

## Features

- Current driver overview with driver number, name, nationality, and date of birth
- Current driver championship standings
- Historical race lookup by season and circuit
- Simple About page with social links

## Requirements

- Python 3.10 or newer
- Internet access for live Formula 1 data
- Python dependencies listed in `requirements.txt`

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

## Tests

Run the test suite with:

```bash
pytest
```

The tests mock live API calls so the basic app wiring can be checked without depending on the network.

## Project Structure

- `main.py` starts the KivyMD app and registers the screens.
- `project.py` contains the main menu screen.
- `my_app/api.py` contains the F1 API access helpers.
- `my_app/views/` contains the individual app screens.
- `test_project.py` contains smoke tests for the app setup and navigation.

## Notes

The app reads Formula 1 data from `https://api.jolpi.ca/ergast/f1`, which provides an Ergast-compatible API. Network requests use a timeout and return empty results on API errors so the UI can still load when the service is unavailable.
