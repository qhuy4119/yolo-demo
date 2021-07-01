import os


def clean():
    dirs = [d for d in os.listdir() if os.path.isdir(d)]
    print("Dirs found: ", dirs)
    for d in dirs:
        for f in os.listdir(d):
            invalidImageFlag = f.endswith("jpg") and not os.path.isfile(
                os.path.join(d, f.rstrip("jpg") + "txt")
            )
            invalidTextFlag = f.endswith("txt") and not os.path.isfile(
                os.path.join(d, f.rstrip("txt") + "jpg")
            )
            if invalidImageFlag or invalidTextFlag:
                os.remove(os.path.join(d, f))


if __name__ == "__main__":
    clean()
