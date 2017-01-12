import sys, cv2

def open_image(params):
    if len(params) == 1:
        filename = input("Please, type the image file name: ")
        return cv2.imread(filename)
    elif len(params) == 2:
        return cv2.imread(params[1])
    else:
        print("USAGE: <caller.py> <image_name>")
        sys.exit()
