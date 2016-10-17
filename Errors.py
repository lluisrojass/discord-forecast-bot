#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager
import sys


class WeatherException(Exception):
    def __init__(self, message):
        super(WeatherException, self).__init__(message)


class DatabaseException(Exception):
    def __init__(self, message):
        super(DatabaseException, self).__init__(message)


def create_error_handler(catch, throw):
    @contextmanager
    def handler():
        try:
            yield
        except catch:
            value = sys.exc_info()[1]
            raise throw(value)
    return handler
