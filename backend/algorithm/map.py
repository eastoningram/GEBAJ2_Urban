#!/usr/bin/env python3

import numpy as np
import cv2
import random
from generator.generator import TownGenerator

# ---- CONFIG ----
n_pixel_y = 300
n_pixel_x = 300
img = np.zeros((n_pixel_y, n_pixel_x, 3), dtype=np.uint8)

# ---- DRAWING FUNCTIONS ----
def draw_buildings(buildings):
    blue  = [255, 0, 0]
    red   = [0, 0, 255]
    green = [0, 255, 0]
    black = [0, 0, 0]
    grey  = [128, 128, 128]

    for b in buildings:
        # Clip building coordinates to image bounds
        x1 = max(0, min(b.x, n_pixel_x-1))
        y1 = max(0, min(b.y, n_pixel_y-1))
        x2 = max(0, min(b.x + b.size_x, n_pixel_x))
        y2 = max(0, min(b.y + b.size_y, n_pixel_y))

        if b.category == 1:
            img[y1:y2, x1:x2] = green
        elif b.category == 2:
            center_x, center_y = b.center()
            center_x = max(0, min(center_x, n_pixel_x-1))
            center_y = max(0, min(center_y, n_pixel_y-1))
            radius = min(b.size_x, b.size_y) // 2
            cv2.circle(img, (center_x, center_y), radius, green, -1)
        elif b.category == 3:
            img[y1:y2, x1:x2] = blue
        elif b.category == 4:
            img[y1:y2, x1:x2] = grey
        else:
            img[y1:y2, x1:x2] = black

def draw_road(p1, p2):
    """Draw Manhattan (L-shaped) road between two points safely."""
    x1, y1 = p1
    x2, y2 = p2
    road_color = [50, 50, 50]

    # Clip to image bounds
    x1 = max(0, min(x1, n_pixel_x-1))
    x2 = max(0, min(x2, n_pixel_x-1))
    y1 = max(0, min(y1, n_pixel_y-1))
    y2 = max(0, min(y2, n_pixel_y-1))

    # Horizontal then vertical
    img[y1, min(x1, x2):max(x1, x2)+1] = road_color
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
if __name__ == "__main__":
    # Set image to white
    img[:] = [255, 255, 255]

    # Define categories
    categories = {
        'residential': 0.3,
        'commerce': 0.2,
        'industry': 0.3,
        'recreation': 0.2
    }

    # Instantiate TownGenerator and get buildings
    town = TownGenerator(1000, 100, categories)
    buildings = town.getBuildings()

    # Randomly assign positions and sizes safely
    for b in buildings:
        # Random size (optional: could be based on area)
        #size_x = random.randint(5, 20)
        #size_y = random.randint(5, 20)
        size_x = b.size_x
        size_y = b.size_y

        # Random position so building fits inside image
        b.x = random.randint(0, n_pixel_x - size_x - 1)
        b.y = random.randint(0, n_pixel_y - size_y - 1)
        b.display()
    # Connect nearest buildings first
    connect_nearest(buildings)

    # Draw buildings on top
    draw_buildings(buildings)

    # Save map
    cv2.imwrite("map.png", img)
    print(f"Map saved as 'map.png' with {len(buildings)} buildings.")
