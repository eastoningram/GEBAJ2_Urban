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
    population = data["population"]
    area = data["area"]
    print(population)
    print(area)

    img=create_map(int(population), float(area))
    filepath = os.path.join("static", "map.png")
    print(filepath)
    cv2.imwrite(filepath, img)
    
    
    return("OK")
    

if __name__ == "__main__":
    app.run(debug=True)
