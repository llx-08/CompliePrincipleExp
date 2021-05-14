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


def build_predict_table(all_first_set):

    for first_set in all_first_set:


        pass


def grammar_analyse(input_buffer, symbol_stack, predict_table):
    pass


def draw_grammar_tree():

    pass