# -*- coding: utf-8 -*-

import hashlib

from compat import b
from exception import UpYunServiceException, UpYunClientException

DEFAULT_CHUNKSIZE = 8192

def make_rest_signature(bucket, username, password,
                                method, uri, date, length):
    if method:
        signstr = '&'.join([method, uri, date, str(length), password])
        signature = hashlib.md5(b(signstr)).hexdigest()
        return "UpYun %s:%s" % (username, signature)

    else:
        signstr = '&'.join([uri, bucket, date, password])
        signature = hashlib.md5(b(signstr)).hexdigest()
        return "UpYun %s:%s:%s" % (bucket, username, signature)

def make_content_md5(value, chunksize=DEFAULT_CHUNKSIZE):
    if hasattr(value, 'fileno'):
        md5 = hashlib.md5()
        for chunk in iter(lambda: value.read(chunksize), b''):
            md5.update(chunk)
        value.seek(0)
        return md5.hexdigest()
    elif isinstance(value, bytes) or (not PY3 and
                                isinstance(value, builtin_str)):
        return hashlib.md5(value).hexdigest()
    else:
        raise UpYunClientException('object type error')

def decode_msg(msg):
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    return msg

def encode_msg(msg):
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    return msg
