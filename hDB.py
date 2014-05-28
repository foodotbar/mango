#!/usr/bin/python3.3

import os
from hashlib import md5
from struct import *
import errno
import fcntl

def lockfile(file, timeout = 10):
                fd = os.open(file, os.O_WRONLY)
                try:
                        fcntl.flock(fd, fcntl.LOCK_EX)
                        return fd
                except IOError as err:
                        raise 

def init_index(istorage, hsize, ichunksize):
        """
        each index chunk has 36 bytes
        """
        """
        md5array = bytes(md5(b'bar').hexdigest(), 'utf-8')
        print(md5array)
        md5key = md5array
        print(md5key)
        print(type(md5key))
        ichunk = bytes(16)
        ichunk += pack('iiiii', 0, 0, 0, 0, 0)
        a = bytes(36)
        print(ichunk)
        print(a)
        """
        try:
                fd = os.open(istorage, os.O_RDWR)
                for i in range(hsize):
                        ichunk = bytes(ichunksize)
                        os.pwrite(fd, ichunk, i * ichunksize)
                os.close(fd)
        except OSError:
                print('init_index error')
                os.abort()

class hDB:
        def __init__(self, dbname):
                self.dbname = dbname
                self.istorage = dbname + '/db.index'
                self.ialloc_lock = dbname + '/.ialloc.lock'
                self.hsize = 10000
                self.ichunksize = 36
                self.next_ichunk = self.hsize * self.ichunksize

                self.dstorage = dbname + '/db.data'
                self.dalloc_lock = dbname+ '/.dalloc.lock'
                self.next_dchunk = 0 
                self.dorphan = dbname + '/db.orphan'
                self.dorphan_lock = dbname + '/.dorphan.lock'
                
                self.ifd = -1
                self.dfd = -1
                self.ofd = -1

                if (os.access(self.dbname, os.F_OK) == 0):
                        try:
                                os.mkdir(self.dbname, 0o777)
                                fd = os.open(self.istorage, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                fd = os.open(self.ialloc_lock, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                fd = os.open(self.dstorage, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                fd = os.open(self.dalloc_lock, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                fd = os.open(self.dorphan, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)
                                fd = os.open(self.dorphan_lock, os.O_RDWR| os.O_CREAT | os.O_TRUNC, 0o644)
                                os.close(fd)

                                init_index(self.istorage, self.hsize, self.ichunksize)
                        except OSError:
                                print('creat db error')
                                os.abort()
                
                self.next_ichunk = os.stat(self.istorage).st_size
                self.next_dchunk = os.stat(self.dstorage).st_size

        def opendb(self):
                try:
                        self.ifd = os.open(self.istorage, os.O_RDWR)
                        self.dfd = os.open(self.dstorage, os.O_RDWR)
                        self.ofd = os.open(self.dorphan, os.O_RDWR)
                except:
                        print('open db error')
                        os.abort()
        
        def closedb(self):
                os.close(self.ifd)
                os.close(self.dfd)
                os.close(self.ofd)

        def ialloc(self):
                ## acquire ialloc lock
                try:
                        print('ialloc lock')
                        fd = lockfile(self.ialloc_lock)
                        addr = self.next_ichunk
                        self.next_ichunk += self.ichunksize
                        os.close(fd)
                        print('ialloc unlock')
                        return addr
                except:
                        print('ialloc error')
                        os.abort()
        
        def dalloc(self, size):
                ## acquire ialloc lock
                try:
                        print('dalloc lock')
                        fd = lockfile(self.dalloc_lock)
                        addr = self.next_dchunk
                        self.next_dchunk += size
                        os.close(fd)
                        print('dalloc unlock')
                        return addr
                except:
                        print('dalloc error')
                        os.abort()
        
        def get_d(self, size, off):
                try:
                        (keylen, ) = unpack('i', os.pread(self.dfd, 4, off))
                        key = os.pread(self.dfd, keylen, off + 4)
                        value = os.pread(self.dfd, size - 4 - keylen, off + 4 + keylen)
                        return (key, value)
                except:
                        print('get_d error')
                        os.abort()

        def put_d(self, off, key, value):
                try:
                        bkey = bytes(key, 'utf-8')
                        bvalue = bytes(value, 'utf-8')
                        dchunk = pack('i', len(key))
                        dchunk += bkey
                        dchunk += bvalue
                        os.pwrite(self.dfd, dchunk, off)
                        return 4 + len(bkey) + len(bvalue)
                except:
                        print('put_d error')
                        os.abort()
        
        def append_orphan(self, size, offset):
                try:
                        print('orphan lock')
                        fd = lockfile(self.dorphan_lock)
                        off = os.stat(self.dorphan).st_size
                        orphan_bar = pack('ii', size, offset)
                        os.pwrite(self.ofd, orphan_bar, off)
                        os.close(fd)
                        print('orphan unlock')
                except:
                        print('append_orphan error')
                        os.abort()

        def lock_hlist(self, slot):
                whence = 0
                start = slot * self.ichunksize
                len = self.ichunksize 
                try:
                        print((b'lock', self.ifd, fcntl.LOCK_EX, len, start, whence))
                        fcntl.lockf(self.ifd, fcntl.LOCK_EX, len, start, whence)
                        print((b'lock OK--> ', self.ifd, fcntl.LOCK_EX, len, start, whence))
                except:
                        print('lock hlist error')
                        os.abort()

        def unlock_hlist(self, slot):
                whence = 0
                start = slot * self.ichunksize
                len = self.ichunksize
                try:
                        fcntl.lockf(self.ifd, fcntl.LOCK_UN, len, start, whence)
                        print((b'unlock', self.ifd, fcntl.LOCK_UN, len, start, whence))
                except:
                        print('unlock hlist error')
                        os.abort()
        
        def __pack_ichunk(self, md5key, prev, next, addr, dsize, doff):
                ichunk = bytes(md5key)
                ichunk += pack('iiiii', prev, next, addr, dsize, doff)
                return ichunk
        
        def __unpack_ichunk(self, iaddr):
                try:
                        md5key = os.pread(self.ifd, 16, iaddr)
                        (prev, next, addr, dsize, doff) = unpack('iiiii', os.pread(self.ifd, 20, iaddr + 16))
                        return (md5key, prev, next, addr, dsize, doff)
                except:
                        print('__from_ichunk error')
                        os.abort()

        def get_i(self, slot, md5key):
                ## we should hash list lock, before we involved get_i
                try:
                        head = self.__unpack_ichunk(slot * self.ichunksize)  
                        print((b'get_i', slot, md5key, head))
                        if (head[4] == 0):
                                return None
                        if (md5key == head[0]):
                                return head
                        next = head[2]
                        while True:
                                if (next == head[3]):
                                        break
                                if (next <= 360):
                                        print(ichunk)
                                        os.abort()
                                ichunk = self.__unpack_ichunk(next)  
                                if (md5key == ichunk[0]):
                                        return ichunk
                                next = ichunk[2]
                        return None
                except:
                        print('get_i pread error')
                        os.abort()

        def put_i(self, md5key, prev, next, addr, dsize, doff):
                ichunk = self.__pack_ichunk(md5key, prev, next, addr, dsize, doff)
                try:
                        os.pwrite(self.ifd, ichunk, addr) 
                except:
                        print('put_i error')
                        os.abort()
        
        def hash_md5key(self, md5key):
                (a, b, c, d) = unpack('IIII', md5key)
                hashvalue = (a + b + c + d) % self.hsize
                return hashvalue
        
        def key_md5(self, key):
                amd5 = md5()
                amd5.update(bytes(key, 'utf-8'))
                md5array = amd5.digest()
                return md5array

        def GET(self, key):
                md5key = self.key_md5(key)
                slot = self.hash_md5key(md5key)
                
                self.lock_hlist(slot)
                ichunk = self.get_i(slot, md5key)
                self.unlock_hlist(slot)
                
                if not ichunk:
                        return None
                return self.get_d(ichunk[4], ichunk[5])
        
        def update(self, slot, md5key, addr, dsize, doff):
                print('*******************')
                print('update') 
                haddr = slot * self.ichunksize
                head = self.__unpack_ichunk(haddr)  
                print(head)
                if (head[4] == 0):
                        print('none..........')
                        self.put_i(md5key, haddr, haddr, haddr, dsize, doff)
                        print((md5key, haddr, haddr, haddr, dsize, doff))
                        print('*******************')
                elif (head[2] == head[3]):
                        print('one..........')
                        if (addr < self.hsize * self.ichunksize):
                                os.abort()
                        if (haddr >= self.hsize * self.ichunksize):
                                os.abort()
                        self.put_i(md5key, addr, addr, haddr, dsize, doff)
                        print((md5key, addr, addr, haddr, dsize, doff))
                        self.put_i(head[0], haddr, haddr, addr, head[4], head[5])
                        print((head[0], haddr, haddr, addr, head[4], head[5]))
                        print('*******************')
                else:
                        print('more..........')
                        first = self.__unpack_ichunk(head[2])
                        if (head[3] > self.hsize * self.ichunksize):
                                os.abort()
                        if (head[1] <= self.hsize * self.ichunksize):
                                os.abort()
                        if (head[2] <= self.hsize * self.ichunksize):
                                os.abort()
                        if (addr <= self.hsize * self.ichunksize):
                                os.abort()
                        self.put_i(md5key, head[1], addr, head[3], dsize, doff)
                        print((md5key, head[1], addr, head[3], dsize, doff))
                        self.put_i(head[0], head[3], head[2], addr, head[4], head[5])
                        print((head[0], head[3], head[2], addr, head[4], head[5]))
                        self.put_i(first[0], addr, first[2], first[3], first[4], first[5])
                        print((first[0], addr, first[2], first[3], first[4], first[5]))
                        print('*******************')
        
        def SET(self, key, value):
                md5key = self.key_md5(key)
                slot = self.hash_md5key(md5key)
                dsize = 4 + len(bytes(key, 'utf-8')) + len(bytes(value, 'utf-8')) 
                doff = self.dalloc(dsize)
                
                print('*******************')
                print('SET')
                print((slot, key,value, md5key))
                self.lock_hlist(slot)
                if (slot >= self.hsize):
                        os.abort()
                ichunk = self.get_i(slot, md5key)
                print((b'get_i return', ichunk))
                if not ichunk:
                        iaddr = self.ialloc()
                        self.update(slot, md5key, iaddr, dsize, doff) 
                        self.unlock_hlist(slot)
                        
                        self.put_d(doff, key, value)

                else:
                        print('*******************')
                        print('replace')
                        print('*******************')
                        self.append_orphan(ichunk[4], ichunk[5])
                        self.put_i(md5key, ichunk[1], ichunk[2], ichunk[3], dsize, doff)
                        print((slot, md5key, ichunk[1], ichunk[2], ichunk[3], dsize, doff, key, value))
                        self.unlock_hlist(slot)
                        print('*******************')
                       
                        self.put_d(doff, key, value)
                        



