# TEST extract target values
from src import helper
a = [1, 2, 3]
b = [{'a': 1}, {'a': 2}, {'a': 3}]
c = [('c', 1), ('a', 2),('d', 3)]
a_exp = [1, 2, 3]
b_exp = [1, 2, 3]
c_exp = [1, 2, 3]


a_result = helper.extract_target_values(a, None)
b_result = helper.extract_target_values(b, 'a')
c_result = helper.extract_target_values(c, 1)

assert a_result == a_exp
assert b_result == b_exp
assert c_result == c_exp
