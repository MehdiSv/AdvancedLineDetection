from moviepy.video.io.VideoFileClip import VideoFileClip

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
    video = 'harder_challenge_video'
    white_output = '{}_done.mp4'.format(video)
    clip1 = VideoFileClip('{}.mp4'.format(video))  # .subclip(14, 16)
    white_clip = clip1.fl_image(process_image)  # NOTE: this function expects color images!!
    white_clip.write_videofile(white_output, audio=False)

    # images = glob.glob('test_images/test*.jpg')
    # images = ['test_images/test1.jpg']
    # images = ['test_images/straight_lines1.jpg']
    # for imname in images:
    #     print('Finding lanes for img {}'.format(imname))
    #     base = imread(imname)
    #     base = cv2.cvtColor(base, cv2.COLOR_BGR2RGB)
    #
    #     # plt.imshow(base)
    #     # plt.show()
    #
    #     img = process_image(base, polydrawer, polyfitter, thresholder, undistorter, warper)

def process_image(base):
    img = undistorter.undistort(base)
    # print('Undistorted')
    # plt.imshow(img, cmap='gray')
    # plt.show()
    img = thresholder.threshold(img)
    # print('Thresholded')
    # plt.imshow(img, cmap='gray')
    # plt.show()
    img = warper.warp(img)
    # print('Warped')
    # plt.imshow(img, cmap='gray')
    # plt.show()
    left_fit, right_fit = polyfitter.polyfit(img)
    img = polydrawer.draw(base, left_fit, right_fit, warper.Minv)
    return img


if __name__ == '__main__':
    main()
