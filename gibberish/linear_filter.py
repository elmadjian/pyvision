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
        for i in range(bound, img.shape[0]-bound):
            for j in range(bound, img.shape[1]-bound):
                square = img[i-bound:i+bound, j-bound:j+bound]
                self.filtered_img[i][j] = round(square.mean())
        return self.filtered_img

    def show_img(self):
        cv2.imshow("testing", self.filtered_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    g = LinearFilter()
    g.average_filter(3)
    g.show_img()
