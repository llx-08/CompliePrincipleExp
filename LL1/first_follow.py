import sys
from LL1.class_methodDefine import *

sys.setrecursionlimit(10000000)


def can_be_null(symbol, production, n_set, t_set):
    print("symbol:can_be_null ", end="")
    print(symbol)
    flag = False
    for p in production:
        if p[0] == symbol:
            if p[1] == ["@"]:
                return True

            else:
                for right in p[1]:

                    if right in t_set and right != "@":
                        flag = False
                        break

                    flag_temp = False
                    if right in n_set:
                        flag_temp = can_be_null(right, production, n_set, t_set)

                    flag &= flag_temp

                if flag:
                    continue
                else:
                    break

    return flag


def get_first_set(t_symbol_set, n_symbol_set, production):
    all_first_set = {}

    for symbol in t_symbol_set:
        all_first_set[symbol] = [symbol]

    remain_add = []  # [a, b] 在最后需要将b的first集加入a中

    for symbol in n_symbol_set:
        for p in production:
            if p[0] == symbol:  # p[0]找到了对应的产生式 p[0] -> Y1Y2
                # X是非终结符，且有产生式X → Y1 Y2…… Yk

                if symbol not in all_first_set.keys():  # 还未创建symbol的first集
                    all_first_set[symbol] = []

                if p[1][0] in t_symbol_set:  # Y1是终结符,将Y1加入到FIRST(X)
                    all_first_set[symbol].append(p[1][0])

                elif p[1][0] in n_symbol_set:
                    # Y1是非终结符,将FIRST(Y1)–ε中的所有符号加入到FIRST(X)
                    # 还未创建需要加入的的first集
                    remain_add.append([symbol, p[1][0]])

                    if p[1][0] in all_first_set.keys():
                        for s in all_first_set[p[1][0]]:
                            if s != "@" and s not in all_first_set[symbol]:
                                all_first_set[symbol].append(s)

                elif p[1][0] == "@":  # X →ε是一个产生式
                    all_first_set[p[0]].append("@")

                # 只能是y1，y2等都能推出空才能让最终的推出空
                flag = 1
                for i in range(len(p[1])):  # i:Y1 Y2…… Yi-1 →ε,将FIRST(Yi)–ε中的所有符号加入到FIRST(X)
                    temp_symbol = p[1][i]

                    if can_be_null(temp_symbol, production, n_symbol_set, t_symbol_set):  # 该终结符能推出空
                        continue
                    else:
                        flag = 0

                        if p[1][i] not in all_first_set.keys():  # 还未创建需要加入的的first集
                            if [symbol, p[1][i]] not in remain_add:
                                remain_add.append([symbol, p[1][i]])
                        else:
                            for ss in all_first_set[p[1][i]]:
                                if ss != "@" and ss not in all_first_set[symbol]:
                                    all_first_set[symbol].append(ss)
                        break

                if flag == 1:  # Y1 Y2…… Yk可推导得到ε,  则将ε加入到FIRST(X)
                    all_first_set[p[0]].append("@")

    # print(all_first_set)
    # print("remaining")
    # print(remain_add)
    #
    # for i in range(len(remain_add)):  # 排序，保证添加first集的顺序
    #     for j in range(i, len(remain_add)):
    #         if remain_add[i][1] == remain_add[j][0]:
    #             temp = remain_add[i]
    #             remain_add[i] = remain_add[j]
    #             remain_add[j] = temp

    for r in remain_add:
        for t_symbol in all_first_set[r[1]]:
            if t_symbol != "@" and t_symbol not in all_first_set[r[0]]:
                all_first_set[r[0]].append(t_symbol)

    for r in reversed(remain_add):
        for t_symbol in all_first_set[r[1]]:
            if t_symbol != "@" and t_symbol not in all_first_set[r[0]]:
                all_first_set[r[0]].append(t_symbol)

    for a in all_first_set["函数块闭包"]:
        if a not in all_first_set["函数块"]:
            all_first_set["函数块"].append(a)

    return all_first_set


def test_first_set():
    grammar = [
        ["E", "T E'"],
        ["E'", "+ T E'"],
        ["E'", "@"],
        ["T", "F T'"],
        ["T'", "* F T'"],
        ["T'", "@"],
        ["F", "( E )"],
        ["F", "id"]
    ]

    n_set, t_set, production = get_grammarAndProduction(grammar=grammar)
    # print()

    first_set = get_first_set(t_set, n_set, production=production)
    # print("first set test result:")
    # for i in first_set:
    #     print(i, end="   ")
    #     print(first_set[i])

    return first_set, n_set, t_set, production


def get_follow_set(t_symbol_set, n_symbol_set, production, first_set):
    all_follow_set = {}

    remain_add = []  # 在最后将所有符号重新加入: 被添加，添加来源

    for n in n_symbol_set:
        all_follow_set[n] = []

    all_follow_set["程序开始"].append("$")

    for n in n_symbol_set:
        for p in production:
            if p[0] == n:  # 此处n为PPT中A
                rightside = p[1]

                if len(rightside) == 1:
                    B = rightside[0]
                    if B in n_symbol_set:
                        for follow_symbol in all_follow_set[n]:
                            if follow_symbol not in all_follow_set[B]:
                                all_follow_set[B].append(follow_symbol)
                        remain_add.append([B, n])

                for i in range(len(p[1]) - 1):
                    B = rightside[i]
                    beta = rightside[i + 1]

                    # 对于A→αB, 将FOLLOW(A)放入FOLLOW(B)中
                    if i+1 == len(p[1])-1 and beta in n_symbol_set:  # beta为最后一个，且为非终结符

                        for follow_symbol in all_follow_set[n]:
                            if follow_symbol not in all_follow_set[beta]:
                                all_follow_set[beta].append(follow_symbol)

                        remain_add.append([beta, n])

                        if B in n_symbol_set:
                            for pro in production:  # A→αBβ且β→ε
                                if pro[0] == beta and pro[1][0] == "@":
                                    remain_add.append([B, n])

                                    for f_a in all_follow_set[n]:
                                        if f_a not in all_follow_set[B]:
                                            all_follow_set[B].append(f_a)

                    # 对于A→αBβ的产生式，则将FIRST(β)–ε放入FOLLOW(B)
                    if B in n_symbol_set:

                        for first_symbol in first_set[beta]:
                            # print(first_symbol)
                            if first_symbol not in all_follow_set[B] and first_symbol != "@":
                                all_follow_set[B].append(first_symbol)

    for i in range(len(remain_add)):
        for re in reversed(remain_add):
            for f_symbol in all_follow_set[re[1]]:
                if f_symbol not in all_follow_set[re[0]]:
                    all_follow_set[re[0]].append(f_symbol)

    return all_follow_set


def test_follow_set():
    first_set, n_set, t_set, production = test_first_set()

    follow_set = get_follow_set(t_set, n_set, production, first_set)

    # print("follow set test result:")
    # for f in follow_set:
    #     print(f, end=": ")
    #     print(follow_set[f])

    return first_set, follow_set, n_set, t_set, production

