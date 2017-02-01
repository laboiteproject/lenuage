# coding: utf-8
from __future__ import unicode_literals
import json
import os

import requests

from .models import AppTraffic


HERE = os.path.dirname(os.path.abspath(__file__))


class MockRequest(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data

    @property
    def ok(self):
        return self.status_code == 200


def test_result_ok(monkeypatch):
    with open(os.path.join(HERE, 'test_data', 'ok.json')) as f:
        data = f.read()
    monkeypatch.setattr(requests, 'get', lambda url, params: MockRequest(200, json.loads(data, encoding='utf-8')))
    monkeypatch.setattr(AppTraffic, 'save', lambda self: True)
    ret = AppTraffic().get_app_dictionary()
    assert ret['trajectory_name'] == 'Rue Réaumur'
    assert ret['trip_duration'] == 10


def test_results_ko(monkeypatch):
    with open(os.path.join(HERE, 'test_data', 'ko.json')) as f:
        data = f.read()
    monkeypatch.setattr(requests, 'get', lambda url, params: MockRequest(200, json.loads(data, encoding='utf-8')))
    monkeypatch.setattr(AppTraffic, 'save', lambda self: True)
    assert AppTraffic().get_app_dictionary() is None
