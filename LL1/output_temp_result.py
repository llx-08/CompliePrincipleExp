from LL1.class_methodDefine import *
from LL1.first_follow import *
from LL1.read_lexical_analyse_result import *
import xlwt


def print_action_table(action_table, t_set, n_set, production):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    font.underline = True  # 下划线
    font.italic = True  # 斜体字
    style.font = font  # 设定样式

    for i in range(len(t_set)):
        worksheet.write(0, i+1, t_set[i], style)

    line_count = 1
    for i in action_table:
        worksheet.write(line_count, 0, i, style)

        for j in range(len(t_set)):
            if t_set[j] not in action_table[i].keys():
                worksheet.write(line_count, j+1, "ERROR")

            elif len(action_table[i][t_set[j]]) == 2:  # 是产生式
                temp_str = action_table[i][t_set[j]][0] + "->"

                for r in action_table[i][t_set[j]][1]:
                    temp_str += r

                worksheet.write(line_count, j+1, temp_str)

            else:
                worksheet.write(line_count, j+1, action_table[i][t_set[j]])

        line_count += 1

    workbook.save('action_table.xls')  # 保存文件

    print("output action table success")
    # max_size = max(max(len(j) for j in action_table[i]) for i in action_table)+10
    # max_col  = len(t_set)
    # print(max_size)
    # print(max_col)

    # split_str = ""
    # for i in t_set:
    #
    #     print(i, end="")
    #     split_str += i
    #     for times in range(max_size - len(i)):
    #         print(" ", end="")
    #         split_str += " "
    #     print("|", end="")
    #     split_str += "|"
    #
    # print()
    # for i in range((max_col+1)*(max_size+1)):
    #     print("=", end="")
    # print()

    # for i in action_table:
    #     print(i, end="")
    #     for times in range(max_size - len(i)):
    #         print(" ", end="")
    #     print("|", end="")
    #
    #     for j in t_set:
    #         if j not in action_table[i].keys():
    #             print("ERROR", end="")
    #             for times in range(max_size - len("ERROR")):
    #                 print(" ", end="")
    #             print("|", end="")
    #         elif len(action_table[i][j]) == 2:  # 是产生式
    #             flag = -1
    #             for p_ind in range(len(production)):
    #                 if production[p_ind] == action_table[i][j]:
    #                     flag = p_ind
    #             print(flag, end="")
    #
    #             for times in range(max_size - len(str(flag))):
    #                 print(" ", end="")
    #         else:
    #             print(action_table[i][j], end="")
    #
    #             for times in range(max_size - len(action_table[i][j])):
    #                 print(" ", end="")
    #             print("|", end="")
    #
    #     print('\n' + '=' * ((max_size + 1) * max_col))


def print_test(grammar, n_set, t_set, first_set, follow_set, action_table, production):
    print("\n\n文法：")
    for g in grammar:
        print(g)

    print("\n\n非终结符集合：")
    for i in range(len(n_set)):
        if i % 10 == 0:
            print()
        print(n_set[i], end=" ")

    print("\n\n终结符集合：")
    for i in range(len(t_set)):
        if i % 10 == 0:
            print()
        print(t_set[i], end=" ")

    print("\n\nfirst 集：")

    for k in first_set:
        print("First ", end="")
        print(k, end=":    ")
        print(first_set[k])

    print("\n\nfollow 集：")

    for k in follow_set:
        print("Follow集 ", end="")
        print(k, end=":    ")
        print(follow_set[k])

    print()
    print_action_table(action_table, t_set, n_set, production)


# def loop_build_subtree(used_production, t_set, n_set, curr_index, right_index):
#     subtree_val = used_production[curr_index][right_index]
#     print("sub tree val: ")
#     print(subtree_val)
#
#     temp_tree_node = treeNode()
#
#     if subtree_val in t_set or subtree_val == "@":
#         print("?")
#         temp_tree_node.node_assign(subtree_val)
#
#     elif subtree_val in n_set:
#         curr_index += 1
#         for next_right_index in range(len(used_production[curr_index][1])):
#             temp_tree_node.add_child(loop_build_subtree(used_production, t_set, n_set, curr_index, right_index))
#
#     return temp_tree_node
#
#
# # 用顺序排列的产生式转为语法树
# def build_grammar_tree(used_production, t_set, n_set):
#     root = treeNode()
#     root.node_assign(used_production[0][0])
#     curr_index = 0
#
#     for right_index in range(len(used_production[curr_index][1])):
#         curr_index += 1
#         print("index: ", end="")
#         print(curr_index)
#         root.add_child(loop_build_subtree(used_production, t_set, n_set, curr_index, right_index))
#
#     return root
#
#
# def print_tree(root, t_set, n_set):  # 从根节点打印语法树
#     if root.val in t_set:
#         print(root.val)
#         return
#     elif root.val in n_set:
#         print(root.val, end=" —————— ")
#
#     for child in root.child_node:
#         print_tree(child, t_set, n_set)
#
#
# def createTree(dataSet, labels,featLabels):
#     classList = [example[-1] for example in dataSet]  # 取分类标签（是否出去玩：yes or no）
#     if classList.count(classList[0]) == len(classList):# 如果类别完全相同则停止继续划分
#         return classList[0]
#     if len(dataSet[0]) == 1:                          # 遍历完所有特征时返回出现次数最多的类标签
#         return majorityCnt(classList)
#     bestFeat = ChoosebestSplitData(dataSet)           # 选择最优特征
#     bestFeatLabel = labels[bestFeat]                  # 最优特征的标签
#     featLabels.append(bestFeatLabel)
#     myTree = {bestFeatLabel: {}}                      # 根据最优特征的标签生成树
#                                                       # 删除已经使用的特征标签
#                                                       # 得到训练集中所有最优解特征的属性值
#     featValues = [example[bestFeat] for example in dataSet]
#     uniqueVals = set(featValues)                      # 去掉重复的属性值
#     for value in uniqueVals:                          # 遍历特征，创建决策树
#         del_bestFeat = bestFeat
#         del_labels = labels[bestFeat]
#         del (labels[bestFeat])
#         myTree[bestFeatLabel][value] = createTree(SplitData(dataSet, bestFeat, value), labels, featLabels)
#         labels.insert(del_bestFeat, del_labels)
#     return myTree