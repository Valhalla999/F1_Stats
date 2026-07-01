import logging
from typing import Any

import requests


BASE_URL = "https://api.jolpi.ca/ergast/f1"
REQUEST_TIMEOUT = 10

logger = logging.getLogger(__name__)


def _fetch_json(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{BASE_URL}/{path.lstrip('/')}"

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        logger.warning("Unable to fetch F1 data from %s: %s", url, error)
        return {}


def _get_nested(data: dict[str, Any], keys: tuple[str, ...], default: Any) -> Any:
    current: Any = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    return default if current is None else current


def get_current_drivers() -> list[dict[str, Any]]:
    data = _fetch_json("current/drivers.json")
    return _get_nested(data, ("MRData", "DriverTable", "Drivers"), [])


def get_driver_standings() -> list[dict[str, Any]]:
    data = _fetch_json("current/driverStandings.json")
    standings = _get_nested(data, ("MRData", "StandingsTable", "StandingsLists"), [])

    if not standings:
        return []

    return standings[0].get("DriverStandings", [])


def get_circuits(year: str | int) -> list[dict[str, Any]]:
    data = _fetch_json(f"{year}/circuits.json")
    return _get_nested(data, ("MRData", "CircuitTable", "Circuits"), [])


def get_seasons() -> list[dict[str, Any]]:
    seasons: list[dict[str, Any]] = []
    offset = 0

    while True:
        data = _fetch_json("seasons.json", params={"limit": 100, "offset": offset})
        page = _get_nested(data, ("MRData", "SeasonTable", "Seasons"), [])

        if not page:
            return seasons

        seasons.extend(page)
        offset += len(page)


def get_race_results(year: str | int, circuit: str) -> list[dict[str, Any]]:
    data = _fetch_json(f"{year}/circuits/{circuit}/results.json")
    return _get_nested(data, ("MRData", "RaceTable", "Races"), [])
