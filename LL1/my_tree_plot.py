from ete3 import Tree


class TreeNode:

    def __init__(self, id, val, is_leaf):
        self.id         = id
        self.child_list = []
        self.value      = val
        self.is_leaf    = is_leaf
        self.father     = None

    def add_child(self, child_node):
        self.child_list.append(child_node)

    def node_is_leaf(self):
        return self.is_leaf

    def set_father(self, father):
        self.father = father


def find_tree_node(tree_node_set, id):
    for t in tree_node_set:
        if t.id == id:
            return t


def build_tree_struct(used_production, n_set, t_set):
    grammar_tree_root = TreeNode(0, used_production[0][0], False)

    root = build_tree(used_production, 0, grammar_tree_root, n_set, t_set)

    return root


def build_tree(used_production, pro_ind, root, n_set, t_set):
    print("pro index := ", end="")
    print(pro_ind)
    print("root value := ", end="")
    print(root.value)
    right = used_production[pro_ind][1]
    print(right)
    count = 1
    for r in right:
        print("     curr r := ", end="")
        print(r)
        if r in t_set:
            root.add_child(TreeNode(0, r, True))

        else:
            temp_node = TreeNode(0, r, False)
            root.add_child(build_tree(used_production, pro_ind+count, temp_node, n_set, t_set))
            count += 1

    return root


def tree_str_generate(tree_root):
    if not tree_root.child_list:
        return tree_root.value

    #
    subtree_str_list = []
    for u in tree_root.child_list:
        subtree_str = tree_str_generate(u)
        subtree_str_list.append(subtree_str)

    return_str = "("
    for str in subtree_str_list:
        return_str += str
        if str != subtree_str_list[-1]:
            return_str += ", "
        else:
            return_str += ")"
            return_str += tree_root.value

    return return_str+";"


def tree_plot(tree_str):
    t = Tree(tree_str, format=1)
    # we add a custom annotation to the node named A

    # we add a complex feature to the A node, consisting of a list of lists

    print(t.get_ascii(attributes=["name", "complex"]))

# "((A, B)subtree1, (C, D)subtree2)root;"


if __name__ == '__main__':
    used_production = [
        ['E', ['A', 'B', 'c']],
        ['A', ['c', 'D']],
        ['D', ['id']],
        ['B', ['c']]
    ]
    n_set = ['E', 'A', 'B', 'D']
    t_set = ['c', 'id']

    root = build_tree_struct(used_production, n_set, t_set)

    tree_str = tree_str_generate(root)

    print(tree_str)

    tree_plot(tree_str)
