class Node:
    def __init__(self, data, next=None):
        self.data=data
        self.next=next

class Stack:
    def __init__(self):
        self.head=None


    def print_stack_structure(self):
        current_node=self.head
        while current_node is not None:
            print(current_node.data)
            current_node=current_node.next


    def push(self, new_node):
        new_node.next=self.head
        self.head=new_node


    def pop(self):
        if self.head is None:
            return None
        popped = self.head
        self.head = self.head.next
        return popped

stack = Stack()
try:
    stack.pop()
except IndexError as e:
    print(f"Error: {e}")

print("Adding the third node to the stack:")
stack.push(Node("Hi, I'm the third node"))
stack.push(Node("Hi, I'm the second node"))
stack.push(Node("Hi, I'm the first node"))
stack.print_stack_structure()

print("Popping the top node from the stack:")
stack.pop()
