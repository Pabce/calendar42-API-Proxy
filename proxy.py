#!/usr/bin/env python

"""
File: proxy.py

Set up a HTTP Proxy server that takes GET requests from a client and forwards them to the C42 API,
returning the answer.

First, the Proxy checks if the GET request has a valid format. If so, it proceeds to call the C42 API.
If the call to the API is successful, it will cache the response for further calls with the same EVENT_ID.
If the call to the API fails, or has an unexpected response, it will inform the user of the occurred error.

The Proxy can be initialized with the default authentication TOKEN provided or with a different one.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import json

import cache_manager
import request_to_C42

__author__ = 'Pablo Barham'


class Handler(BaseHTTPRequestHandler):
    # Handler for GET request:
    def do_GET(self):
        print('\nGET request from {} received by the Proxy'.format(self.client_address))

        # Expected request path: /events-with-subscriptions/$EVENT-ID/
        path_values = manage_path(self.path)
        if len(path_values) == 0:
            self.invalid_request()

        elif path_values[0] == 'events-with-subscriptions' and len(path_values) == 2:
            EVENT_ID = path_values[1]
            self.get_events_with_subscriptions(EVENT_ID)

        else:
            self.invalid_request()

        print('HTTP response sent to client')
        return

    def get_events_with_subscriptions(self, EVENT_ID):
        if proxy_cache_manager.use_cache(EVENT_ID):
            json_event_data = proxy_cache_manager.cache[EVENT_ID]

        else:
            api_request = request_to_C42.GetRequest(TOKEN, EVENT_ID)
            json_event_data = api_request.get_events_with_subscriptions()

            proxy_cache_manager.add_to_cache(EVENT_ID, json_event_data)

        if 'error' in json_event_data:
            self.gateway_error(json_event_data)
            return

        # Status line
        self.send_response(200)

        # Headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Body
        event_data = json.dumps(json_event_data)
        self.wfile.write(bytes(event_data, 'utf-8'))

    def invalid_request(self):
        # Status line
        self.send_response(400)

        # Headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Body
        json_error_data = {
            'error': {
                'status_code': 400,
                'message': 'Bad Request: The path ({}) you requested to the Proxy is invalid. '
                           'Expected path: /events-with-subscriptions/$EVENT_ID/'.format(self.path)
            }
        }

        event_data = json.dumps(json_error_data)
        self.wfile.write(bytes(event_data, 'utf-8'))

    def gateway_error(self, event_data):
        # Status line
        self.send_response(502)

        # Headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Body
        json_error_data = {
            'error': {
                'status_code': 502,
                'message': 'Gateway Error: An error occurred while contacting the C42 API',
                'request_to_C42_error': event_data['error']
            }
        }

        event_data = json.dumps(json_error_data)
        self.wfile.write(bytes(event_data, 'utf-8'))


def manage_path(request_path):
    split_path = request_path.split("/")
    path_values = [value for value in split_path if value != '']

    return path_values


PORT_NUMBER = 8080
TOKEN = ''
proxy_address = ('', PORT_NUMBER)
proxy_handler = Handler
proxy_cache_manager = cache_manager.CacheManager()


def start_proxy(token='43ce3623f44c6bf9ff9a07622eb295ec0d7d2d0a'):
    # Set the authentication token:
    global TOKEN
    TOKEN = token

    # Create a HTTP server and define the handler to manage incoming requests
    server = HTTPServer(proxy_address, proxy_handler)
    print('Started Proxy server on port {}'.format(PORT_NUMBER))

    # Wait for incoming HTTP requests (forever)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Proxy server interrupted by user')
        server.socket.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_proxy(sys.argv[1])
    else:
        start_proxy()
