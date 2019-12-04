from vigor2130_helpers import encode


assert encode('') == 'AA=='
assert encode('1') == 'MQ=='
assert encode('12') == 'MTI='
assert encode('123') == 'MTIz'
assert encode('Canada210') == 'Q2FuYWRhMjEw'
assert encode('user') == 'dXNlcg=='
