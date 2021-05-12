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


class symbol:

    def __init__(self, s_type, s_id, s_name):
        self.symbol_type = s_type
        self.symbol_id = s_id
        self.symbol_name = s_name

    def printSymbol(self):
        print("该符号编号为:", end="")
        print(self.symbol_id)
        print("该符号为", end="")
        if self.symbol_type == 1:
            print("终结符")
        else:
            print("非终结符")

    def equal_symbol(self, s):
        if self.symbol_type == s.symbol_type and self.symbol_id == s.symbol_id:
            return True

        return False


class LR_1_item:

    def __init__(self, id, left, right, next_ss, dot_pos):
        self.item_id = id
        self.leftside = left
        self.rightside = right
        self.next_search_symbol = next_ss
        self.dot_position = dot_pos

    def equal_item(self, i):
        if self.item_id != i.item_id or self.leftside != i.leftside \
                or self.next_search_symbol != i.next_search_symbol \
                or len(self.rightside) != len(i.rightside) \
                or self.dot_position != i.dot_position:
            return False

        for symbol_Ind in range(len(self.rightside)):
            if self.rightside[symbol_Ind] != i.rightside[symbol_Ind]:
                return False

        return True

    def print_item(self):
        print("该项编号为: ", end="")
        print(self.item_id)
        print("该项产生式为: ", end="")
        print(self.leftside.symbol_name, end="")
        print("->")
        for i in range(len(self.rightside)):
            if i == self.dot_position:
                print(" |dot| ", end="")
            print(self.rightside[i].symbol_name, end="")

        print("\n下一个搜索的符号为: " + self.next_search_symbol)

        return

    def if_dot_pos_last(self):
        return self.dot_position == len(self.rightside)

    def symbol_next_dot(self):
        if self.if_dot_pos_last():
            return -1
        else:
            return self.rightside[self.dot_position]


class LR_1_item_set:

    def __init__(self, id):
        self.item_set_id = id
        self.item_set = []

    def item_exist(self, item):
        for i in self.item_set:
            if i.equal_item(item):
                return True

        return False

    def add_item(self, item):
        if self.item_exist(item):
            return -1
        else:
            self.item_set.append(item)


# action_table: {
#     first : s   :操作类型
#     second: num :操作编号
# }
def build_action_table():
    pass


def build_goto_table():
    pass


def goto(item_set, symbol, item_set_id):

    j = LR_1_item_set(item_set_id)

    for item in item_set:
        if item.symbol_next_dot() != symbol:
            continue
        if not j.item_exist(item):
            j.add_item(item)
    return j


def generateItemSet(LR_item_set):
    # 初始化
    item_set_id = 0
    begin_item_set = LR_item_set(item_set_id)

    for g in grammar:
        left = g[0]
        right = g[1].split()
        next_ss = 1  # 怎么确定下一个搜索符号？
        dot_pos = 0
        temp_item = LR_1_item(id, left, right, next_ss, dot_pos)

        begin_item_set.add_item(temp_item)

    flag = 1
    while flag:
        item_set_id += 1
        

def splitGrammarIntoProduction(grammar):
    terminal_set     = []
    non_terminal_set = []
    production       = {}
    count            = 0

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

    while ~status_stack.is_empty() and len(input_buffer) > curr_input:

        # 将
        symbol_stack.push(input_buffer[curr_input])
        curr_input += 1

        action_move = action_table[status_stack.top(), input_buffer[curr_input]]

        if action_move[0] == "s":
            status_stack.push(action_move[1])
        elif action_move[0] == "r":
            id = action_move[1]

        elif action_move[0] == "a":
            return "Grammar Analysis Success"
        else:
            return "Grammar Analysis Failed"






grammar = [
    ["S1", "S"],
    ["S", "C C"],
    ["C", "c C"],
    ["C", "d"]
]

t_set, non_t_set, production = splitGrammarIntoProduction(grammar)
