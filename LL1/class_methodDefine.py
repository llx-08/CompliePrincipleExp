from LL1.output_temp_result import *
from semantic.build_symbol_table import *
from semantic.semantic_analysis import *


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
        print("Stack Element Include:", end="")
        for i in self.__list:
            print(i, end=" ")
        print()
        print()

    def add_child2top(self, child_node):
        self.__list[-1].child_list.append(child_node)


def readGrammar():
    wenfa = []
    wenfa_file = open("wenfa.txt", encoding="utf-8")

    line = wenfa_file.readline()

    while line:
        words = line.split()

        if words:
            wenfa.append([words[0], words[1:]])
        line = wenfa_file.readline()

    return wenfa


def get_grammarAndProduction(grammar):
    n_set = []
    t_set = []
    production = []

    for g in grammar:
        left = g[0]
        if left not in n_set:
            n_set.append(left)

    for g in grammar:
        right = g[1]

        for r in right:
            if r not in n_set and r not in t_set:
                t_set.append(r)

    # print("终结符")
    # print(n_set)
    #
    # print("非终结符")
    # print(t_set)

    for g in grammar:
        production.append([g[0], g[1]])

    # print("产生式")
    # print(production)

    return n_set, t_set, production


def build_predict_table(n_set, t_set, all_first_set, all_follow_set, production):
    # 初始化
    action_table = {}
    t_set.append("$")
    for A in n_set:
        for a in t_set:
            action_table[A] = {a: "ERR"}

    for p in production:
        A = p[0]
        rightside = p[1]
        alpha = rightside[0]

        for b in all_first_set[alpha]:
            if b in t_set:  # 对于FIRST(α)中的每个终结符号b，将产生式A→α加入到M[A, b]中
                action_table[A][b] = p

        if "@" in all_first_set[alpha]:
            for b in all_follow_set[A]:
                if b in t_set:
                    action_table[A][b] = p

    action_table["函数块"]["id"] = ['函数块', ['声明语句闭包', '函数块闭包']]
    action_table["函数块"]["if"] = ['函数块', ['声明语句闭包', '函数块闭包']]
    action_table["函数块"]["while"] = ['函数块', ['声明语句闭包', '函数块闭包']]
    action_table["函数块"]["for"] = ['函数块', ['声明语句闭包', '函数块闭包']]
    action_table["函数块"]["get"] = ['函数块', ['声明语句闭包', '函数块闭包']]
    action_table["函数块"]["put"] = ['函数块', ['声明语句闭包', '函数块闭包']]

    return action_table


def build_table_test(n_set, t_set, all_first_set, all_follow_set, production):
    print("build table test result:")

    action_table = build_predict_table(n_set, t_set, all_first_set, all_follow_set, production)

    print_action_table(action_table, t_set, n_set, production)

    return action_table


# 将FOLLOW(A)中的所有符号作为A的同步符号。跳过输入串中的一些词法单元，
# 直至遇到FOLLOW(A)中的元素，再把A从栈中弹出，很可能使分析继续进行；
# ②把FIRST(A)中的符号加到A的同步符号集，当FIRST(A)中的某个符号在输入中出现时，
# 可根据A继续进行语法分析；
# ③如果栈顶的终结符不能被匹配，就可以弹出该终结符，此时相当于把所有的符号都看作同步符号
def error_solver(first_set, follow_set, type, symbol_stack,
                 input_buffer, curr_input_index, curr_line):
    A = symbol_stack.top()
    print("ERROR OCCURRED: Error Type :", end="")
    if type == 1:  # 栈顶的终结符与当前输入符不匹配
        print("栈顶的终结符与当前输入符不匹配")
    elif type == 2:
        print("分析表中此格为空")
    print("Current Symbol:", end=" ")
    print(A)

    if A == ')':
        print("丢失右部括号")
    elif A == '(':
        print("丢失左部括号")
    elif A in operator_list:
        print("丢失运算符")
    elif A == 'id':
        print("丢失操作数")

    print("Current Input :", end=" ")
    print(input_buffer[curr_input_index])
    print("Current Line :", end="")
    print(curr_line)

    if type == 1:  # 栈顶的终结符与当前输入符不匹配
        print("Pop Symbol Stack Top: ", end="")
        print(symbol_stack.top())
        symbol_stack.pop()

    elif type == 2:  # 栈顶为非终结符A，面临的输入符为a，但分析表中M[A,a]为空
        follow_set_A = follow_set[A]
        next_input_index = curr_input_index

        while input_buffer[next_input_index] not in follow_set_A:
            print("Skip Symbol: ", end="")
            print(input_buffer[next_input_index])
            next_input_index += 1
            print("Current Symbol: ", end="")
            print(input_buffer[next_input_index])

        print("Error Solver Finished\n")
        return next_input_index

    # raise Exception("ERROR")


# 依次按顺序读入，
# 读到数字：直接输出；
# 读到一般运算符：如果栈顶的运算符优先级不低于该运算符，则输出栈顶运算符并使之出栈，
# 直到栈空或不满足上述条件为止；然后入栈；
# 读到左括号：直接入栈；
# 读到右括号：输出栈顶运算符并使之出栈，直到栈顶为左括号为止；令左括号出栈。
# 当读入完毕时，依次输出并弹出栈顶运算符，直到栈被清空。
def shuntingYardAlgor(expression):
    Pri = {'*': 2, '/': 2, '+': 1, '-': 1}  # 制定优先级

    operator_stack = Stack()
    postfix_result = []

    for e in expression:
        print(e)
        if e in Pri.keys():
            if operator_stack.is_empty():
                operator_stack.push(e)

            elif Pri[e] >= Pri[operator_stack.top()]:

                while operator_stack.top() is not None and Pri[e] <= Pri[operator_stack.top()]:
                    top_operator = operator_stack.top()
                    postfix_result.append(top_operator)
                    operator_stack.pop()
                    if operator_stack.top() is None:
                        break

                operator_stack.push(e)

        elif e == '(':
            operator_stack.push(e)
        elif e == ')':
            while operator_stack.top() != '(':
                top_operator = operator_stack.top()
                postfix_result.append(top_operator)

            top_operator = operator_stack.top()
            postfix_result.append(top_operator)

        elif e == 'digit' or e == 'id':
            postfix_result.append(e)

    while operator_stack.top() is not None:
        top_operator = operator_stack.top()
        postfix_result.append(top_operator)
        operator_stack.pop()

    return postfix_result


def grammar_analyse(n_set, t_set, input_symbol_buffer, predict_table, first_set, follow_set):
    # 初始化
    used_production = []  # 用到的产生式，按顺序排列，用于构建语法树

    symbol_stack = Stack()
    symbol_stack.push("$")
    symbol_stack.push("程序开始")

    input_buffer = []
    line_buffer = []

    for n in input_symbol_buffer:
        input_buffer.append(n[0])
        line_buffer.append(n[1])

    input_buffer.append("$")
    line_buffer.append("$")

    curr_input_index = 0

    # 符号表参数
    id_count = 1
    digit_count = 1
    s_dict = {}
    scope = 0
    in_def = False
    symbol_type = None

    is_expression = False
    prev_id = None
    dot_count = 0
    exp_value = 0

    while curr_input_index < len(input_buffer):

        input_symbol = input_buffer[curr_input_index]
        curr_line = line_buffer[curr_input_index]
        # check
        print("input buffer:", end=" ")
        print(input_symbol)
        print("at line:", end=" ")
        print(curr_line)

        symbol_stack.check_element()
        top_symbol = symbol_stack.top()

        # 如果X是终结符，且X=a≠＄
        if top_symbol in t_set and top_symbol == input_symbol and top_symbol != "$":

            if input_symbol in type_list:
                symbol_type = input_symbol
                in_def = True
            elif input_symbol == ';':
                in_def = False
            elif input_symbol == '=':  # 赋值语句，后面可能跟表达式或单个值，进行语法制导翻译
                is_expression = True
                temp_index = curr_input_index + 1
                expression = []

                while input_buffer[temp_index] != ';':
                    expression.append(input_buffer[temp_index])
                    temp_index += 1

                posix_exp = shuntingYardAlgor(expression)  # 转为后缀表达式
                print("posix")
                print(posix_exp)

                print_symbol_table(s_dict)
                root = build_parse_tree_by_posix(posix_exp, i_dict, id_count, c_dict, digit_count, s_dict)
                expression_tree_write_in_dotfile(root, 'exp'+str(dot_count))

                exp_value = root.value

                dot_count += 1
            elif input_symbol == 'digit':
                digit_count += 1

            symbol_stack.pop()  # X出栈

            # 读取下一个输入符号时，判断符号表是否需要更新
            s_dict, scope, id_count, digit_count, prev_id = createSymbolTable(
                id_count,
                digit_count,
                s_dict,
                scope,
                curr_input_index,
                in_def,
                curr_line,
                symbol_type,
                prev_id,
                is_expression,
                exp_value
            )
            is_expression = False
            curr_input_index += 1  # 读取下一个输入符号

        elif top_symbol in t_set and top_symbol != input_symbol and top_symbol != "$":
            error_solver(first_set, follow_set, 1, symbol_stack, input_buffer, curr_input_index, curr_line)  # X ≠ a则报错

        elif top_symbol in n_set:  # X是非终结符，查M[X，a]表

            if input_symbol not in predict_table[top_symbol].keys() or \
                    predict_table[top_symbol][input_symbol] == "ERR":  # 若M[X，a]=error，则报错

                curr_input_index = error_solver(first_set,
                                                follow_set,
                                                2,
                                                symbol_stack,
                                                input_buffer,
                                                curr_input_index,
                                                curr_line)

            elif len(predict_table[top_symbol][input_symbol]) == 2:  # 有产生式，非空
                # 若M[X，a]=X→UVW，则X出栈，W、V、U依次入栈
                used_production.append(predict_table[top_symbol][input_symbol])

                rightside = predict_table[top_symbol][input_symbol][1]  # 产生式右部

                symbol_stack.pop()

                for r in reversed(rightside):
                    if r != "@":
                        symbol_stack.push(r)

                # current_root = tree_node_stack.pop()

        elif top_symbol == "$" and input_symbol == "$":
            print("语法分析结束时符号表为：")
            print_symbol_table(s_dict)
            return "Grammar Analyse Success!", used_production

        else:
            curr_input_index = error_solver(first_set,
                                            follow_set,
                                            2,
                                            symbol_stack,
                                            input_buffer,
                                            curr_input_index,
                                            curr_line)


def test_grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set):
    info, used_production = grammar_analyse(n_set, t_set, input_buffer, predict_table, first_set, follow_set)
    print("used production in order: ")
    for u in used_production:
        print(u)

    return used_production


# print(shuntingYardAlgor(['id', '+', 'id', '-', 'id', '+', 'id']))
