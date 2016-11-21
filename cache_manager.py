#!/usr/bin/env python

"""
File: cache_manager.py

The CacheManager class manages the cache for the Proxy server.

An instance of the CacheManager class stores the cached values for each distinct EVENT_ID that the user has requested,
and also the time at when they were cached.

When the user requests information for the same EVENT_ID, the CacheManager can determine whether enough time has passed
(and a new request to the C42 API will be sent) or not (and the cached value will be returned).

Also, values will only be cached if the request to the C42 API that generated them returned no error.
"""

import time

__author__ = 'Pablo Barham'

CACHE_TIME = 4.2 * 60  # that is 4.2 minutes, as requested


class CacheManager:
    def __init__(self, cache_time=CACHE_TIME):
        self.first_call_time = {}
        self.cache = {}
        self.cache_time = cache_time

    # The following function checks if there is a stored cache value for the current EVENT_ID, returning True or False.
    def use_cache(self, EVENT_ID):
        call_time = time.time()

        if EVENT_ID not in self.first_call_time:
            self.first_call_time[EVENT_ID] = call_time

        time_since_last_call_to_C42 = call_time - self.first_call_time[EVENT_ID]

        if EVENT_ID in self.cache and time_since_last_call_to_C42 < self.cache_time:
            print('Time since last call to the C42 API ({} seconds) for the event with EVENT_ID: {} '
                  'is smaller than the established cache time ({} seconds).\n'
                  'Therefore, requested response is directly from the Proxy cache.'
                  .format(time_since_last_call_to_C42, EVENT_ID, self.cache_time))

            return True

        else:
            self.first_call_time[EVENT_ID] = call_time

            return False

    def add_to_cache(self, EVENT_ID, event_data):
        if 'error' not in event_data:
            self.cache[EVENT_ID] = event_data
