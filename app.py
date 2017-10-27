from flask import Flask, request, render_template
import random, time

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/process_dank", methods=["POST"])
def process_dank():
    image = request.files.get("dank","")
    image.save("static/images/"+image.filename)
    time.sleep(2)
    return "<img src='static/images/{}'>".format(image.filename)

# test
