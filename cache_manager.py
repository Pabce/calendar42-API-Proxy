#!/usr/bin/env python


import time

__author__ = 'Pablo Barham'

CACHE_TIME = 4.2 * 60  # that is 4.2 minutes, as requested


class CacheManager:
    def __init__(self):
        self.first_call_time = {}
        self.cache = {}

    # The following function checks if there is a stored cache value for the current EVENT_ID, returning True or False.
    def use_cache(self, EVENT_ID):
        call_time = time.time()

        if EVENT_ID not in self.first_call_time:
            self.first_call_time[EVENT_ID] = call_time

        time_since_last_call_to_C42 = call_time - self.first_call_time[EVENT_ID]

        if EVENT_ID in self.cache and time_since_last_call_to_C42 < CACHE_TIME:
            print('Time since last call to the C42 API ({} seconds) for the event with EVENT_ID: {} '
                  'is smaller than the established cache time ({} seconds).\n'
                  'Therefore, requested response is directly from the Proxy cache.'
                  .format(time_since_last_call_to_C42, EVENT_ID, CACHE_TIME))

            return True

        else:
            self.first_call_time[EVENT_ID] = call_time

            return False

    def add_to_cache(self, EVENT_ID, event_data):
        if 'error' not in event_data:
            self.cache[EVENT_ID] = event_data
