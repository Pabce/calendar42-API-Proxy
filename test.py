#!/usr/bin/env python

import proxy
import requests
import time
import json

__author__ = 'Pablo Barham'

TOKEN = '43ce3623f44c6bf9ff9a07622eb295ec0d7d2d0a9'
EVENT_ID = '4e662f73d806f4caee212a1656130a73_14770730517003'

r = requests.get("http://localhost/events-with-subscriptions/%s/" % EVENT_ID)
r_json = r.json()
print(json.dumps(r_json, sort_keys=True, indent=4))

# TODO: README, ejemplos, headers, pretty print of json
