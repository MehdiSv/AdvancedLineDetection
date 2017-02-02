import cv2
from matplotlib import pyplot as plt
from moviepy.video.io.VideoFileClip import VideoFileClip
from scipy import misc

from polydrawer import Polydrawer
from polyfitter import Polyfitter
from thresholder import Thresholder
from undistorter import Undistorter
from warper import Warper

undistorter = Undistorter()
thresholder = Thresholder()
warper = Warper()
polyfitter = Polyfitter()
polydrawer = Polydrawer()


def main():
    # video = 'harder_challenge_video'
    # video = 'challenge_video'
    video = 'project_video'
    white_output = '{}_done_2.mp4'.format(video)
    clip1 = VideoFileClip('{}.mp4'.format(video)).subclip(30, 51)
    white_clip = clip1.fl_image(process_image)  # NOTE: this function expects color images!!
    white_clip.write_videofile(white_output, audio=False)


def process_image(base):
    fig = plt.figure(figsize=(10, 8))
    i = 1

    undistorted = undistorter.undistort(base)
    misc.imsave('output_images/undistorted.jpg', undistorted)
    # i = show_image(fig, i, undistorted, 'Undistorted', 'gray')

    img = thresholder.threshold(undistorted)
    misc.imsave('output_images/thresholded.jpg', img)
    # i = show_image(fig, i, img, 'Thresholded', 'gray')

    img = warper.warp(img)
    misc.imsave('output_images/warped.jpg', img)
    # i = show_image(fig, i, img, 'Warped', 'gray')

    left_fit, right_fit = polyfitter.polyfit(img)

    img = polydrawer.draw(undistorted, left_fit, right_fit, warper.Minv)
    misc.imsave('output_images/final.jpg', img)
    # show_image(fig, i, img, 'Final')

    # plt.show()
    # plt.get_current_fig_manager().frame.Maximize(True)

    lane_curve, car_pos = polyfitter.measure_curvature(img)

    if car_pos > 0:
        car_pos_text = '{}m right of center'.format(car_pos)
    else:
        car_pos_text = '{}m left of center'.format(abs(car_pos))

    cv2.putText(img, "Lane curve: {}m".format(lane_curve.round()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                color=(255, 255, 255), thickness=2)
    cv2.putText(img, "Car is {}".format(car_pos_text), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 255, 255),
                thickness=2)

    # show_image(fig, i, img, 'Final')
    # plt.imshow(img)
    # plt.show()

    return img


def show_image(fig, i, img, title, cmap=None):
    a = fig.add_subplot(2, 2, i)
    plt.imshow(img, cmap)
    a.set_title(title)
    return i + 1


if __name__ == '__main__':
    main()
