import cv2, sys, file_handler
import numpy as np

class LinearFilter():
    def __init__(self):
        self.img = file_handler.open_image(sys.argv)
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.filtered_img = None

    def average_filter(self, kernel):
        bound = int((kernel-1)/2)
        img = self.gray_img.copy()
        img = np.pad(img, bound, 'constant', constant_values=0)
        self.filtered_img = img.copy()
        den = kernel*kernel
        self.show_img()
        for i in range(bound, img.shape[0]-bound):
            for j in range(bound, img.shape[1]-bound):
                self.filtered_img[i][j] = round(self._average_conv(img, i, j, bound)/den)
        return self.filtered_img

    def _average_conv(self, img, i, j, bound):
        sum = 0
        for m in range(i-bound, i+bound):
            for n in range(j-bound, j+bound):
                sum += img[m][n]
        return sum

    def show_img(self):
        cv2.imshow("testing", self.filtered_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    g = LinearFilter()
    g.average_filter(5)
    g.show_img()
