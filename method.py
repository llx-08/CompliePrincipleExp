from classDefine_itemDefine import *
from classDefine_symbolDefine import *


def copy_item_with_diff_dot_pos(item, dot_pos):
    item.dot_position = dot_pos
    return item


def build_action_table():
    pass


def build_goto_table():
    pass


def goto(item_set, symbol, item_set_id):
    j = LR_1_item_set(item_set_id)

    for item in item_set.item_set:
        if item.symbol_next_dot() != symbol:
            continue
        if not j.item_exist(item):
            j.add_item(copy_item_with_diff_dot_pos(item, item.dot_position + 1))
    return j


def dfsItemSet(itemSet):
    if itemSet.all_dot_pos_end():  # 不能产生下一个项集
        return

    generate_symbol = []

    for item in itemSet:  # 可以产生下一个项集，遍历每一项点后面的符号，进行项目及的构建

        pass


def generateItemSet(grammar):
    # 初始化
    item_set_id = 0
    begin_item_set = LR_1_item_set(item_set_id)
    id = 0
    for g in grammar:
        left = g[0]
        right = g[1].split()
        next_ss = 1  # 怎么确定下一个搜索符号？
        dot_pos = 0
        temp_item = LR_1_item(id, left, right, next_ss, dot_pos)

        begin_item_set.add_item(temp_item)
        id += 1

    begin_item_set.print_item_set()

    return begin_item_set
    # flag = 1
    # while flag:
    #     item_set_id += 1


def splitGrammarIntoProduction(grammar):
    terminal_set = []
    non_terminal_set = []
    production = {}
    count = 0

    for g in grammar:
        left = g[0]
        if left not in terminal_set:
            terminal_set.append(left)

    for g in grammar:
        right = g[1].split()

        for r in right:
            if r not in terminal_set:
                non_terminal_set.append(r)

    print("终结符")
    for t in terminal_set:
        print(t, end=" ")

    print("\n非终结符")
    for n in non_terminal_set:
        print(n, end=" ")

    for g in grammar:
        production[count] = [g[0], g[1].split()]
        count += 1

    return terminal_set, non_terminal_set, production


# LR 分析器
def LR_analysis(action_table, goto_table, production, input_buffer):  # 符号输入串
    symbol_stack = Stack()  # 符号栈
    status_stack = Stack()  # 状态栈

    status_stack.push(0)
    # 初始化
    input_buffer.append("$")

    curr_input = 0

    while (not status_stack.is_empty()) and len(input_buffer) > curr_input:

        # 将
        symbol_stack.push(input_buffer[curr_input])
        curr_input += 1

        action_move = action_table[status_stack.top(), input_buffer[curr_input]]

        if action_move[0] == "s":
            status_stack.push(action_move[1])
        elif action_move[0] == "r":
            p_id = action_move[1]
            reduce_length = len(production[p_id][1])

            for i in range(reduce_length):
                symbol_stack.pop()

            symbol_stack.push(production[p_id][0])

            # ???: goto表怎么设置

        elif action_move[0] == "a":
            return "Grammar Analysis Success"
        else:
            return "Grammar Analysis Failed"


def test_goto(item_set):
    new_it = goto(item_set, "c", 1)
    print()
    new_it.print_item_set()
