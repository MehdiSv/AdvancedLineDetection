import cv2
import matplotlib.pyplot as plt
import numpy as np


class Thresholder:
    def __init__(self):
        sobel_kernel = 15
        dir_thresh = (0.7, 1.2)
        mag_thresh = (50, 255)
        self.sobel_kernel = sobel_kernel
        self.thresh_dir_min = dir_thresh[0]
        self.thresh_dir_max = dir_thresh[1]
        self.thresh_mag_min = mag_thresh[0]
        self.thresh_mag_max = mag_thresh[1]

    def abs_sobel_thresh(self, sobel, thresh_min=0, thresh_max=255):
        # Apply the following steps to img
        # 3) Take the absolute value of the derivative or gradient
        abs_sobel = np.absolute(sobel)
        # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
        scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))
        # 5) Create a mask of 1's where the scaled gradient magnitude
        # is > thresh_min and < thresh_max
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
        # 6) Return this mask as your binary_output image
        return sxbinary

    def dir_thresh(self, sobelx, sobely):
        abs_sobelx = np.abs(sobelx)
        abs_sobely = np.abs(sobely)
        # 4) Use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the gradient
        scaled_sobel = np.arctan2(abs_sobely, abs_sobelx)
        # 5) Create a binary mask where direction thresholds are met
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= self.thresh_dir_min) & (scaled_sobel <= self.thresh_dir_max)] = 1

        return sxbinary

    def mag_thresh(self, sobelx, sobely):
        # Calculate the gradient magnitude
        gradmag = np.sqrt(sobelx ** 2 + sobely ** 2)
        # Rescale to 8 bit
        scale_factor = np.max(gradmag) / 255
        gradmag = (gradmag / scale_factor).astype(np.uint8)
        # Create a binary image of ones where threshold is met, zeros otherwise
        binary_output = np.zeros_like(gradmag)
        binary_output[(gradmag >= self.thresh_mag_min) & (gradmag <= self.thresh_mag_max)] = 1

        return binary_output

    def color_thresh(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        yellow_min = np.array([15, 100, 120], np.uint8)
        yellow_max = np.array([80, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(img, yellow_min, yellow_max)

        white_min = np.array([0, 0, 200], np.uint8)
        white_max = np.array([255, 30, 255], np.uint8)
        white_mask = cv2.inRange(img, white_min, white_max)

        binary_output = np.zeros_like(img[:, :, 0])
        binary_output[((yellow_mask != 0) | (white_mask != 0))] = 1

        filtered = img
        filtered[((yellow_mask == 0) & (white_mask == 0))] = 0

        # print('Color filter')
        # plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_HSV2RGB))
        # plt.show()

        return binary_output

    def threshold(self, img):
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        sobelx = cv2.Sobel(img[:, :, 2], cv2.CV_64F, 1, 0, ksize=self.sobel_kernel)
        sobely = cv2.Sobel(img[:, :, 2], cv2.CV_64F, 0, 1, ksize=self.sobel_kernel)

        direc = self.dir_thresh(sobelx, sobely)
        # print('Direction threshold')
        # plt.imshow(direc, cmap='gray')
        # plt.show()
        mag = self.mag_thresh(sobelx, sobely)
        # print('Magnitude threshold')
        # plt.imshow(mag, cmap='gray')
        # plt.show()
        color = self.color_thresh(img)
        # print('Color threshold')
        # plt.imshow(color, cmap='gray')
        # plt.show()

        combined = np.zeros_like(direc)
        combined[((color == 1) & ((mag == 1) | (direc == 1)))] = 1

        return combined
