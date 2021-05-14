from class_methodDefine import *


def get_first_set(t_symbol_set, n_symbol_set, production):
    all_first_set = {}

    for symbol in t_symbol_set:
        all_first_set[symbol] = [symbol]

    remain_add = []  # [a, b] 在最后需要将b的first集加入a中

    for symbol in n_symbol_set:
        for p in production:
            if p[0] == symbol:  # p[0]找到了对应的产生式 p[0] -> Y1Y2
                # X是非终结符，且有产生式X → Y1 Y2…… Yk

                print("symbol", end=": ")
                print(symbol)

                if symbol not in all_first_set.keys():  # 还未创建symbol的first集
                    all_first_set[symbol] = []

                if p[1][0] in t_symbol_set:  # Y1是终结符,将Y1加入到FIRST(X)
                    all_first_set[symbol].append(p[1][0])

                elif p[1][0] in n_symbol_set:  # Y1是非终结符,将FIRST(Y1)–ε中的所有符号加入到FIRST(X)
                    if p[1][0] not in all_first_set.keys():  # 还未创建需要加入的的first集
                        remain_add.append([symbol, p[1][0]])
                    else:
                        for s in all_first_set[p[1][0]]:
                            if s != "@" and s not in all_first_set[symbol]:
                                all_first_set[symbol].append(s)

                elif p[1][0] == "@":  # X →ε是一个产生式
                    all_first_set[p[0]].append("@")

                # 只能是y1，y2等都能推出空才能让最终的推出空
                for i in range(len(p[1])):  # i:Y1 Y2…… Yi-1 →ε,将FIRST(Yi)–ε中的所有符号加入到FIRST(X)
                    flag = 0
                    for p2 in production:
                        if p[1][i] == p2[0] and p2[1][0] == "@":
                            flag = 1
                            break

                    if flag == 1:
                        continue
                    elif flag == 0:

                        if p[1][i] not in all_first_set.keys():  # 还未创建需要加入的的first集
                            remain_add.append([symbol, p[1][i]])
                        else:
                            for ss in all_first_set[p[1][i]]:
                                if ss != "@" and ss not in all_first_set[symbol]:
                                    all_first_set[symbol].append(ss)
                        break

                    if flag == 1:  # Y1 Y2…… Yk可推导得到ε,  则将ε加入到FIRST(X)
                        all_first_set[p[0]].append("@")

    print(all_first_set)
    print("remaining")
    print(remain_add)

    for r in remain_add:
        for t_symbol in all_first_set[r[1]]:
            if t_symbol != "@" and t_symbol not in all_first_set[r[0]]:
                all_first_set[r[0]].append(t_symbol)

    return all_first_set


def test_first_set():
    grammar = [
        ["S", "B A"],
        ["A", "B S"],
        ["A", "d"],
        ["B", "a A"],
        ["B", "b S"],
        ["B", "c"]
    ]

    n_set, t_set, production = \
        get_grammarAndProduction(grammar=grammar)
    print()

    first_set = get_first_set(t_set, n_set, production=production)
    print("first set test result:")
    print(first_set)


def get_follow_set():
    pass


if __name__ == '__main__':
    test_first_set()
