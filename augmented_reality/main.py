import cv2, marker_detector

def main():
    md = marker_detector.MarkerDetector()
    video = cv2.VideoCapture(0)
    while True:
        frame = video.read()[1]
        img = md.detect(frame)
        cv2.imshow("teste", img)
        cv2.waitKey(10)


if __name__=="__main__":
    main()
