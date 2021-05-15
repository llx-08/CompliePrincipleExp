from class_methodDefine import *
from first_follow import *


if __name__ == '__main__':
    first_set, follow_set, n_set, t_set, production = test_follow_set()
    predict_table = build_table_test(n_set, t_set, first_set, follow_set, production)
    input_buffer = "id + id * id".split()
    test_grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set)
