import json
from datetime import datetime
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL
from typing import List
from unittest import TestCase

import responses

from pygrocydm.location import LOCATION_ENDPOINT, Location
from pygrocydm.grocy_api_client import GrocyApiClient


class TestLocation(TestCase):

    def setUp(self):
        self.api = GrocyApiClient(CONST_BASE_URL, "demo_mode",  verify_ssl=CONST_SSL, port=CONST_PORT)
        self.endpoint = LOCATION_ENDPOINT + '/2'

    def test_location_data_diff_valid(self):
        location = self.api.get_request(self.endpoint)
        location_keys = location.keys()
        moked_location_json = """{
            "id": "2",
            "name": "Fridge",
            "description": null,
            "row_created_timestamp": "2020-03-01 00:50:24",
            "is_freezer": "0"
        }"""
        moked_keys = json.loads(moked_location_json).keys()
        self.assertCountEqual(list(location_keys), list(moked_keys))

    def test_parse_json(self):
        location = Location(self.api.get_request(self.endpoint), self.api)
        assert isinstance(location.id, int)
        assert isinstance(location.description, str) or location.description is None
        assert isinstance(location.name, str)
        assert isinstance(location.is_freezer, bool)
        assert isinstance(location.row_created_timestamp, datetime)
