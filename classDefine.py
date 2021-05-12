class symbol:

    def __init__(self, s_type, s_id, s_name):
        self.symbol_type = s_type
        self.symbol_id   = s_id
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
        self.item_id            = id
        self.leftside           = left
        self.rightside          = right
        self.next_search_symbol = next_ss
        self.dot_position       = dot_pos

    def equal_item(self, i):
        if self.item_id != i.item_id or self.leftside != i.leftside \
                or self.next_search_symbol != i.next_search_symbol \
                or len(self.rightside) != len(i.rightside)\
                or self.dot_position != i.dot_position :
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

        print("\n下一个搜索的符号为: "+self.next_search_symbol)

        return



def splitGrammarIntoProduction(grammar):

    terminal_set    = []
    non_terminal_set = []

    for g in grammar:
        left  = g[0]
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

    return terminal_set, non_terminal_set

def buildSymbolSet(terminal_set, non_terminal_set):
    terminal_symbol_set     = []
    non_terminal_symbol_set = []

    for t in terminal_set:
        symbol()

def generateItemSet(LR_item_set):

    # 初始化

    for g in grammar:
        left    = g[0]
        right   = g[1].split()
        next_ss =
        dot_pos = 0
        temp_item = LR_1_item(id, left, right, next_ss, dot_pos)


    for lr_item in LR_item_set:
        




grammar = [
    ["S1", "S"],
    ["S", "C C"],
    ["C", "c C"],
    ["C", "d"]
]

t_set, non_t_set = splitGrammarIntoProduction(grammar)

