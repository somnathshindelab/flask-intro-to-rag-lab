from __future__ import annotations

from typing import Any

import requests


class PeopleApiClient:
    """Fetch people data from the JSON endpoint and return it as Python objects."""

    DEFAULT_ENDPOINT = "https://learn-co-curriculum.github.io/json-site-example/endpoints/people.json"

    def __init__(self, endpoint: str | None = None, timeout: int = 10):
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.timeout = timeout

    def get_response_body(self) -> list[dict[str, Any]]:
        """Query the people endpoint and return the parsed JSON payload."""
        response = requests.get(self.endpoint, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


people_client = PeopleApiClient()
