# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


"""store: for getting and putting files
currently only json
and the highly experimental ".bubble" format for testing and comparing purposes"""

import os

from ... import Bubble
from ..counter import Counter
from ..zipit import zipit
from ..inside_try import inside_try
from ..generators import make_gen, make_stamping_gen


def load_storage_type_class(ctx, storage_type):
    ctx.gbc.say('loading module for storage type:' +
                storage_type, verbosity=10)
    if storage_type == '.json':
        return load_storage_type_class_json(ctx)
    if storage_type == '.jsonl':
        return load_storage_type_class_jsonl(ctx)

def load_storage_type_class_json(ctx):
    from .storage_type_json import JsonKV as STOREM
    ctx.gbc.say('storage module loaded', stuff=STOREM, verbosity=10)
    return STOREM


def load_storage_type_class_jsonl(ctx):
    from .storage_type_jsonl import JsonLinesKV as STOREM
    ctx.gbc.say('storage module loaded', stuff=STOREM, verbosity=10)
    return STOREM

def get_file_name(ctx, path, step, stage, stype):
    ctx.gbc.say('get_file_name:', stuff=(path, step, stage, stype))

    storage_file = path + 'remember/' + step + '_' + stage
    storage_file += '.' + stype
    ctx.gbc.say('get_file_name:res:' + storage_file)
    return storage_file


def get_file_info(ctx, storage_file_name):
    file_name, file_extension = os.path.splitext(storage_file_name)
    ret = {'file_name': file_name,
           'file_extension': file_extension}

    ctx.gbc.say('file_info:', stuff=ret)
    return ret


@inside_try
def get_bubble(ctx, bubble_file_name):
    # this is the proof of existence for a bubble content directory
    # TODO:
    # its not in the bubble format yet, when converted to bubble format,
    # we can use something like get_file(...,home+"/.bubble")

    ctx.gbc.say('get_bubble:' + bubble_file_name, verbosity=10)
    if bubble_file_name.endswith('.bubble'):
        with open(bubble_file_name) as bubble_file:
            content = bubble_file.read()
            ctx.say('get_bubble:content:' + str(content), verbosity=200)
            return content


def get_file(ctx, storage_file_name, first_only=False):
    ctx.gbc.say('get_file:' + storage_file_name, verbosity=10)
    file_info = get_file_info(ctx, storage_file_name)
    storem = load_storage_type_class(ctx, file_info['file_extension'])

    data = None

    if not os.path.exists(storage_file_name):
        if first_only:
            ctx.gbc.say('first only: returning empty dict, no such file:' +
                        storage_file_name, verbosity=10)
            return {}
        else:
            ctx.gbc.say('returning empty list, no such file:' +
                        storage_file_name, verbosity=10)
            return {'lod_gen': make_gen(ctx),
                    'total': 0,
                    'status': 'no such file:' + storage_file_name}

    bkv = storem(storage_file_name)
    bkv.set_parent(ctx.gbc)
    data = bkv.load()
    count = Counter()
    count.set_parent(ctx.gbc)

    ctx.gbc.say('get file:data', stuff=data, verbosity=1000)
    ctx.gbc.say('get file:data:type:' + str(type(data)), verbosity=100)

    if data:
        ctx.gbc.say('get file:data', stuff=data, verbosity=2000)
    else:
        ctx.gbc.cry('get file:there is no data', verbosity=10)

    gen_types_23 = ["<type 'generator'>",  # py2
                    "<class 'generator'>"]  # py3

    if str(type(data)) in gen_types_23:
        return {'lod_gen': data,
                'total': 'unknown from generator'}
    if 'data' in data and str(type(data['data'])) in gen_types_23:
        return {'lod_gen': data['data'],
                'total': 'unknown from generator'}

    if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
        if first_only:
            if len(data['data']) >= 1:
                return data['data'][0]
            else:
                return {}
        return {'lod_gen': make_gen(ctx, data['data'], count),
                'total': count.get_total()}
    elif isinstance(data, list):
        # inspect.isgeneratorfunction(data):
        return {'lod_gen': make_gen(ctx, data, count),
                'total': 'unknown from generator'}
    else:
        ctx.gbc.cry('data is not dict with a data list, or list',
                    stuff=data, verbosity=10)
        ctx.gbc.say('make gen and return', verbosity=10)
        return {'lod_gen': make_gen(ctx, data, count),
                'total': 'unknown from generator',
                'last_resort': True}


@inside_try
def put_file(ctx, storage_file_name, data=[], remove_first=False, archive=True, add_timestamp=True, full_data=True):

    # TODO: ensure no data ->no file
    ret = {}
    ret['total'] = 'unknown total'
    count = Counter()
    count.set_parent(ctx.gbc)
    data = make_stamping_gen(ctx.gbc, data, full_data, count)
    # generator calling should happen in STOREC

    ctx.gbc.say('count', stuff=count, verbosity=100)
    ctx.say('count.get_total:', stuff=count.get_total(), verbosity=10)

    file_info = get_file_info(ctx, storage_file_name)

    storec = load_storage_type_class(ctx, file_info['file_extension'])

    if not storec:
        ctx.gbc.cry("cannot load storage module for file", verbosity=10)
        return False
    else:
        ctx.gbc.say("will use loaded storage module for file",
                    stuff=storec, verbosity=10)

    ctx.gbc.say('put_file:' + storage_file_name, verbosity=10)
    ctx.gbc.say('put_file:.bubble', verbosity=999)
    bkv = storec(storage_file_name, reset=remove_first)
    bkv.set_parent(ctx.gbc)
    ctx.gbc.say('bubble data type:' + str(type(data)), verbosity=1000)
    ret['res'] = bkv.dump(data, full_data)
    ctx.gbc.say('counter', stuff=count.get_total(), verbosity=1)

    bkv.close()
    zipped = False
    if archive:
        zipped = zipit(ctx, storage_file_name)
    ret['zipped'] = zipped
    ret['total'] = count.get_total()
    ctx.gbc.say('put_file:return', stuff=ret, verbosity=100)
    return ret


class BubbleKV(Bubble):

    """store and retrieve a List of dictionaries in any file based type.
    """

    def __init__(self,
                 file_name='__bubble_kvdb_data_tmp.unknown_type',
                 name='BubbleKV',
                 reset=False):
        Bubble.__init__(self, name=name)

        self.say(file_name, verbosity=999)
        self._file_name = file_name

        self._count = 0
        self._kcount = 0
        self._vcount = 0
        self._kvcount = 0
        self._can_dump_generator = False
        self._reset = reset
        self.reset()

    def dump(self, lod=[], full_data=True):
        self.say('dumping:' + self._file_name, verbosity=1)
        ret = {}

        if self._can_dump_generator:
            try:
                ret = self._dump(lod)
                return ret
            except Exception as e:
                ret['error'] = 'cannot dump data to file %s' % self._file_name
                ret['exception'] = e
                return ret

        ndata = []
        for item in lod:
            try:
                self._encode_for_try({'test_enc': item})
                ndata.append(item)
            except Exception as encexpt:
                self.cry('skipped: cannot encode item: ' +
                         str(encexpt), stuff=item)
        data_to_dump = {'data': ndata}

        ret['notdumped'] = True
        if not self._dump:
            self.cry('dumping, there is no _dump method', verbosity=1)

        try:
            ret = self._dump(data_to_dump)
            return ret
        except Exception as e:
            ret['error'] = 'cannot dump data to file %s' % self._file_name
            ret['exception'] = e
            return ret

    def load(self):
        self.say('loading:' + self._file_name, verbosity=1)
        if os.path.exists(self._file_name):
            if not self._load:
                self.cry('loading, there is no _load method', verbosity=1)
            res = self._load()
        else:
            res = []
            self.say(
                'loading:file does not exist, returning empty list', verbosity=1)

        self.say('loading:res type=' + str(type(res)), verbosity=1)
        self.say('loading:res:', stuff=res, verbosity=10001)

        return res

    def close(self):
        pass

    def reset(self):
        if self._reset:
            if os.path.exists(self._file_name):
                self.say('reset, removing:' + self._file_name)
                os.remove(self._file_name)
            else:
                self.say('reset, there is no file yet:' + self._file_name)
        else:
            self.say('no reset:' + self._file_name)
