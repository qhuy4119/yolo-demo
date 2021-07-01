import subprocess
import os, shutil

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
        params["cfg"] = "data/custom-data/yolov4-obj.cfg"
        params["weights"] = "data/custom-data/yolov4-obj.weights"
    params["image"] = "../%s" % imagePath
    os.chdir("darknet")
    command = (
        DARKNET_EXECUTABLE
        + DARKNET_COMMAND
        + [params["data"], params["cfg"], params["weights"], params["image"]]
        + ["-dont_show"]
    )
    subprocess.run(command)
    shutil.copy("predictions.jpg", "../static/predictions.jpg")
    os.chdir("..")
    return
