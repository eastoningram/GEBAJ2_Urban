import math

class Building:
    def __init__(self, x:int, y:int, size_x:int, size_y:int, category:int, capacity: int, area:int):
        self.x = x
        self.y = y
        self.size_y = size_y
        self.size_x = size_x
        self.category = category
        self.capacity=capacity
        self.area=area


        # init from area
        if self.x <= 0:
            if self.category ==1:
                self.size_x=math.sqrt(area)
                self.size_y=math.sqrt(area)
            elif self.category ==2:
                self.size_x=math.sqrt(area/math.pi)
                self.size_y=math.sqrt(area/math.pi)
            else:
                self.size_x=math.sqrt(area)
                self.size_y=math.sqrt(area)
        self.x=int(self.x)
        self.size_x=int(self.size_x)
        self.y=int(self.y)
        self.size_y=int(self.size_y)


    def center(self):
        return (self.x + self.size_x // 2, self.y + self.size_y // 2)

    def display(self):
        print("x= " + str(self.x) + ", y=" +str(self.y)+ ", size_x= " \
            + str(self.size_x) + ", size_y= " + str(self.size_y) \
                + ", category= " + str(self.category) +", capacity= " + str(self.capacity) \
                    +", area: " + str(self.area))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,x):
        self.x=x

    def setY(self,y):
        self.y=y