import glob

import cv2
import numpy as np


class Undistorter:
    def __init__(self):
        try:
            self.objpoints = np.load('data/objpoints.npy')
            self.imgpoints = np.load('data/imgpoints.npy')
            self.shape = tuple(np.load('data/shape.npy'))
        except:
            self.objpoints = None
            self.imgpoints = None
            self.shape = None

        if self.objpoints is None or self.imgpoints is None or self.shape is None:
            self.find_corners()

        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,
                                                                               self.shape,
                                                                               None, None)

    def find_corners(self):
        images = glob.glob('camera_cal/calibration*.jpg')
        base_objp = np.zeros((6 * 9, 3), np.float32)
        base_objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
        self.objpoints = []
        self.imgpoints = []
        self.shape = None

        for imname in images:
            img = cv2.imread(imname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if self.shape is None:
                self.shape = gray.shape[::-1]

            print('Finding chessboard corners on {}'.format(imname))
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            if ret:
                self.objpoints.append(base_objp)
                self.imgpoints.append(corners)

        np.save('data/objpoints', self.objpoints)
        np.save('data/imgpoints', self.imgpoints)
        np.save('data/shape', self.shape)

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
