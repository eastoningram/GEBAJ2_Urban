#!/usr/bin/env python3

import numpy as np
import cv2
import random

class Building:
    def __init__(self, x:int, y:int, size_x:int, size_y:int, category:int):
        self.x = x
        self.y = y
        self.size_y = size_y
        self.size_x = size_x
        self.category = category

    def center(self):
        return (self.x + self.size_x // 2, self.y + self.size_y // 2)

n_pixel_y = 300
n_pixel_x = 300
img = np.zeros((n_pixel_x, n_pixel_y, 3), dtype=np.uint8)

def draw_buildings(buildings):
    blue  = [255, 0, 0]
    red   = [0, 0, 255]
    green = [0, 255, 0]
    black = [0, 0, 0]
    grey  = [128, 128, 128]

    for b in buildings:
        if b.category == 1:
            img[b.y:b.y+b.size_y, b.x:b.x+b.size_x] = green
        elif b.category == 2:
            center_x = b.x + b.size_x // 2
            center_y = b.y + b.size_y // 2
            radius = min(b.size_x, b.size_y) // 2
            cv2.circle(img, (center_x, center_y), radius, green, -1)
        elif b.category == 3:
            img[b.y:b.y+b.size_y, b.x:b.x+b.size_x] = blue
        elif b.category == 4:
            img[b.y:b.y+b.size_y, b.x:b.x+b.size_x] = grey
        else:
            img[b.y:b.y+b.size_y, b.x:b.x+b.size_x] = black

def draw_road(p1, p2):
    """Draw simple Manhattan (L-shaped) road between two points."""
    x1, y1 = p1
    x2, y2 = p2
    road_color = [50, 50, 50]

    # Horizontal segment
    img[y1, min(x1, x2):max(x1, x2)+1] = road_color
    # Vertical segment
    img[min(y1, y2):max(y1, y2)+1, x2] = road_color

def connect_nearest(buildings):
    """Connect each building to its nearest neighbor with a road."""
    for i, b in enumerate(buildings):
        c1 = b.center()
        nearest = None
        nearest_dist = float("inf")

        for j, other in enumerate(buildings):
            if i == j:
                continue
            c2 = other.center()
            dist = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])  # Manhattan distance
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = c2

        if nearest:
            draw_road(c1, nearest)


# ---- MAIN ----

# Set image to white
img[:] = [255, 255, 255]

# Random buildings with spacing
buildings = []
for _ in range(8):
    size_x = random.randint(10, 30)
    size_y = random.randint(10, 30)
    x = random.randint(0, n_pixel_x - size_x - 1)
    y = random.randint(0, n_pixel_y - size_y - 1)
    category = random.randint(1, 4)

    too_close = False
    for b in buildings:
        if abs(b.x - x) < 20 and abs(b.y - y) < 20:
            too_close = True
            break
    if not too_close:
        buildings.append(Building(x, y, size_x, size_y, category))

# --- DRAW ROADS FIRST ---
connect_nearest(buildings)

# --- DRAW BUILDINGS ON TOP ---
draw_buildings(buildings)

cv2.imwrite("map.png", img)


cv2.imwrite("map.png", img)
#cv2.imshow("Map", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
