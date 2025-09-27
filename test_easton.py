import numpy as np
import cv2

class Building:
    def __init__(self, x:int, y:int, size_x:int, size_y:int, category:int):
        self.x=x
        self.y=y
        self.size_y=size_y
        self.size_x=size_x
        self.category=category

n_pixel_y=300
n_pixel_x=300
img = np.zeros((n_pixel_x, n_pixel_y, 3), dtype=np.uint8)

def draw_building(b: Building):
    blue =[255, 0, 0]
    green = [0,255, 0]
    red =[0, 0, 255]
    if b.category==1:
        img[b.y:b.y+b.size_y,b.x:b.x+b.size_x] = red




# Set image to white
for y in range(n_pixel_y):
    for x in range(n_pixel_x):
        img[x,y]=[255, 255, 255]


b1=Building(50, 100, 10, 10, 1)
draw_building(b1)

cv2.imwrite("map.png", img)
#cv2.imshow("Map", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


