from collections import namedtuple

from graphviz import Digraph


class TreeNode:

    def __init__(self, name, is_leaf):
        self.id         = -1
        self.child_list = []
        self.name       = name
        self.is_leaf    = is_leaf
        self.father     = None

    def add_child(self, child_node):
        self.child_list.append(child_node)

    def node_is_leaf(self):
        return self.is_leaf

    def set_father(self, father):
        self.father = father

    def set_id(self, id):
        self.id = id


class Edge:
    def __init__(self, begin, end):
        self.begin = begin
        self.end   = end


def find_tree_node(tree_node_set, id):
    for t in tree_node_set:
        if t.id == id:
            return t


def build_tree_struct(used_production, n_set, t_set):
    grammar_tree_root = TreeNode(used_production[0][0], False)

    root, new_ind = build_tree(used_production, 0, grammar_tree_root, n_set, t_set)

    return root


def build_tree(used_production, pro_ind, root, n_set, t_set):
    # 增添语法制导翻译，在建树的过程中，每次root add_child 后，return前会进行语法制导翻译

    right = used_production[pro_ind][1]

    new_ind = pro_ind + 1
    for r in right:

        if r in t_set:
            root.add_child(TreeNode(r, True))

        else:
            temp_node = TreeNode(r, False)
            new_root, new_ind = build_tree(used_production, new_ind, temp_node, n_set, t_set)
            root.add_child(new_root)

    return root, new_ind


def preorder_traversal(root, id, nodes, edges):
    # print("root")
    # print(root.value)
    root.set_id(id)
    nodes.append(root)

    next_id    = id+1
    next_nodes = nodes
    next_edges = edges

    for i in root.child_list:
        new_edge = Edge(root, i)
        next_edges.append(new_edge)
        next_id, next_nodes, next_edges = preorder_traversal(i, next_id, next_nodes, next_edges)

    return next_id, next_nodes, next_edges


def write_in_dotfile(root):
    final_id, final_nodes, final_edges = preorder_traversal(root, 0, [], [])

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
    content += 'edge [fontname="SimHei"];\n' \
               'node [shape=box, fontname="SimHei"];'

    for node in final_nodes:
        content += '    "{}" [label="{}"];\n'.format(node.id, node.name)

    for edge in final_edges:
        start, end = edge.begin, edge.end
        content += '    "{}" -> "{}";\n'.format(start.id, end.id)
    content += '}'

    dotfile1 = '{}.dot'.format("tree")
    with open(dotfile1, 'w', encoding='utf-8') as f:
        f.write(content)
    f.close()


def tree_plot(used_production, n_set, t_set):
    # used_production = [
    #         ['E', ['A', 'B', 'c']],
    #         ['A', ['c', 'D']],
    #         ['D', ['id']],
    #         ['B', ['c']]
    #     ]
    # n_set = ['E', 'A', 'B', 'D']
    # t_set = ['c', 'id']

    root = build_tree_struct(used_production, n_set, t_set)
    write_in_dotfile(root)

    return root


# if __name__ == '__main__':
#     tree_plot(used_production, n_set, t_set)