from classDefine_itemDefine import *
from classDefine_symbolDefine import *
from method import *


if __name__ == '__main__':
    grammar = [
        ["S1", "S"],
        ["S", "C C"],
        ["C", "c C"],
        ["C", "d"]
    ]

    # t_set, non_t_set, production = splitGrammarIntoProduction(grammar)
    # test_goto()

    b_item_set = generateItemSet(grammar=grammar)
    test_goto(b_item_set)