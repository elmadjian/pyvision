import cv2
import numpy as np

class NftDetector():

    def __init__(self, nfeatures, calibration=None, min_match_count=10):
        self.orb = None
        self.marker_img = None
        self.key_points = None
        self.descriptor = None
        self.pts2d = None
        self.pts3d = None
        self.calibration = calibration
        self.mmc = min_match_count
        self.nfeatures  = nfeatures


    def set_marker(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.marker_img = img
        self.orb = cv2.ORB_create(nfeatures=self.nfeatures)
        self.key_points, self.descriptor = self.orb.detectAndCompute(img, None)
        print("NFT: found " + str(len(self.key_points)) + " key points")
        h,w = img.shape
        max_size = max(h,w)
        uh, uw = h/max_size, w/max_size
        self.pts2d = np.float32([[0,0], [w,0], [w,h], [0,h]]).reshape(-1,1,2)
        self.pts3d = np.float32([[-uw,-uh, 0.0],
                                 [ uw,-uh, 0.0],
                                 [ uw, uh, 0.0],
                                 [-uw, uh, 0.0]])


    def show_key_points(self):
        mkr = self.marker_img
        img = cv2.drawKeypoints(mkr, self.key_points, None, (0,0,255), flags=0)
        cv2.imshow("NFT", img)
        cv2.waitKey(0)


    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, des = self.orb.detectAndCompute(gray, None)
        matches = self._get_matches(des)
        if matches is not None:
            corners = self._find_transform(matches, gray, kp)
            if corners is not None:
                return self._estimate_pose(corners)
        return None, None


    def _get_matches(self, des):
        if des is not None:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(self.descriptor, des)
            good = []
            for m in matches:
                if m.distance < 60.0:
                    good.append(m)
            return good


    def _find_homography(self, matches, kp):
        M, matchesMask = None, None
        if len(matches) > self.mmc:
            src_pts = np.float32([self.key_points[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
            dst_pts = np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
        return M, matchesMask


    def _find_transform(self, matches, img, kp):
        M, matchesMask = self._find_homography(matches, kp)
        if M is not None:
            shape = (self.marker_img.shape[1], self.marker_img.shape[0])
            warped_img = cv2.warpPerspective(img, M, shape, flags=cv2.WARP_INVERSE_MAP)
            kp2, des2 = self.orb.detectAndCompute(warped_img, None)
            refined_matches = self._get_matches(des2)
            if refined_matches is not None:
                M2, matchesMask = self._find_homography(refined_matches, kp2)
                if M2 is not None:
                    homography = np.dot(M, M2)
                    dst = cv2.perspectiveTransform(self.pts2d, homography)
                    tmp = cv2.polylines(self.marker_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                    return np.float32(dst)


    def _estimate_pose(self, corners):
        crit = self.calibration.criteria
        C    = self.calibration.C
        dist = self.calibration.dist
        ncorn = cv2.cornerSubPix(self.marker_img, corners, (11,11), (-1,-1), crit)
        ret, rvcs, tvcs, inliers = cv2.solvePnPRansac(self.pts3d, ncorn, C, dist)
        return rvcs, tvcs
