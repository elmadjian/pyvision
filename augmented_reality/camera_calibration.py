import cv2, glob
import numpy as np

class CameraCalibration():
    def __init__(self, itr=30, eps=0.001):
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, itr, eps)

    def calibrate(self):
        objp = np.zeros((7*9,3), dtype="float32")
        objp[:,:2] = np.mgrid[0:9, 0:7].T.reshape(-1,2)
        images = glob.glob("calibration_imgs/*.jpg")
        #for img in images:
