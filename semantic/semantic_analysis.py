from LL1.tree_plot_by_graphvis import *


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


# 语义分析
# 包含的类型

type_list = ['auto', 'int', 'float', 'double', 'char', 'string', 'long', 'short', 'struct', 'register']
operator_list = ['+', '-', '*', '/']  # , '&', '|', '==', '>=', '<=', '%', '&&', '||'


class BinaryExpressionTree():

    def __init__(self, name):
        self.id     = -1
        self.name   = name  # 词法名称
        self.value  = 0
        self.leftC  = None
        self.rightC = None
        self.type   = None

    def set_id(self, id):  # 绘图所用编号
        self.id = id

    def set_value(self, val):  # 值
        self.value = val

    def set_type(self, type):
        self.type = type

    def set_left_child(self, node):
        self.leftC = node

    def set_right_child(self, node):
        self.rightC = node


def build_parse_tree_by_posix(expression, i_dict, id_count, c_dict, digit_count, s_dict):  # 后缀表达式
    stack_temp = Stack()
    temp_i_count = id_count
    temp_d_count = digit_count

    print("id c")
    print(id_count)
    print(i_dict)

    for e in expression:
        if e in operator_list:

            tree_temp = BinaryExpressionTree(e)

            right_node = stack_temp.top()
            stack_temp.pop()

            left_node = stack_temp.top()
            stack_temp.pop()

            tree_temp.set_left_child(left_node)
            tree_temp.set_right_child(right_node)

            print(left_node.value)
            print(right_node.value)

            if left_node.type != right_node.type:
                print("Error: 对"+left_node.type+"类型和"+right_node.type+"类型进行运算，类型检查出错")

            if e == '+':
                value = int(left_node.value) + int(right_node.value)
            elif e == '-':
                value = int(left_node.value) - int(right_node.value)
            elif e == '*':
                value = int(left_node.value) * int(right_node.value)
            elif e == '/':
                value = int(left_node.value) / int(right_node.value)

            tree_temp.set_value(value)
            tree_temp.set_type(left_node.type)
            stack_temp.push(tree_temp)

        elif e == 'id':
            node = BinaryExpressionTree(e)
            node.set_value(s_dict[i_dict[str(temp_i_count)]].value)
            node.set_type(s_dict[i_dict[str(temp_i_count)]].type)
            stack_temp.push(node)

            temp_i_count += 1
        elif e == 'digit':
            node = BinaryExpressionTree(e)
            node.set_value(c_dict[str(temp_d_count)])
            node.set_type('int')
            stack_temp.push(node)

            temp_d_count += 1

    return stack_temp.top()


def pre_order_test(tree):
    print(tree.name)

    if tree.leftC is not None:
        pre_order_test(tree.leftC)

    if tree.rightC is not None:
        pre_order_test(tree.rightC)


# 前序遍历获取边，节点信息
def pre_order(tree, id, nodes, edges):
    tree.set_id(id)
    nodes.append(tree)

    next_id = id + 1
    next_nodes = nodes
    next_edges = edges

    left = tree.leftC
    right = tree.rightC

    if left is not None:
        new_edge = Edge(tree, left)
        next_edges.append(new_edge)
        next_id, next_nodes, next_edges = pre_order(left, next_id, next_nodes, next_edges)
    if right is not None:
        new_edge = Edge(tree, right)
        next_edges.append(new_edge)
        next_id, next_nodes, next_edges = pre_order(right, next_id, next_nodes, next_edges)

    return next_id, next_nodes, next_edges


def expression_tree_write_in_dotfile(root, filename):
    final_id, final_nodes, final_edges = pre_order(root, 0, [], [])

    print("\nTree Nodes Generated:")
    for f in final_nodes:
        print(f.id, end=" ")
        print(f.name)

    print("\nEdge Nodes Generated:")
    for e in final_edges:
        print(e.begin.id, end=" ")
        print(e.begin.name, end=" -> ")

        print(e.end.id, end=" ")
        print(e.end.name)

    content = 'digraph grammar_tree {\n'

    for node in final_nodes:
        if node.name == 'id':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: addtype("
                                                                                                   "id.entry)")
        elif node.name == 'digit':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: "
                                                                                                   "digit.val=lexval")
        elif node.name == '+':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: "
                                                                                                     "node.val=left.val+right.val")
        elif node.name == '-':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: "
                                                                                                     "node.val=left.val-right.val")
        elif node.name == '*':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: "
                                                                                                     "node.val=left.val*right.val")
        elif node.name == '/':
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value) + "\nMove: "
                                                                                                     "node.val=left.val/right.val")
        else:
            content += '    "{}" [label="{}"];\n'.format(node.id, node.name + " Value: " + str(node.value))


            # 添加语义动作，求值，打印出来
    for edge in final_edges:
        start, end = edge.begin, edge.end
        content += '    "{}" -> "{}";\n'.format(start.id, end.id)
    content += '}'

    dotfile1 = '{}.dot'.format(filename)
    with open(dotfile1, 'w', encoding='utf-8') as f:
        f.write(content)
    f.close()

# root = build_parse_tree_by_posix(['id', 'id', '+'])