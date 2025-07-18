from abc import ABC,abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def calculate_perimeter(self):
        pass


    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius


    def calculate_perimeter(self):
        return 2*math.pi*self.radius
    

    def calculate_area(self):
        return math.pi*(self.radius**2)

class Square(Shape):
    def __init__(self,side):
        self.side=side


    def calculate_perimeter(self):
        return 4*self.side
    

    def calculate_area(self):
        return self.side**2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width=width
        self.height=height

    def calculate_perimeter(self):
        return 2*(self.width+self.height)

    def calculate_area(self):
        return self.width*self.height

circle = Circle(radius=20)
square = Square(side=8)
rectangle = Rectangle(width=12, height=6)

print("The circle perimeter is:", circle.calculate_perimeter())
print("The circle area is:", circle.calculate_area())

print("The square perimeter is:", square.calculate_perimeter())
print("The square area is:", square.calculate_area())

print("The rectangle perimeter is:", rectangle.calculate_perimeter())
print("The rectangle area is:", rectangle.calculate_area())