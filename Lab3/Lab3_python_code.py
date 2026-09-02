#create classes
class Shape():
    def __init__(self):
        pass

class Rectangle(Shape):
    def __init__(self, l, w):
        self.length = l
        self.width = w
    def getArea(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self,r):
        self.radius = r
    def getArea(self): 
        return 3.14 * self.radius * self.radius

class Triangle(Shape):
    def __init__(self, b, h):
        self.base = b
        self.height = h
    def getArea(self): 
        return 0.5 * self.base * self.height

#read txt file 
file = open(r'C:\Users\jocel\DevSource\GEOG676Bravo\Bravo-online-GEOG676-fall26\Lab3\shape.txt', 'r')
lines = file.readlines()
file.close()

for line in lines:
    components = line.split(',')
    shape = components[0]

    if shape == 'Rectangle':
        rect = Rectangle(int(components[1]), int(components[2]))
        print('Area of rectangle is:', rect.getArea())
    elif shape == 'Circle': 
        cirl = Circle(int(components[1]))
        print('Area of circle is:', cirl.getArea())
    elif shape == 'Triangle':
        tri = Triangle(int(components[1]), int(components[2]))
        print('Area of triangle is:', tri.getArea())
    else: 
        pass
