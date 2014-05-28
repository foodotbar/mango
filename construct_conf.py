#!/usr/bin/python3.3

from tempfile import mkstemp
import pickle 
import os
import os.path
from hDBclient_obj import *

def write_pickle(obj, dest, tmp=None, pickle_protocol=0): 
        if tmp is None:
                tmp = os.path.dirname(dest)
        fd, tmppath = mkstemp(dir=tmp, suffix='.tmp')
        with os.fdopen(fd, 'wb') as fo:
                pickle.dump(obj, fo, pickle_protocol)
                fo.flush()
                os.fsync(fd)
                os.rename(tmppath, dest)

def read_pickle(dest):
        with open(dest, 'rb') as fp:
                obj = pickle.load(fp)
                return obj

argvdata = " ".join(sys.argv[1:])
av = argvdata.split(' ')

if (len(av) != 3):
        size = os.stat(av[0]).st_size
        if (size == 0):
                print('null')
                os._exit(1)
        obj = read_pickle(av[0])
        print(obj)
        os._exit(1)

size = os.stat(av[0]).st_size
if (size == 0):
        obj = {'root':'123456'}
else:
        obj = read_pickle(av[0])
obj[av[1]] = av[2]
write_pickle(obj, av[0])

obj = read_pickle(av[0])
print(obj)


