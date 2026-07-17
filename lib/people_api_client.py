from __future__ import annotations

import requests

from lib.GetRequester import GetRequester


class PeopleApiClient(GetRequester):
    """Compatibility wrapper for the people data endpoint."""

    pass


people_client = PeopleApiClient()
