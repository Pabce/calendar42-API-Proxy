#!/usr/bin/env python


import json
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

        json_to_return = {
            'id': self.EVENT_ID,
            'title': title,
            'first_names': first_names
        }

        if status_code == 401:
            json_to_return['error'] = '401: Unauthorized error (C42 API)'
            json_to_return['error_message'] = 'A 401: Unauthorized error ' \
                                              'occurred when attempting to contact the C42 API. ' \
                                              'Authentication credentials were not valid'
        elif status_code == 404:
            json_to_return['error'] = '404: Not Found error (C42 API) '
            json_to_return['error_message'] = 'A 404: Not Found error ' \
                                              'occurred when attempting to contact the C42 API. ' \
                                              'The EVENT_ID you requested does not exist'
        elif status_code != 200:
            json_to_return['error'] = status_code
            json_to_return['error_message'] = 'Something strange occurred when attempting to contact the C42 API.' \
                                              'This was completely unexpected!'

        to_return = json.dumps(json_to_return)
        return to_return

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
