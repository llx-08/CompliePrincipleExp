from symbol_id import keyword
from output_temp_result import *


def read_lexical_result():
    lexical_result_list = []
    lexical_result = open("../byyl_exp1/cmake-build-debug/result.txt")

    line = lexical_result.readline()
    while line:
        words = line.split()
        # print(words)
        if not words:
            break
        lexical_result_list.append([words[1], words[3], words[8]])
        line = lexical_result.readline()

    lexical_result.close()
    return lexical_result_list


def read_symbol_table():
    identifier_table_list = []
    const_table_list = []
    symbol_table = open("../byyl_exp1/cmake-build-debug/symbol_table.txt")

    line = symbol_table.readline()
    flag = 0

    while line:
        words = line.split()

        if words == [] or not line:
            line = symbol_table.readline()
            continue
        if words[0] == "Const":
            line = symbol_table.readline()
            flag = 0
            continue
        if words[0] == "Identifier":
            line = symbol_table.readline()
            flag = 1
            continue
        if words[0] == "Error":
            break

        if flag == 0:
            const_table_list.append([words[0], words[1]])
        if flag == 1:
            identifier_table_list.append([words[0], words[3]])

        line = symbol_table.readline()

    symbol_table.close()
    return const_table_list, identifier_table_list


def replaceID_WithSymbol(lexical_result_list, const_table_list, identifier_table_list):
    new_lr_list     = []
    new_symbol_dict = []
    new_const_dict  = []

    for l in lexical_result_list:
        if l[1] == "-":
            new_lr_list.append([keyword[int(l[0])], l[2]])

        elif l[0] == "68":  # 常量
            new_lr_list.append([keyword[int(l[0])], l[2]])
        elif l[0] == "71":  # 变量
            new_lr_list.append([keyword[int(l[0])], l[2]])

    return new_lr_list


def read_test():
    lexical_res = read_lexical_result()
    c, i = read_symbol_table()

    for i in range(len(lexical_res)):
        if i % 5 == 0:
            print()
        print(lexical_res[i], end="  ")

    print("\nconst:")
    print(c)
    print("symbol")
    print(i)

    new_lr = replaceID_WithSymbol(lexical_res, c, i)
    print(new_lr)


read_test()