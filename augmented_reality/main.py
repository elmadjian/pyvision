import cv2
import marker_detector
import sys
import camera_calibration
import renderer
import streamer

def main():
    code = [0,1,0,0,0,1,1,1,1]
    calibration = camera_calibration.CameraCalibration()
    md = marker_detector.MarkerDetector(calibration)
    video = cv2.VideoCapture(0)
    pusher = streamer.Streamer()
    # img = cv2.imread(sys.argv[1])
    # img = md.detect(img, code)
    # cv2.imshow("teste", img)
    # cv2.waitKey(0)
    #rd = renderer.Renderer()
    #rd.start()
    while True:
        frame = video.read()[1]
        rvecs, tvecs = md.detect(frame, code)
        img = cv2.imencode(".jpg", frame)[1]
        pusher.send_image(img)
        #rd.image = frame
        #rd.rvecs = rvecs
        #rd.tvecs = tvecs
        # print(rvecs, tvecs)
        # cv2.imshow("teste", frame)
        # cv2.waitKey(10)


if __name__=="__main__":
    main()
