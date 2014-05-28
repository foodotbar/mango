#!/usr/bin/python3.3

import sys
import httplib2
import urllib.parse
import urllib.request
import os
from hDBclient_obj import *

#url = 'http://www.baidu.com'
#resp = urllib.request.urlopen(url)
#print(type(resp))
#print(resp)

data = " ".join(sys.argv[1:])

#c = hDBclient_obj('localhost', 5678)
c = hDBclient_obj()
c.construct_toke()
m = c.exec_cmd(data)
if not m:
        print('None')
else:
        print(m)   

