from flask import Flask, render_template, request, jsonify, url_for
import os

# import the map generator function from algorithm.map
from algorithm.map import generate_map

app = Flask(__name__, static_folder="static", template_folder="templates")


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
    data = request.get_json() or {}
    try:
        population = int(data.get("population", 0))
        area = float(data.get("area", 0))
    except Exception as e:
        return jsonify({"error": "Invalid input", "message": str(e)}), 400

    if population <= 0 or area <= 0:
        return jsonify({"error": "Population and area must be > 0"}), 400

    # where the map will be written
    out_path = os.path.join(app.static_folder, "map.png")

    # call the map generator -- it writes the file
    try:
        generate_map(population=population, area=area, output_path=out_path)
    except Exception as e:
        # helpful debug info returned to client
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500

    # return the static URL for the frontend to load
    return jsonify({"map_url": url_for("static", filename="map.png")})
    

if __name__ == "__main__":
    # run from project root
    app.run(debug=True)
