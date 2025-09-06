class Node:
    def __init__(self, data):
        self.data=data
        self.left=None
        self.right=None       

class Binary_Tree:
    def __init__(self):
        self.root= None 

    def print_binary_tree(self, node):
        if node is not None:
            print(node.data)
            self.print_binary_tree(node.left)
            self.print_binary_tree(node.right)
    
    def structure_root(self,new_node):
        self.root=new_node      

binary_tree=Binary_Tree()
try:
    binary_tree.print_binary_tree(binary_tree.root)
except IndexError as e:
    print(f"Error: {e}")    

binary_tree.structure_root(Node("A"))
binary_tree.root.left=Node("B")
binary_tree.root.right=Node("C")

print("Binary Tree:")
binary_tree.print_binary_tree(binary_tree.root)