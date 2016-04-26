# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


"""store: for getting and putting files in json format"""

import io
import six
from . import BubbleKV

import simplejson as json

def no_enc_fun():
    pass


class JsonLinesKV(BubbleKV):

    """store and retrieve a List of dictionaries in jsonlines.
    wanted to use:
    https://raw.githubusercontent.com/wbolster/jsonlines/master/jsonlines/jsonlines.py
    but thats still 0.0.1 and does not work in PY2
    """
    _encode = no_enc_fun
    _decode = no_enc_fun

    def __init(self, file_name, reset=False):
        BubbleKV.__init__(self,
                          name='JsonLinesKV',
                          file_name=file_name,
                          reset=reset)
        self._can_dump_generator = True
        self.say('here')

    def _dump(self, data, full_data=True):
        self.say('dumping', verbosity=10)
        with io.open(self._file_name, 'w', encoding='utf8') as jsonl_file:
            for item in data['data']:
                sitem=json.dumps(item,ensure_ascii=False)
                if six.PY3:
                    sitem+=u"\n"
                    jsonl_file.write(sitem)
                else:
                    sitem+=b"\n"
                    jsonl_file.writelines([unicode(sitem)])

    def _encode_for_try(self, data={}):
        self.say('_encode_for_try', verbosity=10)
        json.dumps(data, ensure_ascii=False)

    def _load(self):
        jsonl_file = io.open(self._file_name,'r')
        try:
            for item in jsonl_file.readlines():
                jlitem=json.loads(item)
                self.say('jsonlines item', stuff=jlitem, verbosity=10001)
                yield jlitem
        except ValueError as ve:
            res = {}
            res['error'] = 'cannot decode json, ValueError'
            res['exception'] = str(ve)
            yield res
