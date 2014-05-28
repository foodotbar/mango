#!/usr/bin/python3.3

from tempfile import mkstemp
import os.path
import pickle 
import socket
import sys
import os

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

class hDBclient_obj:
        def __init__(self, host = 'localhost', port = 5678):
                self.host = host
                self.port = port
                self.token = 'token.conf'
        
        def construct_toke(self):
                if (os.access(self.token, os.F_OK) == 0):
                        try:
                                fd = os.open(self.token, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                size = os.stat(self.token).st_size
                                if (size == 0):
                                        obj = {"token":'0'}
                                        write_pickle(obj, self.token)
                        except:
                                print('contruct token.conf error')

        def exec_cmd(self, data):
                av = data.split(' ')
                if (not (av[0] == 'GET' or av[0] == 'SET' or av[0] == 'AUTH' or av[0] == 'URL')):
                        print('Only Support get/set :( ')
                        return None
                if (av[0] == 'GET'):
                        if (len(av) < 2):
                                print('GET Key needed')
                                return None
                if (av[0] == 'SET' or av[0] == 'AUTH' or av[0] == 'URL'):
                        if (len(av) < 3):
                                print('3 params needed')
                                return None
                if (av[0] == 'URL'):
                        obj = read_pickle(self.token)
                        if (obj['token'] == '0'):
                                print('Do auth first')
                                return None

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                        sock.connect((self.host, self.port))
                        sock.sendall(bytes(data + "\n", 'utf-8'))
                        received = str(sock.recv(8192), 'utf-8')
                finally:
                        sock.close()

                if (av[0] == 'GET'):
                        if (received == 'None'):
                                return None
                        return (av[1], received)
                elif (av[0] == 'SET'):
                        return (av[1], av[2])
                elif (av[0] == 'AUTH'):
                        if (received == 'Token'):
                                obj = read_pickle(self.token)
                                obj['token'] = '1'
                                write_pickle(obj, self.token)
                                return (av[1], '0')
                        else:
                                return (av[1], '-1')
                elif (av[0] == 'URL'):
                        return (av[1], received)


