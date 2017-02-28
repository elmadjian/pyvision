import cv2
import numpy as np

class NftDetector():

    def __init__(self, thresh):
        self.surf = None
        self.marker_img = None
        self.key_points = None
        self.descriptor = None
        self.threshold  = thresh


    def set_marker(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.marker_img = img
        self.surf = cv2.xfeatures2d.SURF_create(self.threshold)
        self.key_points, self.descriptor = self.surf.detectAndCompute(img, None)
        print("NFT: found " + str(len(self.key_points)) + "key points")


    def show_key_points(self):
        mkr = self.marker_img
        img = cv2.drawKeypoints(mkr, self.key_points, None, (0,0,255), 4)
        cv2.imshow("NFT", img)
        cv2.waitKey(0)


    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        surf = cv2.xfeatures2d.SURF_create(self.threshold)
        kp, des = surf.detectAndCompute(gray, None)
        if des is not None:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(self.descriptor, des, k=2)
            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append([m])
            img2 = gray.copy()
            img2 = cv2.drawMatchesKnn(self.marker_img, self.key_points, gray, kp, good, img2, flags=2)
            cv2.imshow("NFT", img2)
            cv2.waitKey(0)
