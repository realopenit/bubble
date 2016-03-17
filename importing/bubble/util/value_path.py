# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

'''not sure if we need this a lot anymore, flat<->unflat seems to work great,
eventually add the get_path and set_path to flat_dict'''

from .. import Bubble


class ValuePath(Bubble):

    def __init__(self):
        Bubble.__init__(self, name='ValuePath')
        self.verbose = 0

    def get_path(self, data, path):
        self.say('get_path:' + str(path) + ' from ' + str(data))

        parts = path.split('.')
        curr = None
        try:
            for p in parts:
                p = p.strip()
                if p.isdigit() and isinstance(curr, list):
                    p = int(p)
                if curr:
                    curr = curr[p]
                else:
                    curr = data[p]
                self.say('current part:' + str(p) + ' type:' + str(type(curr)))

        except KeyError:
            curr = {'KEY ERROR': path, 'in': data}
            # err = True

        self.say('key_path:res>>> ' + str(curr) + ' >>>as>>>' +
                 str(path) + '>>>from>>>' + str(data))
        return curr

    def exists(self, data, path):
        res = self.get_path(data, path)
        if 'KEY ERROR' not in res:
            return True
        return False
        # yes this path exists in this d
        self.say('does path>>> ' + path + ' >>> exits:' + str(res))
        return res

    def _list(self, atindex, content=''):
        # TODO: move 'empty' to some configuration
        self.say('create a list with index:' + str(atindex))
        i = int(atindex)
        l = [''] * i
        self.say('new list:' + str(l))
        l[i - 1] = content
        return l

    def _dict(self, key, content):
        d = {key: content}
        return d

    # def _make(self, key, in_path, content):
    #    self.say('make a new key>>>'+key+'>>>with>>>'+in_path+':'+str(content) )
    def _make(self, key, content):
        """clean"""
        pass
        self.say('make a new key>>>' + key + '>>>with>>>:' + str(content))
        if key.isdigit():
            i = int(key)  # list index [p]
            self.say('extending parent list to contain index:' + key)
            # make a list with size
            return self._list(i, content)
        else:
            return self._dict(key, content)

    # def set_path(self,value='',  path='', data={} ):
    def set_path(self, data, path, value):
        """
        Sets the given key in the given dict object to the given value. If the
        given path is nested, child dicts are created as appropriate.
        Accepts either a dot-delimited path or an array of path elements as the
        `path` variable.
        """
        self.say('set_path:value:' + str(value) +
                 ' at:' + str(path) + ' in:' + str(data))

        if isinstance(path, str):
            path = path.split('.')
        if len(path) > 1:
            self.set_path(data.setdefault(path[0], {}), path[1:], value)
        else:
            data[path[0]] = value
        return data


# for generic usage
val_path = ValuePath()


def get_keypath(current, kpath, default_not_existing=None):
    if val_path.exists(current, kpath):
        return val_path.get_path(current, kpath)
    else:
        return default_not_existing


if __name__ == '__main__':
    inp = {'abra': {'cad': {'abdra': 'hello'}, 'l': [12, 13, 14]}}
    vp = ValuePath()

    print(vp.exists(inp, 'abra.cad.abdra'))
    print(vp.get_path(inp, 'abra.cad.abdra'))

    print(vp.exists(inp, 'abra.cad.l.1'))
    print(vp.get_path(inp, 'abra.cad.l.1'))

    print(vp.set_path(inp, 'val.77.and.keyword.hello', 'world'))
    print(vp.get_path(inp, 'val.77.and.keyword.hello'))
