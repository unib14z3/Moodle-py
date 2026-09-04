import requests

from moodlepy.config import MOODLE_TOKEN, MOODLE_URL

TOKEN = MOODLE_TOKEN


class MoodleClient:
    def __init__(self, token=TOKEN, url=MOODLE_URL):
        self.token = token
        self.url = url

    def build_request_params(self, wsfunction, params_extra=None):
        params = [
            ("wstoken", self.token),
            ("wsfunction", wsfunction),
            ("moodlewsrestformat", "json"),
        ]

        if params_extra:
            for key, value in params_extra.items():
                if isinstance(value, (list, tuple)):
                    for index, item in enumerate(value):
                        params.append((f"{key}[{index}]", item))
                else:
                    params.append((key, value))

        return params

    def call(self, wsfunction, params_extra=None):
        params = self.build_request_params(wsfunction, params_extra)
        response = None

        try:
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            return {
                "error": f"Request failed: {exc}",
                "status_code": getattr(response, "status_code", None),
                "response_text": getattr(response, "text", ""),
            }

        except ValueError as exc:
            return {
                "error": f"Invalid JSON response: {exc}",
                "status_code": getattr(response, "status_code", None),
                "response_text": getattr(response, "text", ""),
            }
