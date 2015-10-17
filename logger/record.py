#! /usr/bin/env python3

from collections import UserDict, OrderedDict
from datetime import datetime
import simplejson as json


class Record(UserDict):
    
    def __init__(self, initial_data=None):
        if initial_data is not None:
            if isinstance(initial_data, OrderedDict):
                self.data = initial_data
            elif isinstance(initial_data, dict):
                self.data = OrderedDict([(k, v) for k, v in initial_data.items()])
            else:
                raise ValueError('Optional initial data must be a (ordered) dictionary.')
        else:
            # Create a new one.
            self.data = OrderedDict()

    @staticmethod
    def parse(data):
        if isinstance(data, bytes):
            data = data.decode('utf8')
        o = json.loads(data, object_pairs_hook=OrderedDict)
        if '@timestamp' not in o:
            o['@timestamp'] = datetime.now().isoformat()
        if '@version' in o:
            assert o['@version'] == 1
        else:
            o['@version'] = 1
        return Record(o)

