from first_follow import *


class Stack(object):  # 实现栈，后面符号栈需要使用

    def __init__(self):
        # 创建空列表实现栈
        self.__list = []

    def is_empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self, item):
        # 压栈，添加元素
        self.__list.append(item)

    def pop(self):
        # 弹栈，弹出最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        # 取最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list[-1]

    def check_element(self):
        # 查看栈内元素，方便调试
        for i in self.__list:
            print(i, end=" ")
        print()


def readGrammar():
    pass


def get_grammarAndProduction(grammar):
    n_set = []
    t_set = []
    production = []

    for g in grammar:
        left = g[0]
        if left not in n_set:
            n_set.append(left)

    for g in grammar:
        right = g[1].split()

        for r in right:
            if r not in n_set:
                t_set.append(r)

    print("终结符")
    print(n_set)

    print("非终结符")
    print(t_set)

    for g in grammar:
        production.append([g[0], g[1].split()])

    print("产生式")
    print(production)

    return n_set, t_set, production


def build_predict_table(n_set, t_set, all_first_set, all_follow_set, production):
    # 初始化
    action_table = {}
    t_set.append("$")
    for A in n_set:
        for a in t_set:
            action_table[A] = {a: "ERR"}

    for p in production:
        A         = p[0]
        rightside = p[1]
        alpha     = rightside[0]

        for b in all_first_set[alpha]:
            if b in t_set:  # 对于FIRST(α)中的每个终结符号b，将产生式A→α加入到M[A, b]中
                action_table[A][b] = p

        if "@" in all_first_set[alpha]:
            for b in all_follow_set[A]:
                if b in t_set:
                    action_table[A][b] = p

    return action_table


def build_table_test(n_set, t_set, all_first_set, all_follow_set, production):
    print("build table test result:")

    action_table = build_predict_table(n_set, t_set, all_first_set, all_follow_set, production)
    print("raw table")

    for A in action_table:
        print(A)
        print(action_table[A])
    print("format output")

    for A in action_table:
        for b in action_table[A]:
            print(A, end=" ")
            print(b, end=": ")
            print(action_table[A][b], end="   ")
        print()

    return action_table


def error_solver(first_set, follow_set, type):
    if type == 1:  # 栈顶的终结符与当前输入符不匹配
        pass

    elif type == 2:  # 栈顶为非终结符A，面临的输入符为a，但分析表中M[A,a]为空
        pass


def grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set):
    # 初始化
    used_production = []  # 用到的产生式，按顺序排列，用于构建语法树

    symbol_stack = Stack()
    symbol_stack.push("$")
    symbol_stack.push("E")

    input_buffer.append("$")

    print("check init: symbol stack & input buffer")
    symbol_stack.check_element()
    print(input_buffer)

    curr_input_index = 0
    f = 1
    # 补一个判断语句
    while curr_input_index < len(input_buffer):

        input_symbol = input_buffer[curr_input_index]
        top_symbol = symbol_stack.top()

        print("check each loop: input symbol & stack top symbol")
        print(input_symbol)
        print(top_symbol)
        # if f == 10:
        #     break

        # 如果X是终结符，且X=a≠＄
        if top_symbol in t_set and top_symbol == input_symbol and top_symbol != "$":
            symbol_stack.pop()  # X出栈
            curr_input_index += 1  # 读取下一个输入符号

        elif top_symbol in t_set and top_symbol != input_symbol and top_symbol != "$":
            error_solver(first_set, follow_set, 1)  # X ≠ a则报错

        elif top_symbol in n_set:  # X是非终结符，查M[X，a]表
            if predict_table[top_symbol][input_symbol] == "ERR":  # 若M[X，a]=error，则报错
                error_solver(first_set, follow_set, 2)

            elif predict_table[top_symbol][input_symbol] is not None:  # 有产生式，非空
                used_production.append(predict_table[top_symbol][input_symbol])

                symbol_stack.pop()

                rightside = predict_table[top_symbol][input_symbol][1]  # 产生式右部

                for r in reversed(rightside):
                    if r != "@":
                        symbol_stack.push(r)

        elif top_symbol == "$" and input_symbol == "$":
            return "Grammar Analyse Success!", used_production

        else:
            error_solver(first_set, follow_set, 2)


def test_grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set):

    used_production = grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set)
    print("used production in order: ")
    for u in used_production:
        print(u)


def draw_grammar_tree(used_prediction):
    for prediction in used_prediction:
        pass


def loop_drawing():
    pass
