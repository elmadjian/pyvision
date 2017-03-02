import cv2
import marker_detector
import nft_detector
import sys
import camera_calibration
import renderer
import streamer
import numpy as np

already_found  = False
initial_matrix = []

def main():
    code = [0,1,0,0,0,1,1,1,1]
    calibration = camera_calibration.CameraCalibration()
    #md = marker_detector.MarkerDetector(calibration)
    nft = nft_detector.NftDetector(1000)
    nft.set_marker(cv2.imread("stones.jpg"))
    nft.show_key_points()
    video = cv2.VideoCapture(1)
    # pusher = streamer.Streamer()

    # #rd = renderer.Renderer()
    # #rd.start()
    # counter = 0 #Kalman filter McGyver
    while True:
       frame = video.read()[1]
       nft.detect(frame)
    #     rvecs, tvecs = md.detect(frame, code)
    #     img = cv2.imencode(".jpg", frame)[1]
    #     pusher.send_image(img)
    #     #rd.image = frame
    #
    #     if rvecs is not None:
    #         matrix4 = create_transf_matrix_obj(rvecs, tvecs)
    #         pusher.send_matrix("yes", matrix4)
    #         counter = 12
    #     else:
    #         counter -= 1
    #         if counter < 0:
    #             counter = 0
    #             pusher.send_matrix("no", [])
    #
    #         #rd.rvecs = rvecs
    #         #rd.tvecs = tvecs
    #     # print(rvecs, tvecs)
    #     # cv2.imshow("teste", frame)
    #     #cv2.waitKey(10)

def create_transf_matrix_obj(rvecs, tvecs):
    global initial_matrix
    global already_found
    rmtx = cv2.Rodrigues(rvecs)[0]
    vmtx = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0]],
                     [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1][0]],
                     [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2][0]],
                     [0.0       ,0.0       ,0.0       ,1.0    ]])
    inverse_mtx = np.array([[ 1.0, 1.0, 1.0, 1.0],
                            [-1.0,-1.0,-1.0,-1.0],
                            [-1.0,-1.0,-1.0,-1.0],
                            [ 1.0, 1.0, 1.0, 1.0]])
    nmtx = vmtx * inverse_mtx
    if not already_found:
        initial_matrix = nmtx.copy()
        already_found = True

    #print("x:", nmtx[0,3], "y:", nmtx[1,3], "z:", nmtx[2,3])

    matrix4 = {}
    matrix4[11] = nmtx[0][0]
    matrix4[12] = nmtx[0][1]
    matrix4[13] = nmtx[0][2]
    matrix4[14] = nmtx[0][3]
    matrix4[21] = nmtx[1][0]
    matrix4[22] = nmtx[1][1]
    matrix4[23] = nmtx[1][2]
    matrix4[24] = nmtx[1][3]
    matrix4[31] = nmtx[2][0]
    matrix4[32] = nmtx[2][1]
    matrix4[33] = nmtx[2][2]
    matrix4[34] = nmtx[2][3]
    matrix4[41] = nmtx[3][0]
    matrix4[42] = nmtx[3][1]
    matrix4[43] = nmtx[3][2]
    matrix4[44] = nmtx[3][3]
    return matrix4


if __name__=="__main__":
    main()
