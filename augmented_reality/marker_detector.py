import cv2
import numpy as np

class MarkerDetector():

    def __init__(self, calibration=None):
        self.calibration = calibration

    def detect(self, img):
        preprocessed_img = self._preprocess(img)
        contour_list     = self._find_contours(preprocessed_img)
        self._find_candidates(contour_list, img)
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
        # temp = np.zeros(img.shape, dtype="uint8")
        for c in contours:
            if len(c) > 5:
                contour_list.append(c)
                # cv2.drawContours(temp, [c], 0, (255, 255, 255), 2)
                # cv2.imshow("teste", temp)
                # cv2.waitKey(0)
        return contour_list


    def _find_candidates(self, contour_list, img):
        # temp = np.zeros(img.shape, dtype="uint8")
        for c in contour_list:
            eps = cv2.arcLength(c, True) * 0.05
            approx = cv2.approxPolyDP(c, eps, True)
            # print(len(approx))
            if len(approx) != 4:
                continue
            if not cv2.isContourConvex(approx):
                continue

                # cv2.drawContours(temp, [approx], 0, (255,255,255), 2)
                # cv2.imshow("teste", temp)
                # cv2.waitKey(0)
