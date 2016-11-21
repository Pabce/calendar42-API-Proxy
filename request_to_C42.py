#!/usr/bin/env python

"""
File: request_to_C42.py

A module for talking to the C42 API.

The GetRequest class can be used to send GET requests to the API.
Other classes can be added in the future for increased functionality (PUT, HEAD, etc).

The get_events_with_subscriptions method does exactly what we want:
send a couple of GET requests and filter and combine the results from them.

Every GET request to the API should be handled by a new instance of the GetRequest class,
which takes a EVENT_ID and a authentication TOKEN as arguments.
"""

import requests

__author__ = 'Pablo Barham'


class GetRequest:

    def __init__(self, token, event_id):
        self.TOKEN = token
        self.EVENT_ID = event_id

        authorization_string = 'Token {}'.format(self.TOKEN)
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authorization': authorization_string
        }

    def get_events_with_subscriptions(self):
        # Send two GET requests to the C42 API, and filter and combine them
        print("Calling the Calendar42 API...")
        title, status_code = self.get_title()
        first_names = self.get_first_names()

        if status_code == 200:
            json_to_return = {
                'id': self.EVENT_ID,
                'title': title,
                'first_names': first_names
            }

        elif status_code == 401:
            json_to_return = {
                'error': {
                    'status_code': 401,
                    'message': 'A 401: Unauthorized error occurred when attempting to contact the C42 API. '
                               'Authentication credentials were not valid'
                }
            }
        elif status_code == 404:
            json_to_return = {
                'error': {
                    'status_code': 404,
                    'message': 'A 404: Not Found error occurred when attempting to contact the C42 API. '
                               'The EVENT_ID you requested does not exist'
                }
            }
        else:
            json_to_return = {
                'error': {
                    'status_code': status_code,
                    'message': 'Something strange occurred when attempting to contact the C42 API. '
                               'This was completely unexpected!'
                }
            }

        return json_to_return

    # Get event details (title)
    def get_title(self):
        url = 'https://demo.calendar42.com/api/v2/events/{}/'.format(self.EVENT_ID)

        try:
            r = requests.get(url, headers=self.headers)
            # Make HTTP status errors raise an exception
            r.raise_for_status()

            r_json = r.json()
            title = r_json['data'][0]['title']

            return title, r.status_code

        except requests.exceptions.RequestException as e:
            print('{} occurred while attempting to connect to {}'.format(e, url))
            return 'Could not be retrieved', r.status_code

    # Get event subscriptions (first names of participants)
    def get_first_names(self):
        url = 'https://demo.calendar42.com/api/v2/event-subscriptions/?event_ids=[{}]'.format(self.EVENT_ID)

        try:
            r = requests.get(url, headers=self.headers)
            # Make HTTP status errors raise an exception
            r.raise_for_status()

            r_json = r.json()
            number_of_subscribers = r_json['meta_data']['count']
            first_names = [r_json['data'][n]['subscriber']['first_name'] for n in range(number_of_subscribers)]

            return first_names

        except requests.exceptions.RequestException as e:
            print('{} occurred while attempting to connect to {}'.format(e, url))
            return 'Could not be retrieved'
