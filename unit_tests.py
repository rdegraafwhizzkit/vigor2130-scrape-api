from vigor2130 import Vigor2130

x = Vigor2130('', '', '')

assert x.encode('') == 'AA=='
assert x.encode('1') == 'MQ=='
assert x.encode('12') == 'MTI='
assert x.encode('123') == 'MTIz'
