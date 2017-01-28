import cv2, marker_detector, sys

def main():
    md = marker_detector.MarkerDetector()
    #video = cv2.VideoCapture(0)
    img = cv2.imread(sys.argv[1])
    img = md.detect(img)
    cv2.imshow("teste", img)
    cv2.waitKey(0)
    # while True:
    #     frame = video.read()[1]
    #     img = md.detect(frame)
    #     cv2.imshow("teste", img)
    #     cv2.waitKey(10)


if __name__=="__main__":
    main()
