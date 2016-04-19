# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

"""dataset: for getting and putting datasets, with archives in freeze files """

import arrow
import os
import simplejson as json

DATASET_PRESENT=False
try:
    import dataset
    DATASET_PRESENT=True
except ImportError as e:
    class dummy_dataset(object):
         def connect(*args,**kwargs):
            #print("Bubble:import:there is n dataset present, pip install dataset")
            msg="\nImportError, there is no dataset present, please use:\"pip install dataset\""
            import click
            click.echo(msg)
            raise click.Abort()
    dataset=dummy_dataset()

from ..counter import Counter
from ..generators import make_stamping_gen
from ..zipit import zipit

def _get_db(ctx, stage, dataset_args):
    if dataset_args['DS_TYPE'] == 'sqlite':
        ds_uri = 'sqlite:///remember/' + stage + '.sqlite.db'
    elif dataset_args['DS_TYPE'] == 'freeze_json':
        ds_uri = 'sqlite:///:memory:'
    else:
        ds_uri_tmpl = '%s://%s:%s@%s/%s'
        ds_uri = ds_uri_tmpl % (dataset_args['DS_TYPE'],
                                dataset_args['DS_USER'],
                                dataset_args['DS_PASSWORD'],
                                dataset_args['DS_HOST'],
                                dataset_args['DS_DB'])

    ctx.gbc.say('ds_uri:', stuff=ds_uri, verbosity=10)

    lod_db = dataset.connect(ds_uri)
    ctx.gbc.say('lod_db:', stuff=lod_db, verbosity=10)
    return lod_db



def _get_step_table_in_stage(ctx, step, stage, reset, dataset_args):
    ctx.gbc.say('_get_step_table_in_stage:' + stage + ' ' + step, verbosity=10)
    ctx.gbc.say('dataset_args:', stuff=dataset_args, verbosity=10)

    lod_db = _get_db(ctx, stage, dataset_args)
    table_name = dataset_args['DS_BUBBLE_TAG'] + '_' + step + '_' + stage
    step_table = lod_db[table_name]

    if reset:
        step_table.drop()
        # recreate table after drop
        step_table = lod_db[table_name]
    elif dataset_args['DS_TYPE'] == 'freeze_json':
        freeze_file = './remember/dataset_freeze_' + step + '_' + stage + '.json'
        step_table = _lod_load_frozen_json(ctx, step_table, freeze_file)

    return step_table


def lod_dump(ctx, dataset_args, step, stage, reset, full_data, data, archive=True):
    """
    :param ctx:
    :param path:
    :param step:
    :param stage:
    :param first_only:
    :return:
    """
    lod_db = _get_db(ctx, stage, dataset_args)

    step_table = _get_step_table_in_stage(
        ctx, step, stage, reset, dataset_args)
    counter = Counter()
    counter.set_parent(ctx.gbc)

    stamped_data = make_stamping_gen(ctx, data, full_data, counter)
    rows = []
    if 'DS_CHUNKSIZE' in dataset_args:
        chunk_size = dataset_args['DS_CHUNKSIZE']
    else:
        chunk_size = 10
    ctx.gbc.say('dumping chunksize: %d' % chunk_size, verbosity=40)

    start_ts = arrow.now()
    for ditem in stamped_data:
        jitem = {u'json_str': json.dumps(ditem)}
        rows.append(jitem)
        if len(rows) == chunk_size:
            # lod_db._release()
            lod_db.begin()
            step_table.insert_many(rows, chunk_size=chunk_size)
            lod_db.commit()
            rows = []
            curr_time = arrow.now() - start_ts
            ctx.gbc.say('dumping chunk took: ' + str(curr_time), verbosity=40)
    # take care of the rest
    if len(rows) > 0:
        step_table.insert_many(rows)

    ret = {}
    ret['total'] = counter.get_total()
    ret['count_in_table'] = step_table.count()

    totals_equal = False
    if ret['count_in_table'] == ret['count_in_table']:
        totals_equal = True
    ret['totals_equal'] = totals_equal

    ctx.gbc.say('lod_dump:return', stuff=ret, verbosity=100)
    freeze_file = './remember/dataset_freeze_' + step + '_' + stage + '.json'

    dataset.freeze(step_table, format='json', filename=freeze_file)
    if archive:
        zipped = zipit(ctx, freeze_file)
    if zipped and dataset_args['DS_TYPE'] != 'freeze_json':
        os.remove(freeze_file)
    total_time = arrow.now() - start_ts
    ctx.gbc.say('dumping took:' + str(total_time), verbosity=10)
    return ret


def _lod_load_frozen_json(ctx, memdb_table, frozen_json_file):
    # TODO: util.cli_misc.file_exist,
    # split off file and dirs related from cli_misc and import there and here.
    # cannot load from here, as lod_load is defined in cli_misc also
    if not (os.path.exists(frozen_json_file) and
            os.path.isfile(frozen_json_file)):
        return memdb_table

    res = {}
    try:
        jsonfile = open(frozen_json_file)
        res = json.loads(jsonfile.read())
    except Exception as excpt:
        res['error'] = 'cannot decode json'
        res['excpt'] = str(excpt)
        ctx.gbc.cry('cannot load frozen json:', stuff=res)

    if 'count' in res:
        for item in res['results']:
            memdb_table.insert(item)
    return memdb_table


def lod_load(ctx, dataset_args, step, stage):
    step_table = _get_step_table_in_stage(
        ctx, step, stage, False, dataset_args)
    # step_table.unlock()

    counter = Counter()
    if dataset_args['DS_TYPE'] != 'sqlite':
        for ditem in step_table:
            counter.count()
            ctx.gbc.say('lod_load:ditem', stuff=ditem, verbosity=100)
            item = json.loads(ditem[u'json_str'])
            yield item
    else:
        # WA: issue #582
        temp_in_mem=[]
        for ditem in step_table:
            temp_in_mem.append(ditem)
        # here the lock should be released, issue #582
        for ditem in temp_in_mem:
            counter.count()
            ctx.gbc.say('lod_load:ditem', stuff=ditem, verbosity=100)
            item = json.loads(ditem[u'json_str'])
            yield item

    res = {}
    res['total'] = counter.get_total()
    ctx.gbc.say('lod_dump:result', stuff=res, verbosity=100)
