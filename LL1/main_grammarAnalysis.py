from class_methodDefine import *
from first_follow import *


if __name__ == '__main__':
    # 构建语法分析器
    grammar                  = readGrammar()
    n_set, t_set, production = get_grammarAndProduction(grammar=grammar)
    first_set                = get_first_set(t_set, n_set, production)
    follow_set               = get_follow_set(t_set, n_set, production, first_set)
    action_table             = build_predict_table(n_set, t_set, first_set, follow_set, production)

    print("\n\n文法：")
    for g in grammar:
        print(g)

    print("\n\n非终结符集合：")
    for i in range(len(n_set)):
        if i % 10 == 0:
            print()
        print(n_set[i], end=" ")

    print("\n\n终结符集合：")
    for i in range(len(t_set)):
        if i % 10 == 0:
            print()
        print(t_set[i], end=" ")

    print("\n\nfirst 集：")
    count = 0
    for k in first_set:
        count += 1
        if count % 3 == 0:
            print()
        print(k, end=":  ")
        print(first_set[k], end=" ")

    print("\n\nfollow 集：")
    count = 0
    for k in follow_set:
        count += 1
        if count % 3 == 0:
            print()
        print(k, end=":  ")
        print(follow_set[k], end=" ")


    # 读取词法分析器结果
