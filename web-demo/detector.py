import subprocess
import os, shutil, glob
import json

DARKNET_EXECUTABLE = ["darknet"]
DARKNET_COMMAND = "detector test".split()


def predict(imagePath, model="original"):
    params = {}
    if model == "original":
        params["data"] = "cfg/coco.data"
        params["cfg"] = "cfg/yolov4-tiny.cfg"
        params["weights"] = "yolov4-tiny.weights"
    elif model == "custom":
        params["data"] = "data/custom-data/obj.data"
        params["cfg"] = "data/custom-data/yolov4-tiny-obj.cfg"
        params["weights"] = "data/custom-data/yolov4-tiny-obj_best.weights"
    params["image"] = "../%s" % imagePath
    os.chdir("darknet")
    command = (
        DARKNET_EXECUTABLE
        + DARKNET_COMMAND
        + [params["data"], params["cfg"], params["weights"], params["image"]]
        + "-dont_show -out predictions.json".split()
    )
    subprocess.run(command)
    for f in glob.glob("predictions*"):
        shutil.copy(f, "../static/")
    with open("predictions.json", "r") as f:
        data = json.load(f)
        objects = data[0]["objects"]
    os.chdir("..")
    return objects
