class Node:
    def __init__(self, data, next=None):
        self.data=data
        self.next=next

class Double_Ended_Queue:
    head: Node

    def __init__(self):
        self.head= None
        self.tail= None 


    def print_Double_Ended_Queue_structure(self):
        current=self.head
        while current is not None:
            print(current.data)
            current =current.next


    def push_left(self, new_node):
        if self.head is None:
            self.head=self.tail=new_node
        else:
            new_node.next= self.head
            self.head=new_node


    def push_right(self, new_node):
        if self.tail is None:
            self.head= self.tail= new_node
        else:
            self.tail.next= new_node
            self.tail= new_node


    def pop_left(self):
        if self.head is None:
            raise IndexError("Pop left from empty deque")
        popped= self.head
        self.head=self.head.next
        if self.head is None:
            self.tail=None
        return popped


    def pop_right(self):
        if self.tail is None:
            raise IndexError("Pop right from empty deque")  
        popped= self.tail
        if self.head==self.tail:
            self.head=self.tail =None
        else:
            current=self.head
            while current.next!= self.tail:
                current=current.next
            current.next=None
            self.tail =current
        return popped

double_ended_queue = Double_Ended_Queue()
try:
    double_ended_queue.pop_left()
except IndexError as e:
    print(f"Error: {e}")

try:
    double_ended_queue.pop_right()      
except IndexError as e:
    print(f"Error: {e}")

double_ended_queue.push_right(Node("3"))
double_ended_queue.push_right(Node("2"))
double_ended_queue.push_left(Node("1"))    
print("Pushing:")
double_ended_queue.print_Double_Ended_Queue_structure()

print("Pop left:", double_ended_queue.pop_left().data)
print("Pop right:", double_ended_queue.pop_right().data)
print("Popping:")
double_ended_queue.print_Double_Ended_Queue_structure()
