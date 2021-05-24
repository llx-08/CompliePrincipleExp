import copy
from ete3 import Tree, TreeStyle
from collections import defaultdict

'''

 将语法树在控制台画出
 
'''

tree = [None for i in range(300)]
dic = defaultdict(list)


class Node():
    def __init__(self, id, val, is_leaf):
        self.id = id
        self.val = val
        self.is_leaf = is_leaf
        self.sons = []

    def get_id(self):
        return self.id

    def add(self, son):
        self.sons.append(son)

    def get_val(self):
        return self.val

    def get_is_leaf(self):
        return self.is_leaf

    def get_sons(self):
        return self.sons


def read_int(line, index):
    re = ''
    while (line[index] >= '0' and line[index] <= '9'):
        re += line[index]
        index += 1;
    return re


def read_data():
    path = '../data/tree.txt'
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            f = 0
            left = None
            for i in range(len(line)):
                if line[i] == '(' and f == 0:
                    f = 1
                    id = read_int(line, i + 1)
                    i += len(id) + 1
                    val = read_int(line, i + 1)
                    i += len(val) + 1
                    is_leaf = read_int(line, i + 1)
                    # print(id, val, is_leaf, end='        ')
                    if tree[int(id)] == None:
                        tree[int(id)] = Node(int(id), int(val), int(is_leaf))
                        left = copy.deepcopy(tree[int(id)])
                    else:
                        left = copy.deepcopy(tree[int(id)])
                elif line[i] == '(' and f == 1:
                    id = read_int(line, i + 1)
                    i += len(id) + 1
                    val = read_int(line, i + 1)
                    i += len(val) + 1
                    is_leaf = read_int(line, i + 1)
                    # print(id, val, is_leaf, end='    ')
                    if tree[int(id)] == None:
                        tree[int(id)] = Node(int(id), int(val), int(is_leaf))
                        left_id = left.get_id()
                        # print(left_id)
                        tree[left_id].add(tree[int(id)])
                    else:
                        left_id = left.get_id()
                        tree[left_id].add(tree[int(id)])
        # print(tree[0])
        # print(dic[left])


def get_tree_string(node):
    sons = node.get_sons()
    tree_str = '('
    first = 0
    for son in sons:
        if son.get_is_leaf() == 0:  # 非终结符/非叶子结点
            if first == 0:
                tree_str += str(get_tree_string(son))
                first = 1
            else:
                tree_str += ',' + str(get_tree_string(son))
        else:
            if first == 0:
                tree_str += 'a' + str(son.get_val())
                first = 1
            else:
                tree_str += ',a' + str(son.get_val())
    return tree_str + ')A' + str(node.get_val()) + '--'


read_data()
print(len(tree[0].get_sons()))
tree_str = get_tree_string(tree[0])
print(tree_str)
t = Tree(tree_str + ";", format=1)
print(t.get_ascii(attributes=["name", "complex"]))
