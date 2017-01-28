import cv2, marker_detector, sys

def main():
    code = [0,1,0,0,0,1,1,1,1]
    md = marker_detector.MarkerDetector()
    video = cv2.VideoCapture(0)
    # img = cv2.imread(sys.argv[1])
    # img = md.detect(img, code)
    # cv2.imshow("teste", img)
    # cv2.waitKey(0)
    while True:
        frame = video.read()[1]
        img = md.detect(frame, code)
        cv2.imshow("teste", img)
        cv2.waitKey(10)


if __name__=="__main__":
    main()
