# 构建符号表
from LL1 import tree_plot_by_graphvis
from LL1 import main_grammarAnalysis
from LL1.read_lexical_analyse_result import *
from semantic.semantic_analysis import *


class Symbol:  # 在程序声明的时候建立对象
    def __init__(self, name, def_line, type, scope):
        self.name = name
        self.def_line = def_line
        self.quote_lines = []  # 引用行
        self.type = type  # int char float double array struct bool
        self.scope = scope  # 作用域
        self.value = None

    def setValue(self, value):
        self.value = value

    def add_quote_line(self, line):
        if line not in self.quote_lines:
            self.quote_lines.append(line)


lexical_list = read_lexical_result()
const_table_list, identifier_table_list = read_symbol_table()
new_lr_list = replaceID_WithSymbol(lexical_list,
                                   const_table_list,
                                   identifier_table_list)
c_dict = {}
i_dict = {}

# list -> dict
for c in const_table_list:
    c_dict[c[0]] = c[1]
for i in identifier_table_list:
    i_dict[i[0]] = i[1]


def getGrammarTree():
    tree_root = main_grammarAnalysis.grammarAnalysis()


# 遍历词法单元序列，使用栈记录作用域，遇到 { 入栈，遇到 } 出栈，每次入栈出栈打印符号表
def createSymbolTable(id_count, digit_count, s_dict, scope, i, in_def, symbol_line, symbol_type, p_id, is_expression, exp_value):
    #                第几个变量名，第几个常数名，当前符号表，作用域编号，第几个输入字符，是否在声明后，符号类型，前一个符号，是否在表达式中，表达式计算后的值

    # elif new_lr_list[i][0] in type_list:  # 声明
    #     symbol_type = new_lr_list[i][0]
    #     symbol_line = new_lr_list[i][1]
    #
    #     return symbol_type, symbol_line
    prev_id = None
    if in_def:  # 在声明内

        if new_lr_list[i][0] == 'id':
            symbol_name = i_dict[str(id_count)]
            prev_id = symbol_name

            if symbol_name in s_dict.keys():  # 重复定义
                print("Error:")
                print("      程序第" + str(new_lr_list[i][1]) + "行产生错误：对变量" + i_dict[str(id_count)] + "重复声明")

            else:
                new_s = Symbol(symbol_name, symbol_line, symbol_type, 0)

                s_dict[symbol_name] = new_s

            id_count += 1

    else:
        if new_lr_list[i][0] == 'id':
            symbol_name = i_dict[str(id_count)]
            prev_id = symbol_name
            if symbol_name in s_dict.keys():  # 在之前声明过
                s_dict[symbol_name].add_quote_line(new_lr_list[i][1])
            else:
                print("Error:")
                print("      程序第" + str(new_lr_list[i][1]) + "行产生错误：调用未声明的变量" + i_dict[str(id_count)])

            id_count += 1

    if new_lr_list[i][0] == '{':
        print('程序第'+symbol_line+'行进入新的作用域，进入前符号表为：')
        # 格式化输出当前符号表
        print_symbol_table(s_dict)
        scope += 1

    elif new_lr_list[i][0] == '}':
        print('程序第'+symbol_line+'行退出当前作用域，退出前符号表为：')
        # 格式化输出当前符号表
        print_symbol_table(s_dict)

        for k in s_dict.keys():
            if s_dict[k].scope == scope:
                s_dict.pop(k)

        scope -= 1

    if is_expression:
        s_dict[p_id].setValue(exp_value)

    return s_dict, scope, id_count, digit_count, prev_id


def print_symbol_table(symbol_table):
    # self.name = name
    # self.def_line = def_line
    # self.quote_lines = []  # 引用行
    # self.type = type  # int char float double array struct
    # self.scope = scope  # 作用域
    # self.value = None

    print("Symbol\t\tDefLine\t\tType\tValue\tScope")
    for k in symbol_table.keys():
        if len(k) < 4:
            print(k, end="\t\t\t")
        else:
            print(k, end="\t\t")

        print(symbol_table[k].def_line, end="\t\t\t")

        print(symbol_table[k].type, end="\t\t")
        print(symbol_table[k].value, end="\t\t")
        print(symbol_table[k].scope)

    print()


