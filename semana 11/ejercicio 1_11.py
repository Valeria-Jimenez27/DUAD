import math

class Circle:
    def __init__(self,radius):
        self.radius=radius


    def get_area(self):
        return math.pi * (self.radius**2)

circle1=Circle(10)
print("The area of the circle is:",circle1.get_area())