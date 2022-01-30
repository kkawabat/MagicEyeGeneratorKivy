import cProfile
import os
import pstats

import numpy as np
import scipy
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from scipy.signal import peak_widths, find_peaks


def degen_sis(magic_image_path):
    magic_image = Image.open(magic_image_path)
    if hasattr(magic_image, "is_animated") and magic_image.is_animated:
        raise NotImplementedError('magic eye degenerator only works on static image atm')
        # sis_frames = []
        # for frame in range(0, magic_image.n_frames):
        #     print(f"processing frame {frame+1} of {magic_image.n_frames}")
        #     magic_image.seek(frame)
        #     sis_frame = degen_sis_single(magic_image)
        #     sis_frames.append(sis_frame)
        #
        # return sis_frames
    else:
        natural_image = degen_sis_single(magic_image)
        return natural_image


def degen_sis_single(magic_image):
    bw_magic_image = ImageOps.grayscale(magic_image)
    img_arr = np.asarray(bw_magic_image)

    depth_width = estimate_depth_width(img_arr)
    if depth_width is None:
        return Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'could_not_degenerate.png'))

    result_depth_map_arr = np.zeros(img_arr.shape)
    depth_range = np.linspace(0, 256, depth_width-1)
    for i, depth in enumerate(depth_range):
        print(i)
        img_arr_shifted = np.roll(img_arr, -i, axis=1)
        diff_zeros = (img_arr - img_arr_shifted) == 0
        result_depth_map_arr[diff_zeros] = depth

    return Image.fromarray(result_depth_map_arr.astype(np.uint8))


def estimate_depth_width(img_arr):
    shift_zero_count = []
    for i in range(img_arr.shape[1]):
        print(i)
        img_arr_shifted = np.roll(img_arr, -i, axis=1)
        diff_zeros = (img_arr - img_arr_shifted) == 0
        shift_zero_count.append(sum(sum(diff_zeros)))

    a = scipy.fft(shift_zero_count)
    b = scipy.fft(a)
    peaks, _ = find_peaks(b, height=b[0]*.10)
    # # for debugging
    # plt.plot(b)
    # plt.plot(peaks, b[peaks], "x")
    # plt.show()
    if len(peaks) == 0:
        return None
    else:
        return peaks[0]
