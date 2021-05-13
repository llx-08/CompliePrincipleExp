from classDefine_symbolDefine import *


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
        print(self.leftside, end="")
        print("->", end="")
        for i in range(len(self.rightside)):
            if i == self.dot_position:
                print(" |dot| ", end="")
            print(self.rightside[i], end="")

        print("\n下一个搜索的符号为: ", end="")
        print(self.next_search_symbol)

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

    def all_dot_pos_end(self):  # 是否所有都得项都是待规约项

        for item in self.item_set:
            if item.symbol_next_dot != -1:
                return False

        return True

    def print_item_set(self):
        print("第", end="")
        print(self.item_set_id, end="")
        print("项集包含的项为: ")

        for item in self.item_set:
            item.print_item()


# action_table: {
#     first : s   :操作类型
#     second: num :操作编号
# }


