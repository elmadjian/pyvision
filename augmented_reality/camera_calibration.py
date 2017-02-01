import cv2, glob
import numpy as np

class CameraCalibration():
    def __init__(self, itr=30, eps=0.001):
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, itr, eps)
        self.obj_points = []
        self.img_points = []
        self.C = None
        self.dist = None


    def _get_corners(self):
        objp = np.zeros((7*9,3), dtype="float32")
        objp[:,:2] = np.mgrid[0:9, 0:7].T.reshape(-1,2)
        images = glob.glob("calibration_imgs/*.jpg")
        h, w = 0, 0

        for filename in images:
            img = cv2.imread(filename, 0)
            h, w = img.shape[:2]
            ret, corners = cv2.findChessboardCorners(img, (9,7))
            if ret:
                self.obj_points.append(objp)
                ref_corners = cv2.cornerSubPix(img, corners, (11,11), (-1,-1),
                                               self.criteria)
                self.img_points.append(ref_corners)
                img = cv2.drawChessboardCorners(img, (9,7), ref_corners, ret)
        return w, h


    def calibrate(self):
        w, h = self._get_corners()
        ret, self.C, self.dist, rvcs, tvcs = cv2.calibrateCamera(self.obj_points,
                                        self.img_points, (w,h), None, None)
        print("\nRMS:", ret)
        print("camera matrix:\n", self.C)
        print("distortion coefficients: ", self.dist.ravel())



    def undistort(self, img, filename):
        h, w = img.shape[:2]
        C, roi = cv2.getOptimalNewCameraMatrix(self.C, self.dist, (w,h), 1)
        dst = cv2.undistort(img, self.C, self.dist, None, C)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite(filename, dst)



if __name__=="__main__":
    cc = CameraCalibration()
    cc.calibrate()
    img = cv2.imread("calibration_imgs/camshot_4.jpg")
    cc.undistort(img, "calibration_imgs/camshot_4_undistorted.jpg")
