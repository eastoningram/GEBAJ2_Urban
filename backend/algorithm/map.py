import os
import math
import random
import numpy as np
import cv2

# Try both relative and non-relative import so module works both run-as-script and imported
try:
    from .generator import TownGenerator
except Exception:
    from generator import TownGenerator


class Building:
    def __init__(self, x: int, y: int, size_x: int, size_y: int, category: str):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.category = category

    def center(self):
        return (self.x + self.size_x // 2, self.y + self.size_y // 2)

    def edges(self):
        return {
            "left": self.x,
            "right": self.x + self.size_x,
            "top": self.y,
            "bottom": self.y + self.size_y,
        }


# category → BGR color for cv2
CATEGORY_COLORS = {
    "residential": (0, 200, 0),
    "commerce": (0, 0, 200),
    "industry": (200, 0, 0),
    "recreation": (128, 128, 128),
    "L": (0, 0, 0),
}


# ---------- helper drawing functions ----------
def draw_rect(img, b: Building):
    color = CATEGORY_COLORS.get(b.category, (0, 0, 0))
    x1, y1 = b.x, b.y
    x2, y2 = b.x + b.size_x, b.y + b.size_y
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=-1)


def draw_L_shape(img, shape_grid, start_x, start_y, block_size, color):
    for r in range(len(shape_grid)):
        for c in range(len(shape_grid[0])):
            if shape_grid[r][c] == 1:
                x1 = start_x + c * block_size
                y1 = start_y + r * block_size
                x2 = x1 + block_size
                y2 = y1 + block_size
                cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)


L_BUILDING = [
    [1, 0],
    [1, 0],
    [1, 1],
]


def draw_road_segment(img, p1, p2, road_width):
    """Draw Manhattan L-shaped road between p1 and p2 with thickness=road_width (in pixels)."""
    x1, y1 = p1
    x2, y2 = p2
    road_color = (50, 50, 50)

    # horizontal then vertical
    x_start, x_end = min(x1, x2), max(x1, x2)
    y_start, y_end = min(y1, y2), max(y1, y2)

    # horizontal strip centered at y1
    y0 = y1
    y0a = max(0, y0 - road_width // 2)
    y0b = min(img.shape[0], y0 + road_width // 2 + 1)
    img[y0a:y0b, x_start:x_end + 1] = road_color

    # vertical strip centered at x2
    x0 = x2
    x0a = max(0, x0 - road_width // 2)
    x0b = min(img.shape[1], x0 + road_width // 2 + 1)
    img[y_start:y_end + 1, x0a:x0b] = road_color


def edge_connect(b1: Building, b2: Building):
    e1 = b1.edges()
    e2 = b2.edges()
    c1 = b1.center()
    c2 = b2.center()

    # decide whether mostly horizontal or vertical
    if abs(c1[0] - c2[0]) >= abs(c1[1] - c2[1]):
        # horizontal main leg
        if c1[0] < c2[0]:
            start = (e1["right"], c1[1])
            end = (e2["left"], c2[1])
        else:
            start = (e1["left"], c1[1])
            end = (e2["right"], c2[1])
    else:
        # vertical main leg
        if c1[1] < c2[1]:
            start = (c1[0], e1["bottom"])
            end = (c2[0], e2["top"])
        else:
            start = (c1[0], e1["top"])
            end = (c2[0], e2["bottom"])
    return start, end


def connect_nearest_and_draw(img, buildings, road_width):
    for i, b in enumerate(buildings):
        nearest = None
        nearest_dist = float("inf")
        c1 = b.center()
        for j, other in enumerate(buildings):
            if i == j:
                continue
            c2 = other.center()
            dist = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = other
        if nearest:
            p1, p2 = edge_connect(b, nearest)
            draw_road_segment(img, p1, p2, road_width)


# ---------- main generator function ----------
def generate_map(population: int, area: float, output_path: str = "static/map.png", categories: dict = None):
    """
    Generate a map image and write it to output_path.
    - population: integer
    - area: sq km (float)
    - categories: optional category distribution dict (keys: residential, commerce, industry, recreation).
    """

    if categories is None:
        categories = {"residential": 0.5, "commerce": 0.2, "industry": 0.2, "recreation": 0.1}

    # 1) compute buildings via your TownGenerator
    town = TownGenerator(population, area, categories)
    result = town.calculate_buildings()
    category_counts = result.get("category_buildings", {})

    # 2) choose image size scaled to area (but keep reasonable min/max)
    scale = math.sqrt(max(0.1, area))  # sqrt to avoid huge growth
    height = max(200, int(300 * scale))
    width = max(300, int(400 * scale))

    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # 3) road width and spacing scale based on map size
    road_width = max(2, int(min(width, height) * 0.015))
    spacing = max(40, int(min(width, height) * 0.12))

    # optional: draw a light grid of roads first (this makes connectivity easier)
    for x in range(0, width, spacing):
        cv2.line(img, (x, 0), (x, height), (50, 50, 50), road_width)
    for y in range(0, height, spacing):
        cv2.line(img, (0, y), (width, y), (50, 50, 50), road_width)

    # 4) compute scaled building sizes per category:
    # take average building footprint as percent of spacing
    avg_building_size = int(min(spacing * 0.6, min(width, height) * 0.08))
    size_variation = max(3, int(avg_building_size * 0.4))

    # 5) place buildings with spacing checks
    buildings = []
    rng = random.Random(12345)  # deterministic during dev; change seed or remove for randomness

    spacing_margin = max(6, int(min(width, height) * 0.02))

    for cat in ["residential", "commerce", "industry", "recreation"]:
        count = int(category_counts.get(cat, 0))
        for _ in range(count):
            placed = False
            attempts = 0
            while not placed and attempts < 200:
                w = rng.randint(max(6, avg_building_size - size_variation), avg_building_size + size_variation)
                h = rng.randint(max(6, avg_building_size - size_variation), avg_building_size + size_variation)

                x = rng.randint(0, width - w - 1)
                y = rng.randint(0, height - h - 1)

                # check spacing from other buildings
                ok = True
                for b in buildings:
                    if abs(b.x - x) < (w + b.size_x) // 2 + spacing_margin and abs(b.y - y) < (h + b.size_y) // 2 + spacing_margin:
                        ok = False
                        break
                if ok:
                    buildings.append(Building(x, y, w, h, cat))
                    placed = True
                attempts += 1
            # if attempts exhausted we skip (keeps generator robust)

    # 6) Draw roads connecting nearest neighbors but *after* grid roads:
    # Connect centers using edge-aware segments that stop at building edges
    connect_nearest_and_draw(img, buildings, road_width=road_width)

    # 7) Draw buildings on top (so they mask roads at edges)
    for b in buildings:
        if b.category == "L":
            draw_L_shape(img, L_BUILDING, b.x, b.y, block_size=max(6, int(avg_building_size/3)), color=CATEGORY_COLORS["L"])
        else:
            draw_rect(img, b)

    # 8) ensure directory exists and save
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    cv2.imwrite(output_path, img)
    return output_path


# Allow running the map generator from CLI for quick testing
if __name__ == "__main__":
    p = int(input("Population: "))
    a = float(input("Area (sq km): "))
    print("Generating into static/map.png ...")
    generate_map(p, a, output_path="static/map.png")
    print("Done.")
