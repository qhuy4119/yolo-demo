# create yolov4-tiny-obj.cfg
#### classes = classes in lines 220, 269
#### filters = (classes + 5)*3 in lines 212, 263

import subprocess
import os, shutil


def get_obj_data(classes):
    backupPath = input("Enter path of backup dir: ")
    objectData = dict(
        classes=classes,
        train="data/custom-data/train.txt",
        valid="data/custom-data/val.txt",
        names="data/custom-data/obj.names",
        backup=backupPath,
    )
    return objectData


def write_cfg_file(classes, batch, subdivisions, width, height):
    commandAndArgs = ["sed", "-i"]
    filename = ["yolov4-tiny-obj.cfg"]
    expressions = [
        [r"/^batch=/c\batch=%s" % batch],
        [r"/^subdivisions/c\subdivisions=%s" % subdivisions],
        [r"/^width/c\width=%s" % width],
        [r"/^height/c\height=%s" % height],
        [r"/^max_batches/c\max_batches=%s" % max(6000, (classes * 2000))],
        [
            r"/^steps/c\steps=%s,%s"
            % (int(classes * 2000 * 80 / 100), int(classes * 2000 * 90 / 100))
        ],
        [r"220c classes=%s" % classes],
        [r"269c classes=%s" % classes],
        [r"212c filters=%s" % ((classes + 5) * 3)],
        [r"263c filters=%s" % ((classes + 5) * 3)],
    ]
    for e in expressions:
        subprocess.run(commandAndArgs + e + filename)


def write_files(objectData, classes, batch, subdivisions, width, height):
    with open("obj.data", "w") as f:
        for k, v in objectData.items():
            f.write("%s = %s\n" % (k, v))
    write_cfg_file(classes, batch, subdivisions, width, height)


if __name__ == "__main__":
    classes = int(input("Enter number of classes: "))
    batch = int(input("Enter batch number (default is 64) : "))
    subdivisions = int(input("Enter subdivisions (default is 1): "))
    width = int(input("Enter network image width (default is 416): "))
    height = int(input("Enter network image height (default is 416): "))
    print("IN THE NEXT SECTION: ALL PATHS ARE RELATIVE TO THE DARKNET EXECUTABLE\n")
    objectData = get_obj_data(classes)
    write_files(objectData, classes, batch, subdivisions, width, height)
    shutil.copyfile("classes.txt", "obj.names")
