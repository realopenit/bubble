# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

"""store: for getting and putting files in bubble format (experimental)"""

import os
import hashlib

import yaml


from . import BubbleKV
from ..flat_dict import flat, escape, unescape

def _get_hash(gbc, val):
    vald = yaml.dump(val)
    valdh = hashlib.sha1(vald)
    valdhh = valdh.hexdigest()
    return valdhh

def _bubble_encode_key(gbc, keyval, keyhash):
    res = '>>>0,"%s","%s">>>key>>>' % (keyval, keyhash)
    gbc.say('enc key:' + res, verbosity=999)
    return res

def _bubble_encode_val(gbc, valval, valhash):
    res = '>>>0,"%s",%s>>>val>>>' % (valval, valhash)
    gbc.say('enc val:' + res, verbosity=999)
    return res

def _bubble_encode_kv(gbc, index, keyhash, valhash):
    res = '>>>0,"%s",%s>>>keyval>>>' % (keyhash, keyhash)
    gbc.say('enc kv:' + res, verbosity=999)
    return res

def _bubble_encode_ikv(gbc, ipos, key, val):
    # esc_key=escape(key)
    esc_val = escape(gbc, str(val))
    res = '>>>%s,%s,%s>>>' % (ipos, key, esc_val)  # insert
    gbc.say('enc kv:' + res, verbosity=999)
    return res

def _bubble_encode_line(gbc, index, linehash):
    res = '>>>%d,"%s">>>flatline>>>' % (index, linehash)
    gbc.say('enc kvl:' + res, verbosity=999)
    return res

def bubble_encode(gbc, bubble_file, lod=[]):
    gbc.say('bubble encoding lod', verbosity=999)
    gbc.say('bubble encoding lod', stuff=lod, verbosity=1000)
    index = 0
    keys = []
    values = []
    kvs = []
    lines = 0
    res = '# encoding bubble start\n'
    # for item in lod['data']:
    for item in lod:
        index += 1
        gbc.say('#bubble encoding lod[%d]' % index, verbosity=999)
        gbc.say('#item:', stuff=item, verbosity=999)
        res += '#Adding at bubble index %d\n' % (index)
        flitem = flat(gbc, item)
        gbc.say('#bubble encoding lod[%d]  flat' %
                (index), stuff=flitem, verbosity=999)
        fkey = True
        pos = 0
        for key in flitem.keys():
            gbc.say('k:%s fk:%s' % (key, str(fkey)), verbosity=999)
            if fkey:
                fkey = False
                ipos = index
            else:
                pos += 1
                # ipos='+%d'%(pos)
                ipos = '+'

            val = flitem[key]
            line = _bubble_encode_ikv(gbc, ipos, key, val)
            bubble_file.write(line + '\n')
            lines += 1
            gbc.say('index:%d\n' % (index), verbosity=999)
    res += '# encoding bubble end\n'
    m = """i:%s
      k:%d
      v:%d
      kv:%d
      lines:%d""" % (index, len(keys), len(values), len(kvs), lines)
    gbc.say(m, verbosity=999)
    ret = {'total': index}
    gbc.say(ret, stuff=ret, verbosity=999)
    return ret

def bubble_encode_kvs(gbc, bubble_file, lod=[]):
    gbc.say('bubble encoding lod', verbosity=999)
    gbc.say('bubble encoding lod', stuff=lod, verbosity=1000)
    index = 0
    keys = []
    values = []
    kvs = []
    lines = 0
    res = '# encoding bubble start\n'
    for item in lod:
        index += 1
        gbc.say('#bubble encoding lod[%d]' % index, verbosity=999)
        gbc.say('#item:', stuff=item, verbosity=999)
        res += '#Adding at bubble index %d\n' % (index)
        flitem = flat(gbc, item)
        gbc.say('#bubble encoding lod[%d]  flat' %
                (index), stuff=flitem, verbosity=999)
        for key in flitem.keys():
            enc_key = key.encode('utf-8')
            key_hash = _get_hash(gbc, enc_key)
            if key_hash not in keys:
                line = _bubble_encode_key(gbc, enc_key, key_hash)
                bubble_file.write(line + '\n')
                keys.append(key_hash)
            val = flitem[key]
            enc_val = val.encode('utf-8')
            val_hash = _get_hash(gbc, enc_val)
            if val_hash not in values:
                line = _bubble_encode_val(gbc, enc_val, val_hash)
                bubble_file.write(line + '\n')
                values.append(val_hash)
            kv_hash = _get_hash(gbc, key_hash + val_hash)
            if kv_hash not in kvs:
                kvs.append(kv_hash)
                line = _bubble_encode_kv(gbc, key_hash, val_hash, kv_hash)
                bubble_file.write(line + '\n')
            lines += 1
            line = _bubble_encode_line(gbc, index, kv_hash)
            bubble_file.write(line + '\n')
            gbc.say('index:%d\n' % (index), verbosity=999)
    res += '# encoding bubble end\n'
    m = "i:%s\nk:%d\nv:%d\nkv:%d\nlines:%d" % (index,
                                               len(keys),
                                               len(values),
                                               len(kvs),
                                               lines)
    gbc.say(m, verbosity=999)
    return {"res": res, "msg": m, "total": index}


def bubble_decode(gbc, bubble_file):
    gbc.say('bubble decoding, yielding', stuff=bubble_file, verbosity=999)
    item = {}
    not_first = False
    for line in bubble_file.readlines():
        gbc.say('bubble decoding : %s' % (line), verbosity=999)
        lparts = line.split('>>>')
        gbc.say('bubble decoding line parts', stuff=lparts, verbosity=1000)
        if len(lparts) == 3:
            ikv = lparts[1]
            ikvparts = ikv.split(',')
            ipos = ikvparts[0]
            key = ikvparts[1]
            val = ikvparts[2]
            if ipos.isdigit():
                index = ipos
                if not_first:
                    yield item
                    item = {}

            gbc.say("ipos:" + ipos, verbosity=999)
            gbc.say("index:" + index, verbosity=999)
            gbc.say('bubble decoding ikv parts', stuff=ikvparts, verbosity=999)
            gbc.say('adding:raw_lod[%s][%s] = unescape(%s)' %
                    (index, key, val), verbosity=999)
            item[key] = unescape(gbc, val)
            not_first = True
        else:
            gbc.say(
                'bubble decoding ikv parts: wrong amount no ikvparts(?)', verbosity=999)

    if item:
        gbc.say('yield last:', verbosity=999)
        yield item


class BubbleFlatKV(BubbleKV):

    """store and retrieve a List of dictionaries in sqlite.
    """

    def __init__(self, file_name='__bubble_kvdb_data_tmp.bubble', reset=False):
        BubbleKV.__init__(self,
                          name='BubbleFlatKV',
                          file_name=file_name,
                          reset=reset)

        self.say(file_name, verbosity=999)
        self._file_name = file_name

        if reset:
            self.reset()

        self._count = 0
        self._kcount = 0
        self._vcount = 0
        self._kvcount = 0
        self._encode_for_try = bubble_encode
        self._can_dump_generator = True
        self.say('here')

    def dump(self, LOD=[], full_data=True):
        self.say('dumping', verbosity=10)
        return self._dump(LOD)

    def load(self):
        return self._load()

    def close(self):
        pass

    def get_total(self):
        self.say('get_total:%d' % self._count, verbosity=10)
        return self._count

    def _dump(self, LOD=[]):
        self.say('ydump:type of LOD:' + str(type(LOD)), verbosity=100)
        bubble_file = open(self._file_name, 'w')
        return bubble_encode(self, bubble_file, LOD)

    def _load(self):
        if not os.path.isfile(self._file_name):
            # should be crying..
            self.cry('bubble load:no such file:' +
                     self._file_name, verbosity=10)
            return []

        bubble_file = open(self._file_name)
        return bubble_decode(self, bubble_file)
