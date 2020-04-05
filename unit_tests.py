from helper.vigor2130_helpers import encode
from helper.global_helpers import dict_path_value as dpv
import base64

assert encode('') == 'AA=='  # Not Base64
assert encode('1') == 'MQ=='
assert encode('12') == 'MTI='
assert encode('123') == 'MTIz'
assert encode('Canada12345') == 'Q2FuYWRhMTIzNDU='
assert encode('Canada12345') == base64.b64encode(bytes('Canada12345'.encode('utf-8'))).decode('utf-8')
assert encode('user') == 'dXNlcg=='

d = {'a': {'b': True}}

assert dpv(d=d, path='a.b')
assert dpv(d=d, path='a.c', default=123) == 123
assert dpv(d=d, path='a.c') is None
