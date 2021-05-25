from ete3 import Tree
unrooted_tree = Tree( "((((H,K)D,(F,I)G)B,E)A,((L,(N,Q)O)J,(P,S)M)C);", format=1)
print (unrooted_tree)
#
#     /-A
#    |
#----|--B
#    |
#    |     /-C
#     \---|
#          \-D

rooted_tree = Tree( "(f,((A,B),f,(C,D)));" )
t = Tree(rooted_tree + ";", format=1)
print (t)