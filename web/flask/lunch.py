from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World"

@app.route("/하늘과 바다/")
def sky_sea():
    collections = ["하늘.jpg", "바다.jpg"]
    pick = random.choice(collections)
    return render_template('index.html', want_img = pick)



if __name__== "__main__":
    app.run(debug=True)