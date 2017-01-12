import cv2

class MarkerDetector():

    def __init__(self, calibration=None):
        self.calibration = calibration

    def detect(self, img):
        preprocessed_img = self._preprocess(img)
        return preprocessed_img

    def _preprocess(self, img):
        filtered_img = cv2.medianBlur(img, 5)
        gray_img = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        return  cv2.adaptiveThreshold(gray_img, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 7, 7)

    def _find_contours(self, img):
        contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1]
        #for c in contours:



    def _find_markers(self):
        pass
