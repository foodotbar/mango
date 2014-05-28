#!/usr/bin/python3.3

from tempfile import mkstemp
import os.path
import pickle 
import socket
import sys
import socketserver
from hDB import *
import httplib2
import urllib.parse

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

class MyTCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
                obj = read_pickle('./auth.conf')
                db = hDB('db/010')
                db.opendb()
                
                self.data = self.request.recv(8192).strip()
                av = str(self.data, 'utf-8').split(' ')
                print(av)
                
                if (av[0] == 'GET'):
                        m = db.GET(av[1])
                        if not m:
                                self.request.sendall(b'None')
                        else:
                                self.request.sendall(m[1])
                elif (av[0] == 'SET'):
                        db.SET(av[1], av[2])
                        self.request.sendall(b'SET ok')
                elif (av[0] == 'AUTH'):
                        match = 0
                        for (k, v) in obj.items():
                                if (k == av[1]):
                                        if (v == av[2]):
                                                match = 1
                                                self.request.sendall(b'Token')
                                                break
                        if (match == 0):
                                self.request.sendall(b'None')
                elif (av[0] == 'URL'):
                        m = db.GET(av[1])
                        if not m:
                                try:
                                        status = "status "
                                        length = "content-length "
                                        http = httplib2.Http()
                                        response, content = http.request(av[2], 'GET')
                                        
                                        for (k, v) in response.items():
                                                if (k == 'status'):
                                                        status += response['status']
                                                if (k == 'content-length'):
                                                        length += response['content-length']
                                        httpvalue = status
                                        httpvalue += " " 
                                        httpvalue += length
                                        
                                        db.SET(av[1], httpvalue)
                                        self.request.sendall(bytes(httpvalue, 'utf-8'))

                                except:
                                        print((av[2], "get status size error"))
                                        self.request.sendall(b'None')
                        else:
                                self.request.sendall(m[1])

                db.closedb()        

if __name__ == "__main__":
        data = " ".join(sys.argv[1:])
        av = data.split(' ')
        
        host, port = 'localhost', 5678
        if ( len(av) == 4):
                if (av[0] == '--port'):
                        port = int(av[1])
                elif (av[0] == '--host'):
                        host = av[1]
                else:
                        print('invalid param')
                        os._exit(1)
        
                if (av[2] == '--port'):
                        port = int(av[3])
                elif (av[2] == '--host'):
                        host = av[3]
                else:
                        print('invalid param')
                        os._exit(1)
        elif (len(av) == 2):
                host = 'localhost'
                port = 5678
        elif (len(av) == 3):
                if (av[0] == '--host' and av[1] == '--port'):
                        port = int(av[2])
                elif (av[0] == '--host' and av[2] == '--port'):
                        host = av[1]
                elif (av[0] == '--port' and av[2] == '--host'):
                        port = int(av[1])
                elif (av[0] == '--host' and av[1] == '--port'):
                        host = av[2]
        server = socketserver.TCPServer((host, port), MyTCPHandler)
        server.serve_forever()
                

