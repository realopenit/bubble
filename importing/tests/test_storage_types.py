from bubble import Bubble
from bubble.util.store import get_file,put_file
def _test_storage_type(sty):
    bu=Bubble('ST'+sty+'ST', verbose=1000)
    testf='./tests_tmp/test_storage.'+sty
    ind=[{'a':'A'},{'b':'B'}]
    put_file(bu, testf,ind)
    res=get_file(bu,testf)
    assert 'lod_gen' in res

    rd=[]
    for i in res['lod_gen']:
        rd.append(i)
    bu.say(testf)
    bu.say(stuff=ind)
    bu.say(stuff=rd)
    assert ind==rd

def test_bubble():
    _test_storage_type('bubble')
def test_json():
    _test_storage_type('json')
def test_yaml():
    _test_storage_type('yaml')
def test_msgpack():
    _test_storage_type('msgpack')
def test_msgpack():
    _test_storage_type('sqlite3')


