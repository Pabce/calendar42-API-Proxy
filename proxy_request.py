#!/usr/bin/env python

"""
File: proxy_request.py

A very simple script that calls the API Proxy for a determined EVENT_ID
"""

import json
import requests

__author__ = 'Pablo Barham'


EVENT_ID = '4e662f73d806f4caee212a1656130a73_14770730517003'

r = requests.get('http://localhost:8080/events-with-subscriptions/{}/'.format(EVENT_ID))

r_json = r.json()
print(json.dumps(r_json, sort_keys=True, indent=4))
