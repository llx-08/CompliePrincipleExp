from classDefine_itemDefine import *


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
