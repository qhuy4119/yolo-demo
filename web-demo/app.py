from flask import Flask
from flask import render_template, request
from .detector import predict

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    uploaded_img = request.files["uploaded-img"]
    imgSavePath = "static/user-uploaded-img.jpg"
    uploaded_img.save(imgSavePath)
    if request.form["choose-model"] == "original-model":
        print("Using original yolo")
        objects = predict(imgSavePath, "original")
    elif request.form["choose-model"] == "custom-model":
        print("Using custom yolo")
        objects = predict(imgSavePath, "custom")
    numObjects = len(objects)
    listObjects = [(obj["name"], round(obj["confidence"]*100, 2)) for obj in objects]
    return render_template("detect.html", numObjects=numObjects, listObjects=listObjects)

@app.route("/models_info")
def models_info():
    return render_template("models_info.html")
