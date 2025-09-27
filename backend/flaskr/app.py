from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)