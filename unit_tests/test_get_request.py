#!/usr/bin/env python

"""
File: test_get_request.py

A unit test for the GetRequest class in the request_to_C42.py module.
"""

import sys

sys.path.append("../")
import request_to_C42

__author__ = 'Pablo Barham'

class TestGetRequest:

    def setup_class(self):
        # We create a list of GET requests, with both valid and invalid authentication Tokens and Event ids
        real_token = '43ce3623f44c6bf9ff9a07622eb295ec0d7d2d0a'
        real_event_id = '4e662f73d806f4caee212a1656130a73_14770730517003'

        self.gr_list = [request_to_C42.GetRequest('fake_token', 'fake_event_id'),
                        request_to_C42.GetRequest(real_token, 'fake_event_id'),
                        request_to_C42.GetRequest(real_token, real_event_id)]

    def test_get_title(self):
        for gr in self.gr_list:
            title, status = gr.get_title()

            if gr.TOKEN == 'fake_token' or gr.EVENT_ID == 'fake_event_id':
                expected = True
            else:
                expected = False

            assert (title == 'Could not be retrieved') == expected

    def test_get_first_names(self):
        for gr in self.gr_list:
            first_names = gr.get_first_names()

            if gr.TOKEN == 'fake_token':
                expected = True
            else:
                expected = False

            assert (first_names == 'Could not be retrieved') == expected

    def test_get_events_with_subscriptions(self):
        for gr in self.gr_list:
            json_response = gr.get_events_with_subscriptions()

            if gr.TOKEN == 'fake_token':
                expected = 401
            elif gr.EVENT_ID == 'fake_event_id':
                expected = 404
            else:
                assert ('error' in json_response) == False
                continue

            assert json_response['error']['status_code'] == expected




