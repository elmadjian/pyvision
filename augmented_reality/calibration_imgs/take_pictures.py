import cv2

def main():
    video = cv2.VideoCapture(0)
    num_pics = 15
    input("place the checkerboard in front of the camera and press a key to start")
    while num_pics > 0:
        frame = video.read()[1]
        cv2.imshow("shot", frame)
        key = cv2.waitKey(0)
        print("(%s pictures left) -- save the picture? [s/n]" % num_pics)
        if key & 0xFF == ord('s'):
            filename = "camshot_" + str(num_pics) + ".jpg"
            cv2.imwrite(filename, frame)
            num_pics -= 1
    print("15 pictures saved! bye...")

if __name__=="__main__":
    main()
