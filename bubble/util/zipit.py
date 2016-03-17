# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import os
import arrow
import gzip

from .inside_try import inside_try


@inside_try
def zipit(ctx, org_file_name):
    now = str(arrow.now())
    if not os.path.isfile(org_file_name):
        return False

    zip_file_name = org_file_name.replace('/remember/', '/remember/archive/')

    # TODO: make bz2 default if available
    with open(org_file_name, 'rb') as source:
        zip_file = zip_file_name + '_' + now + '.gz'
        target = gzip.open(zip_file, 'wb')
        while True:
            chunk = source.read(1 << 10)
            if not chunk:
                break
            target.write(chunk)
        target.close()
    return os.path.isfile(zip_file)
