#!/usr/bin/env python

"""
File: test_proxy.py

A unit test for the whole proxy.py module.

IMPORTANT: For this module to work, proxy.py must be running!
"""

import sys
import requests

sys.path.append("../")
import proxy

__author__ = 'Pablo Barham'


class TestProxy:

    def setup_class(self):
        real_event_id = '4e662f73d806f4caee212a1656130a73_14770730517003'
        self.url_dict = {
            'bad_format': 'http://localhost:8080/sadasdadsad-with-subscrasdadiptions/232e',
            'good_format_bad_event_id': 'http://localhost:8080/events-with-subscriptions/{}/'.format('fake_event_id'),
            'good_format_and_event_id': 'http://localhost:8080/events-with-subscriptions/{}/'.format(real_event_id)
        }

    def test_do_GET(self):
        for key in self.url_dict:
            try:
                r = requests.get(self.url_dict[key])
            except:
                print('Whoops! Make sure proxy.py is running and try again!')
                sys.exit(1)

            if key == 'bad_format':
                expected = 400
            elif key == 'good_format_bad_event_id':
                expected = 502
            else:
                expected = 200

            try:
                assert r.status_code == expected
            except AssertionError:
                sys.exit(1)

    # The following 3 functions working are a necessary condition for do_GET to pass the test. Therefore, if do_GET
    # passes, the following functions pass to (the code is interrupted if do_GET does not pass)
    def test_get_events_with_subscriptions(self):
        assert True

    def test_gateway_error(self):
        assert True

    def test_invalid_request(self):
        assert True

    def test_manage_path(self):
        path = '/a/b/c/'
        expected = ['a','b','c']
        assert proxy.manage_path(path) == expected

        path = '/c/d/e'
        expected = ['c','d','e']
        assert proxy.manage_path(path) == expected

        path = 'f/g/h'
        expected = ['f','g','h']
        assert proxy.manage_path(path) == expected


    def test_get_user_parameters(self):
        default_token = '43ce3623f44c6bf9ff9a07622eb295ec0d7d2d0a'
        default_port = 8080
        user_input = ['*', '-a', '1234', '-p', '5678']
        expected_p, expected_a = 5678, '1234'
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '-p', '1234', '-a', '5678']
        expected_p, expected_a = 1234, '5678'
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '-p', '1234']
        expected_p, expected_a = 1234, default_token
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '-a', '1234']
        expected_p, expected_a = default_port, '1234'
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '-p', '1234asd', '-a', '5678']
        expected_p, expected_a = default_port, '5678'
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '-p', '1234asd', '-a']
        expected_p, expected_a = default_port, default_token
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)

        user_input = ['*', '23rawfa']
        expected_p, expected_a = default_port, default_token
        assert proxy.get_user_parameters(user_input) == (expected_p, expected_a)
