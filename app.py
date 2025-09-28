#!/usr/bin/env python3
from flask import Flask, render_template, request
import os
import cv2

from map import create_map

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "A simple urban planning website, made for HackUMBC 2025!"

@app.route('/team')
def team():
    return "Alex, Griffin, Easton, Ben, Josh^2."

@app.route("/generateCity", methods=["POST"])
def generateCity():
    data = request.get_json()
    population = int(data["population"])
    area = float(data["area"])

    print("generateCity called with:", population, area)

    img = create_map(population, area)

    # Save into Flask static folder (use app.static_folder to be safe)
    filepath = os.path.join(app.static_folder, "map.png")
    abspath = os.path.abspath(filepath)
    print("Attempting to write to:", filepath, "abs:", abspath, "app.static_folder:", app.static_folder)

    ok = cv2.imwrite(filepath, img)
    print("cv2.imwrite returned:", ok)

    if os.path.exists(abspath):
        print("Saved file size (bytes):", os.path.getsize(abspath))
        print("Saved file mtime:", os.path.getmtime(abspath))
    else:
        print("File NOT found after write!")

    return "OK"



    

if __name__ == "__main__":
    app.run(debug=True)
