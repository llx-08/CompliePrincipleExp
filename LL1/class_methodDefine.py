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


def build_predict_table(all_first_set, all_follow_set, production):
    for first_set in all_first_set:
        pass


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
    symbol_stack.push("S")

    input_buffer.append("$")

    curr_input_index = 0

    # 补一个判断语句
    while curr_input_index < len(input_buffer):

        input_symbol = input_buffer[curr_input_index]
        top_symbol = symbol_stack.top()

        # 如果X是终结符，且X=a≠＄
        if top_symbol in t_set and top_symbol == input_symbol and top_symbol != "@":
            symbol_stack.pop()  # X出栈
            curr_input_index += 1  # 读取下一个输入符号

        elif top_symbol in t_set and top_symbol != input_symbol and top_symbol != "@":
            error_solver(first_set, follow_set, 1)  # X ≠ a则报错

        elif top_symbol in n_set:  # X是非终结符，查M[X，a]表
            if predict_table[top_symbol][input_symbol] == "ERR":  # 若M[X，a]=error，则报错
                error_solver(first_set, follow_set, 2)

            elif predict_table[top_symbol][input_symbol] is not None:  # 有产生式，非空
                used_production.append(predict_table[top_symbol][input_symbol])

                symbol_stack.pop()

                rightside = predict_table[top_symbol][input_symbol][1]  # 产生式右部

                for r in reversed(rightside):
                    symbol_stack.push(r)

        elif top_symbol == "$" and input_symbol == "$":
            return "Grammar Analyse Success!", used_production

        else:
            error_solver(first_set, follow_set, 2)


def draw_grammar_tree(used_prediction):

    for prediction in used_prediction:
        pass


def loop_drawing():

    pass
