import cv2
import numpy as np

class NftDetector():

    def __init__(self, features, min_match_count=10):
        self.orb = None
        self.marker_img = None
        self.key_points = None
        self.descriptor = None
        self.mmc = min_match_count
        self.features = features


    def set_marker(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.marker_img = img
        self.orb = cv2.ORB_create(nfeatures=self.features)
        self.key_points, self.descriptor = self.orb.detectAndCompute(img, None)
        print("NFT: found " + str(len(self.key_points)) + " key points")


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
            matchesMask = self._find_transform(matches, gray, kp)


    def _get_matches(self, des):
        if des is not None:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(self.descriptor, des)
            good = []
            for m in matches:
                if m.distance < 60.0:
                    good.append(m)
            return good
        return None


    def _find_homography(self, matches, kp):
        M, matchesMask = None, None
        if len(matches) > self.mmc:
            src_pts = np.float32([self.key_points[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
            dst_pts = np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
            matchesMask = mask.ravel().tolist()
        else:
            print("Sorry, not enough matches found")
        return M, matchesMask


    def _find_transform(self, matches, img, kp):
        M, matchesMask = self._find_homography(matches, kp)
        shape = (self.marker_img.shape[1], self.marker_img.shape[0])
        warped_img = cv2.warpPerspective(img, M, shape, flags=cv2.WARP_INVERSE_MAP)
        kp2, des2 = self.orb.detectAndCompute(warped_img, None)
        refined_matches = self._get_matches(des2)
        if refined_matches is not None:
            M2, matchesMask = self._find_homography(refined_matches, kp2)
            if M2 is not None:
                homography = np.dot(M, M2)
                h,w = self.marker_img.shape
                pts = np.float32([[0,0], [0,h-1], [w-1,h-1], [w-1,0]]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts, homography)
                tmp = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                cv2.imshow("ha", tmp)
                cv2.waitKey(10)
