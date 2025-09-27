#!/usr/bin/env python3

import numpy as np
import cv2
import random
from generator import TownGenerator  # import your generator class

# ------------------- Building Class -------------------
class Building:
    def __init__(self, x:int, y:int, size_x:int, size_y:int, category:str):
        self.x = x
        self.y = y
        self.size_y = size_y
        self.size_x = size_x
        self.category = category

    def center(self):
        return (self.x + self.size_x // 2, self.y + self.size_y // 2)

    def edges(self):
        return {
            'left': self.x,
            'right': self.x + self.size_x,
            'top': self.y,
            'bottom': self.y + self.size_y
        }

# ------------------- Map Setup -------------------
n_pixel_y = 300
n_pixel_x = 300
img = np.zeros((n_pixel_x, n_pixel_y, 3), dtype=np.uint8)

CATEGORY_COLORS = {
    'residential': [0, 255, 0],
    'commerce': [0, 0, 255],
    'industry': [255, 0, 0],
    'recreation': [128, 128, 128],
    'L': [0, 0, 0]
}

CATEGORY_INDEX = {
    'residential': 1,
    'commerce': 2,
    'industry': 3,
    'recreation': 4
}

# ------------------- Draw Functions -------------------
def draw_buildings(buildings):
    for b in buildings:
        color = CATEGORY_COLORS.get(b.category, [0, 0, 0])
        if b.category == 'L':
            draw_L_shape(img, L_BUILDING, b.x, b.y, color)
        else:
            img[b.y:b.y+b.size_y, b.x:b.x+b.size_x] = color

def draw_road(p1, p2):
    """Draw Manhattan-style road between two points."""
    x1, y1 = p1
    x2, y2 = p2
    road_color = [50, 50, 50]
    road_width = 2

    for w in range(-road_width, road_width+1):
        img[y1+w, min(x1, x2):max(x1, x2)+1] = road_color
    for w in range(-road_width, road_width+1):
        img[min(y1, y2):max(y1, y2)+1, x2+w] = road_color

def edge_connect(b1, b2):
    """Calculate points where road should stop at building edges."""
    e1 = b1.edges()
    e2 = b2.edges()

    c1 = b1.center()
    c2 = b2.center()

    if abs(c1[0] - c2[0]) > abs(c1[1] - c2[1]):  # Horizontal connection
        if c1[0] < c2[0]:
            start = (e1['right'], c1[1])
            end = (e2['left'], c2[1])
        else:
            start = (e1['left'], c1[1])
            end = (e2['right'], c2[1])
    else:  # Vertical connection
        if c1[1] < c2[1]:
            start = (c1[0], e1['bottom'])
            end = (c2[0], e2['top'])
        else:
            start = (c1[0], e1['top'])
            end = (c2[0], e2['bottom'])
    return start, end

def connect_nearest(buildings):
    """Connect each building to its nearest neighbor with edge stops."""
    for i, b in enumerate(buildings):
        nearest = None
        nearest_dist = float("inf")
        for j, other in enumerate(buildings):
            if i == j:
                continue
            c1 = b.center()
            c2 = other.center()
            dist = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = other
        if nearest:
            p1, p2 = edge_connect(b, nearest)
            draw_road(p1, p2)

L_BUILDING = [
    [1, 0],
    [1, 0],
    [1, 1]
]
BLOCK_SIZE = 10

def draw_L_shape(img, shape_grid, start_x, start_y, color):
    for row in range(len(shape_grid)):
        for col in range(len(shape_grid[0])):
            if shape_grid[row][col] == 1:
                x1 = start_x + col * BLOCK_SIZE
                y1 = start_y + row * BLOCK_SIZE
                x2 = x1 + BLOCK_SIZE
                y2 = y1 + BLOCK_SIZE
                img[y1:y2, x1:x2] = color

def rotate_building(building_grid):
    """Rotate a 2D building grid 90° clockwise."""
    rows = len(building_grid)
    cols = len(building_grid[0])
    rotated = [[0]*rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            rotated[c][rows - 1 - r] = building_grid[r][c]
    return rotated



# ------------------- MAIN -------------------
def main():
    # Step 1: Get inputs from TownGenerator
    print("=== Town Building Generator ===")
    population = int(input("Enter total population: "))
    area = float(input("Enter total area (sq km): "))
    print("Enter category percentages (sum should be 1.0):")
    categories = {}
    for cat in ['residential', 'commerce', 'industry', 'recreation']:
        categories[cat] = float(input(f"{cat.title()}: "))

    town = TownGenerator(population, area, categories)
    result = town.calculate_buildings()

    # Step 2: Build buildings list with spacing
    buildings = []
    category_buildings = result['category_buildings']
    sizes = {
        'residential': 15,
        'commerce': 20,
        'industry': 25,
        'recreation': 18
    }

    for cat in category_buildings:
        for _ in range(category_buildings[cat]):
            size = sizes[cat]
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, n_pixel_x - size - 1)
                y = random.randint(0, n_pixel_y - size - 1)
                too_close = False
                for b in buildings:
                    if abs(b.x - x) < size + 5 and abs(b.y - y) < size + 5:
                        too_close = True
                        break
                if not too_close:

                    if cat == 'commerce' and random.random() < 0.3:
                        buildings.append(Building(x, y, 0, 0, 'L'))
                    else:
                        buildings.append(Building(x, y, size, size, cat))
                    placed = True
                attempts += 1

    # Step 3: Set background to white
    img[:] = [255, 255, 255]

    # Step 4: Draw roads first with edge stops
    connect_nearest(buildings)

    # Step 5: Draw buildings after roads
    draw_buildings(buildings)

    # Step 6: Save map
    cv2.imwrite("map.png", img)
    print("Map generated and saved as map.png")

if __name__ == "__main__":
    main()
