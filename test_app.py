import time

import requests


APP_URL = "http://localhost:8000"


def wait_for_app(url, timeout=240, interval=5):
    deadline = time.time() + timeout
    last_error = None

    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.status_code
        except requests.RequestException as exc:
            last_error = exc

        time.sleep(interval)

    if last_error:
        raise AssertionError(f"Unable to load Streamlit app: {last_error}") from last_error

    raise AssertionError("Unable to load Streamlit app within the timeout window.")


def test_app_loading():
    status_code = wait_for_app(APP_URL)
    assert status_code == 200, "Unable to load Streamlit App"
