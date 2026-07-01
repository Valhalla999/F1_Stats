from my_app import api


def test_fetch_json_uses_base_url_and_timeout(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": True}

    def fake_get(url, params=None, timeout=None):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(api.requests, "get", fake_get)

    result = api._fetch_json("current/drivers.json", params={"limit": 10})

    assert result == {"ok": True}
    assert captured == {
        "url": "https://api.jolpi.ca/ergast/f1/current/drivers.json",
        "params": {"limit": 10},
        "timeout": api.REQUEST_TIMEOUT,
    }


def test_fetch_json_returns_empty_dict_on_request_error(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        raise api.requests.RequestException("offline")

    monkeypatch.setattr(api.requests, "get", fake_get)

    assert api._fetch_json("current/drivers.json") == {}


def test_get_nested_returns_default_for_missing_path():
    data = {"MRData": {"DriverTable": {}}}

    assert api._get_nested(data, ("MRData", "DriverTable", "Drivers"), []) == []
