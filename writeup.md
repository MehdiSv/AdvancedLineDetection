**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistorted.jpg "Undistorted"
[image2]: ./output_images/thresholded.jpg "Thresholded"
[image3]: ./output_images/warped.jpg "Warped"
[image4]: ./output_images/polylines.jpg "Polylines"
[image5]: ./output_images/final.jpg "Final"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

#### 1. Camera Calibration and Image Undistortion

I used the provided 20 camera calibration images. I iterated on each of them, finding the chessboard corners and corresponding coordinates on the board using `cv2.findChessboardCorners()` in the `find_corners()` method of the [Undistorter](undistorter.py) class.

I stored all of these results in a single array that I passed to `cv2.calibrateCamera()` to calibrate to camera. I stored the resulting matrix and distortion coefficients for later use through the `undistort()` method of the [Undistorter](undistorter.py) class.

Example undistorted image:

![alt text][image1]

#### 2. Image Filtering

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at methods `dir_thresh`, `mag_thresh`,`color_thresh` in the [Thresholder](thresholder.py) class).

I first applied a color filtering, keeping only white or yellow-ish pixels of the image. I then only kept pixels that either match a sufficent magnitude or direction threshold.

Example filtered image:

![alt text][image2]

#### 3. Image Warping

I then warped the image to obtain a bird's-eye view of the road.

To do so, I used the `cv2.getPerspectiveTransform()` method (in `__init__()` of the [Warper](warper.py) class) with these source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 580, 460      | 260, 0        |
| 700, 460      | 1040, 0       |
| 1040, 680     | 1040, 720     |
| 260, 680      | 260, 720      |


![alt text][image3]

#### 4. Lane detection

I first computed the histogram of the picture on its lower half to find the rough position of each lane line (lines 58 through 62 of the [Polyfitter](polyfitter.py) class).

I then ran a sliding window vertically to detect the position of the center of each lane line on each part of the image (lines 64 through 97 of the [Polyfitter](polyfitter.py) class).

I then used these positions to compute polylines describing each lane line using the `np.polyfit()` method (lines 104 and 105 of the [Polyfitter](polyfitter.py) class)

![alt text][image4]

#### 5. Measuring lane curvature

I used the computed polyline along with the estimated lane width (~3.7m) to compute the real-world lane curvature.
I also measured the position of the car in respect to the lane by computing the difference between the center of the lane and the center of the image.

These computations can be found in the `measure_curvature()` method of the [Polyfitter](polyfitter.py) class

#### 6. Displaying the detected lane

I then created a polygon using the curves of each computed polyline and warped back the result using the reversed source and destination of step #3.

I finally drew this polygon on the undistorted image.

![alt text][image5]

---

### Pipeline (video)

Here's a [link to my video result](./project_video_done.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

The implementation overall went pretty smoothly.

It might fail in extreme lighting conditions or in countries with lanes line colors different than white and yellow, or if they are not well visually defined (worn out or missing).

I could make it more robust by handling more lightning conditions and lane line colors, and also by adding recovery options in case I dont detect any lane line, or if they differ too much from the previously detected lines.
