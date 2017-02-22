import cv2, marker_detector, sys, camera_calibration, renderer

def main():
    code = [0,1,0,0,0,1,1,1,1]
    calibration = camera_calibration.CameraCalibration()
    md = marker_detector.MarkerDetector(calibration)
    video = cv2.VideoCapture(0)
    # img = cv2.imread(sys.argv[1])
    # img = md.detect(img, code)
    # cv2.imshow("teste", img)
    # cv2.waitKey(0)
    rd = renderer.Renderer()
    rd.start()
    while True:
        frame = video.read()[1]
        rvecs, tvecs = md.detect(frame, code)
        rd.image = frame
        rd.rvecs = rvecs
        rd.tvecs = tvecs
        # print(rvecs, tvecs)
        # cv2.imshow("teste", frame)
        # cv2.waitKey(10)


if __name__=="__main__":
    main()
