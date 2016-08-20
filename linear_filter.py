import cv2, sys, file_handler
import numpy as np

class LinearFilter():
    def __init__(self):
        self.img = file_handler.open_image(sys.argv)
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def average_filter(self, kernel):
        img = self.gray_img.copy()
        h_zeros = np.zeros(img.shape[1], dtype="uint8")
        v_zeros = np.zeros(img.shape[0], dtype="uint8").reshape((img.shape[0],1))
        img = np.vstack((h_zeros, img))
        img = np.vstack((img, h_zeros))
        img = np.hstack((v_zeros, img))
        img = np.hstack((img, v_zeros))
