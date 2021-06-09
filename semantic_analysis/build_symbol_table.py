# 构建符号表
from LL1 import tree_plot_by_graphvis
from LL1 import main_grammarAnalysis


def getGrammarTree():
    tree_root = main_grammarAnalysis.grammarAnalysis()
