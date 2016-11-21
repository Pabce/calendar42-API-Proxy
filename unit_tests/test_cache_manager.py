#!/usr/bin/env python

"""
File: test_cache_manager.py

A unit test for the CacheManager class.
"""

import random
import time
import sys

sys.path.append("../")
import cache_manager

__author__ = 'Pablo Barham'


class TestCacheManager:

    def setup_class(self):
        self.cache_time = 0.01
        self.cm = cache_manager.CacheManager(cache_time=self.cache_time)

    def test_use_cache(self):
        # Test a number of random EVENT_IDs.
        # They should all return False the first time (no cached values for that event ID)
        # True the second (the value has just been cached)
        # False again the third (the cached value has expired)

        test_list = [str(random.randint(0, 100000)) for n in range(1000)]
        for event_id in test_list:
            self._use_cache(event_id, 1, False)

            self.cm.add_to_cache(event_id, {})
            self._use_cache(event_id, 2, True)

        time.sleep(self.cache_time)
        for event_id in test_list:
            self._use_cache(event_id, 3, False)

    def _use_cache(self, event_id, run, expected):
        assert self.cm.use_cache(event_id) == expected

    def test_add_to_cache(self):
        error_event_data = {'error': 1234}
        self.cm.add_to_cache('fake_id_1', error_event_data)
        expected = False
        assert ('fake_id_1' in self.cm.cache) == expected

        non_error_event_data = {'not_an_error': 3456}
        self.cm.add_to_cache('fake_id_2', non_error_event_data)
        expected = True
        assert ('fake_id_2' in self.cm.cache) == expected


