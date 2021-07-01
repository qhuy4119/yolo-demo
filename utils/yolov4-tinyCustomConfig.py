# create yolov4-tiny-obj.cfg
#### classes = classes in lines 220, 269
#### filters = (classes + 5)*3 in lines 212, 263

import subprocess
import os, shutil

def get_obj_data(classes):
    cwd = os.getcwd()
    backupPath = input("Enter path of backup dir: ")
    objectData = dict(
        classes=classes,
        train=os.path.join(cwd, "train.txt"),
        valid=os.path.join(cwd, "val.txt"),
        names=os.path.join(cwd, "obj.names"),
        backup=backupPath,
    )
    return objectData


def write_cfg_file(classes):
    commandAndArgs = ["sed", "-i"]
    filename = ["yolov4-tiny-obj.cfg"]
    expressions = [
        [r"/^max_batches/c\max_batches=%s" % (classes * 2000)],
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


def write_files(objectData, classes):
    with open("obj.data", "w") as f:
        for k, v in objectData.items():
            f.write("%s = %s\n" % (k, v))
    write_cfg_file(classes)


if __name__ == "__main__":
    classes = int(input("Enter number of classes: "))
    print("IN THE NEXT SECTION: ALL PATHS ARE RELATIVE TO THE DARKNET EXECUTABLE\n")
    objectData = get_obj_data(classes)
    write_files(objectData, classes)
    shutil.copyfile("classes.txt", "obj.names")
