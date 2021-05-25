from class_methodDefine import *
from first_follow import *
from read_lexical_analyse_result import *
from output_temp_result import *

if __name__ == '__main__':
    # 构建语法分析器
    grammar = readGrammar()
    n_set, t_set, production = get_grammarAndProduction(grammar=grammar)

    # print(can_be_null("取地址", production, n_set, t_set))

    first_set = get_first_set(t_set, n_set, production)
    follow_set = get_follow_set(t_set, n_set, production, first_set)
    action_table = build_predict_table(n_set, t_set, first_set, follow_set, production)

    # 查看语法分析器构建结果
    print("语法分析器构建结果")
    print_test(grammar, n_set, t_set, first_set, follow_set, action_table, production)

    # 读取词法分析器结果
    lexical_result                          = read_lexical_result()
    const_table_list, identifier_table_list = read_symbol_table()
    new_lexical_result                      = replaceID_WithSymbol(lexical_result, const_table_list, identifier_table_list)

    # print("?")
    # for new in range(len(new_lexical_result)):
    #     print(new_lexical_result[new], end=" ")
    #     print(lexical_result[new])

    # 分析开始
    msg, used_production = grammar_analyse(n_set, t_set,
                                           new_lexical_result,
                                           action_table,
                                           first_set, follow_set)

    print(msg)

    # for u in used_production:
    #     print(u)