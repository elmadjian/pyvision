import cv2, glob
import numpy as np

class CameraCalibration():
    def __init__(self, itr=30, eps=0.001):
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, itr, eps)
        self.obj_points = []
        self.img_points = []
        self.objp = np.zeros((7*9,3), dtype="float32")
        self.objp[:,:2] = np.mgrid[0:9, 0:7].T.reshape(-1,2)
        with np.load("cameraspecs.npz") as X:
            self.C    = X['mtx']
            self.dist = X['dist']


    def _get_corners(self):
        images = glob.glob("calibration_imgs/*.jpg")
        h, w = 0, 0

        for filename in images:
            img = cv2.imread(filename, 0)
            h, w = img.shape[:2]
            ret, corners = cv2.findChessboardCorners(img, (9,7))
            if ret:
                self.obj_points.append(self.objp)
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
        np.savez("cameraspecs", ret=ret, mtx=self.C, dist=self.dist,
                 rvecs=rvcs, tvecs=tvcs)



    def undistort(self, img, filename):
        h, w = img.shape[:2]
        C, roi = cv2.getOptimalNewCameraMatrix(self.C, self.dist, (w,h), 1)
        dst = cv2.undistort(img, self.C, self.dist, None, C)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite(filename, dst)


    def estimate_pose(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,7))
        axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
        if ret:
            refcorners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
                                                self.criteria)
            ret, rvcs, tvcs, inliers = cv2.solvePnPRansac(self.objp, refcorners,
                                                       self.C, self.dist)
            imgpts, jac = cv2.projectPoints(axis, rvcs, tvcs, self.C, self.dist)
            img = self._test_draw(img, refcorners, imgpts)
            cv2.imshow("test", img)
            cv2.waitKey(0)


    def _test_draw(self, img, corners, imgpts):
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 3)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 3)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 3)
        return img



if __name__=="__main__":
    cc = CameraCalibration()
    cc.calibrate()
    img = cv2.imread("calibration_imgs/camshot_4_undistorted.jpg")
    cc.estimate_pose(img)
    #cc.undistort(img, "calibration_imgs/camshot_3_undistorted.jpg")
