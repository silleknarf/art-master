#!/usr/bin/python

from flask import jsonify
from database.database import session
import logging 

logfile = logging.getLogger('file')

class BaseExceptionHandler(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        logfile.error(message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidUsage(BaseExceptionHandler):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        BaseExceptionHandler.__init__(self, message, status_code, payload)
