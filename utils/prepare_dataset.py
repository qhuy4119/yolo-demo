import os, shutil, glob, sys
import csv
import numpy as np
from sklearn.model_selection import train_test_split
import argparse


def prepend_image_name(imageRootDir="."):
    imageDirs = [d for d in os.listdir(imageRootDir) if os.path.isdir(d)]
    print("Found %d image directory" % len(imageDirs))
    for imageDir in imageDirs:
        print("Entering %s directory" % imageDir)
        for file in os.listdir(imageDir):
            if file == "classes.txt":
                continue
            os.rename(
                os.path.join(imageRootDir, imageDir, file),
                os.path.join(imageRootDir, imageDir, "%s-%s" % (imageDir, file)),
            )


def write_csv_file(filename="images.csv"):
    def get_class_mapping(classFile="classes.txt"):
        classMapping = dict()
        with open(classFile, "r") as f:
            for labelID, labelName in enumerate(f):
                classMapping[labelName.strip("\n")] = labelID
        return classMapping

    with open(filename, mode="w") as f:
        f_writer = csv.writer(f)
        imageDirs = [d for d in os.listdir() if os.path.isdir(d)]
        classMapping = get_class_mapping()
        for imageDir in imageDirs:
            for file in os.listdir(imageDir):
                if file.endswith(".jpg") and os.path.isfile(
                    os.path.join(imageDir, file.rstrip(".jpg") + ".txt")
                ):
                    labelID = classMapping[imageDir]
                    f_writer.writerow(
                        [os.path.join("data", "custom-data", imageDir, file), labelID]
                    )
        print(
            "Write image paths and their corresponding labels to %s successfully "
            % os.path.join(os.getcwd(), filename)
        )


def split_dataset(dataFile="images.csv"):
    trainRatio = 0.75
    validationRatio = 0.15
    testRatio = 0.1
    df = np.loadtxt(dataFile, delimiter=",", dtype=object)
    X = df[:, 0]
    y = df[:, 1]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1 - trainRatio, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_test,
        y_test,
        test_size=testRatio / (testRatio + validationRatio),
        random_state=42,
    )
    np.savetxt("train.txt", X_train, fmt="%s")
    np.savetxt("val.txt", X_val, fmt="%s")
    np.savetxt("test.txt", X_test, fmt="%s")
    print(
        "Split data from %s into train.txt, val.txt, and test.txt successfully"
        % dataFile
    )
    print("Shape of train: ", X_train.shape)
    print("Shape of val: ", X_val.shape)
    print("Shape of test: ", X_test.shape)


def generate_dirs():
    for d in ["train", "val", "test"]:
        if os.path.isdir(d):
            print("Overwriting existing %s" % d)
            shutil.rmtree(d)
        else:
            print("Creating %s" % d)
        os.mkdir(d)
        print("Reading list of images from %s" % (d + ".txt"))
        with open(d + ".txt", "r") as f:
            for imageFilePath in f:
                globPattern = imageFilePath.strip(".jpg\n") + "*"
                for f in glob.glob(globPattern):
                    shutil.copy(f, d)


if __name__ == "__main__":
    print("Current working directory: ", os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate_dirs",
        action="store_true",
        help="Copy images specified in train.txt, val.txt, and test.txt into 3 directories: train, val, test ",
    )
    parser.add_argument(
        "--prepend",
        action="store_true",
        help="Use this flag to prepend image filenames",
    )
    args = parser.parse_args()
    if args.prepend:
        print("***Prepending image filenames***")
        prepend_image_name()
    if args.generate_dirs:
        print("Generating train, val, test directories")
        generate_dirs()
        sys.exit()
    print("***Writing csv file***")
    write_csv_file()
    print("***Splitting dataset***")
    split_dataset()
