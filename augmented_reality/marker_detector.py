import cv2, sys
import numpy as np

class MarkerDetector():

    def __init__(self, calibration=None):
        self.calibration = calibration

    def detect(self, img):
        preprocessed_img = self._preprocess(img)
        contour_list     = self._find_contours(preprocessed_img)
        possible_markers = self._find_candidates(contour_list, img)
        transformed_ones = self._transform_marker(possible_markers, img)
        
        return preprocessed_img

    def _preprocess(self, img):
        filtered_img = cv2.medianBlur(img, 5)
        gray_img = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray_img, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

    def _find_contours(self, img):
        contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1]
        contour_list = []
        for c in contours:
            if len(c) > 5:
                contour_list.append(c)
        return contour_list


    def _find_candidates(self, contour_list, img):
        possible_markers = []
        for c in contour_list:
            eps = cv2.arcLength(c, True) * 0.05
            approx = cv2.approxPolyDP(c, eps, True)
            if len(approx) != 4:
                continue
            if not cv2.isContourConvex(approx):
                continue
            if self._is_min_length(approx, 1000):
                continue
            v1 = (approx[1] - approx[0])[0]
            v2 = (approx[2] - approx[0])[0]
            lr = (v1[0] * v2[1]) - (v1[1] * v2[0])
            if lr < 0.0:
                approx[1], approx[3] = approx[3], approx[1]
            possible_markers.append(approx)
        return possible_markers


    def _is_min_length(self, approx, min_length):
        min_dist = sys.maxsize
        for i in range(4):
            points = approx[i] - approx[(i+1)%4]
            squared_length = np.dot(points, points.T)
            min_dist = min(min_dist, squared_length[0][0])
        if min_dist < min_length:
            return True
        return False


    def _transform_marker(self, candidates, img):
        markers = []
        for m in candidates:
            (m0, m1, m2, m3) = m
            m0, m1, m2, m3 = m0[0], m1[0], m2[0], m3[0]
            new_m = np.array([m0, m1, m2, m3], dtype="float32")
            side0 = np.sqrt((m0[0]-m1[0])**2 + (m0[1]-m1[1])**2)
            side1 = np.sqrt((m1[0]-m2[0])**2 + (m1[1]-m2[1])**2)
            side2 = np.sqrt((m2[0]-m3[0])**2 + (m2[1]-m3[1])**2)
            side3 = np.sqrt((m3[0]-m0[0])**2 + (m3[1]-m0[1])**2)
            side  = int(max(side0, side1, side2, side3))
            dst = np.array([
                [0,0],
                [side-1, 0],
                [side-1, side-1],
                [0, side-1]
            ], dtype="float32")
            M = cv2.getPerspectiveTransform(new_m, dst)
            warped = cv2.warpPerspective(img, M, (side, side))
            markers.append(warped)
        return markers
            # cv2.imshow("teste", warped)
            # cv2.waitKey(0)

                # temp = np.zeros(img.shape, dtype="uint8")
                # cv2.drawContours(temp, [approx], 0, (255,255,255), 2)
                # cv2.imshow("teste", temp)
                # cv2.waitKey(0)
