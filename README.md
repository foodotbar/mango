mango
=====

a Key-Value DB (just for fun, quick and dirty) like Redis

1. Key-Value DB����Python3.3�������ɵ�
2. ��Ҫ��װ httplib2 Packages
3. ʵ����"GET", "SET", "AUTH", "URL" ����
4. ʹ����������


[root@vm2 hDB_v1]# ./hDBclient_2.py 
Only Support get/set :( 
None
[root@vm2 hDB_v1]# ./hDBclient_2.py GET ui
('ui', 'ioiowriqweorwerwqr')
[root@vm2 hDB_v1]# ./hDBclient_2.py SET LiTao Tom
('LiTao', 'Tom')
[root@vm2 hDB_v1]# ./hDBclient_2.py GET LiTao
('LiTao', 'Tom')
[root@vm2 hDB_v1]# ./hDBclient_2.py AUTH root 123456
('root', '0')
[root@vm2 hDB_v1]# ./hDBclient_2.py URL baidu www.baidu.com
('baidu', 'status 200 content-length 54470')
[root@vm2 hDB_v1]# 

 


[root@vm2 hDB_v1]# ./hDBserver.py --host  --port 
['GET', 'ui']
(b'lock', 5, 2, 36, 75024, 0)
(b'lock OK--> ', 5, 2, 36, 75024, 0)
(b'get_i', 2084, b'}\\\x00\x9eN\xb8\xbb\xc7\x86G\xca\xec\xa3\x08\xe6\x1b', (b'}\\\x00\x9eN\xb8\xbb\xc7\x86G\xca\xec\xa3\x08\xe6\x1b', 75024, 75024, 75024, 24, 0))
(b'unlock', 5, 8, 36, 75024, 0)
['SET', 'foo', 'bar']
dalloc lock
dalloc unlock
*******************
SET
(3109, 'foo', 'bar', b'8\xf3\xef\xe3L\xb2\x90\x92\x00\x7f\xe0C1\xb3\x83\xa3')
(b'lock', 5, 2, 36, 111924, 0)
(b'lock OK--> ', 5, 2, 36, 111924, 0)
(b'get_i', 3109, b'8\xf3\xef\xe3L\xb2\x90\x92\x00\x7f\xe0C1\xb3\x83\xa3', (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0, 0, 0, 0, 0))
(b'get_i return', None)
ialloc lock
ialloc unlock
*******************
update
(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0, 0, 0, 0, 0)
none..........
(b'8\xf3\xef\xe3L\xb2\x90\x92\x00\x7f\xe0C1\xb3\x83\xa3', 111924, 111924, 111924, 12, 64)
*******************
(b'unlock', 5, 8, 36, 111924, 0)
['GET', 'foo']
(b'lock', 5, 2, 36, 111924, 0)
(b'lock OK--> ', 5, 2, 36, 111924, 0)
(b'get_i', 3109, b'8\xf3\xef\xe3L\xb2\x90\x92\x00\x7f\xe0C1\xb3\x83\xa3', (b'8\xf3\xef\xe3L\xb2\x90\x92\x00\x7f\xe0C1\xb3\x83\xa3', 111924, 111924, 111924, 12, 64))
(b'unlock', 5, 8, 36, 111924, 0)
['AUTH', 'root', '123456']
['URL', 'baidu', 'www.baidu.com']
(b'lock', 5, 2, 36, 357948, 0)
(b'lock OK--> ', 5, 2, 36, 357948, 0)
(b'get_i', 9943, b'\xbf\xe2y\x94\\a\t\xd0g\xbc\xd2\x95\xb5\x18\x9d\x86', (b'\xbf\xe2y\x94\\a\t\xd0g\xbc\xd2\x95\xb5\x18\x9d\x86', 357948, 357948, 357948, 40, 24))
(b'unlock', 5, 8, 36, 357948, 0)
 
 
