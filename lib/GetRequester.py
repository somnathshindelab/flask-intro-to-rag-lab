from __future__ import annotations

import json
from typing import Any

import requests


class GetRequester:
    """Fetch a remote response body and optionally convert it to JSON data."""

    DEFAULT_ENDPOINT = "https://learn-co-curriculum.github.io/json-site-example/endpoints/people.json"

    def __init__(self, endpoint: str | None = None, timeout: int = 10):
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.timeout = timeout

    def get_response_body(self) -> Any:
        """Query the configured endpoint and return parsed JSON when possible."""
        response = requests.get(self.endpoint, timeout=self.timeout)
        response.raise_for_status()

        if hasattr(response, "json"):
            return response.json()

        if hasattr(response, "content"):
            return response.content

        if hasattr(response, "text"):
            return response.text.encode("utf-8")

        return self.load_json(response)

    def get_raw_response_body(self) -> bytes:
        """Query the configured endpoint and return the raw response body bytes."""
        response = requests.get(self.endpoint, timeout=self.timeout)
        response.raise_for_status()
        if hasattr(response, "content"):
            return response.content
        if hasattr(response, "text"):
            return response.text.encode("utf-8")
        return json.dumps(self.load_json(response)).encode("utf-8")

    def load_json(self, response: requests.Response | None = None) -> Any:
        """Convert the API response into JSON data."""
        if response is None:
            response = requests.get(self.endpoint, timeout=self.timeout)
            response.raise_for_status()

        if hasattr(response, "json"):
            return response.json()

        return json.loads(response.text)
