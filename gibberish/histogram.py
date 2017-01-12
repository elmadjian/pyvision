import cv2, sys, file_handler
import numpy as np
import matplotlib.pyplot as plt

class Histogram():
    def __init__(self):
        self.img = file_handler.open_image(sys.argv)
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.histogram = None

    def standard_grayscale_histogram(self, N):
        h = [0 for i in range(N)]
        for row in self.gray_img:
            for intensity in row:
                h[intensity] += 1
        self.histogram = h
        return h

    def relative_f_grayscale_histogram(self, N):
        rows = self.gray_img.shape[0]
        cols = self.gray_img.shape[1]
        h = self.standard_grayscale_histogram(N)
        h = [i/(rows*cols) for i in h]
        self.histogram = h
        return h

    def equalized_grayscale_histogram(self, N):
        h = self.relative_f_grayscale_histogram(N)
        f = [0 for i in range(N)]
        sum = 0
        for i in range(N):
            sum += h[i]
            f[i] = round(sum * (N-1))
        self.histogram = f
        return f

    def plot_histogram(self):
        plt.plot(self.histogram)
        plt.ylabel("frequency")
        plt.show()


if __name__ == "__main__":
    h = Histogram()
    # h.standard_grayscale_histogram()
    # h.plot_histogram()
    # h.relative_f_grayscale_histogram()
    # h.plot_histogram()
    # h.equalized_grayscale_histogram(256)
    # h.plot_histogram()
