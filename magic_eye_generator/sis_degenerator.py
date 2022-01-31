import os

import numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import convolve


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
        return Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'could_not_degenerate.png'))

    result_depth_map_arr = np.zeros(img_arr.shape)
    depth_range = np.linspace(0, 256, depth_width-1)
    for shift_idx, diff_zeros_smoothed in get_depth_zeros(range(depth_width-1), img_arr):
        result_depth_map_arr[diff_zeros_smoothed] = depth_range[shift_idx]

    return Image.fromarray(result_depth_map_arr.astype(np.uint8))


def estimate_depth_width(img_arr):
    shift_zero_count = []

    for shift_idx, diff_zeros_smoothed in get_depth_zeros(range(img_arr.shape[1]), img_arr):
        shift_zero_count.append(sum(sum(diff_zeros_smoothed)))

    r, lag = autocorr(np.array(shift_zero_count))

    # # for debugging
    # import matplotlib.pyplot as plt
    # plt.plot(b)
    # plt.plot(peaks, b[peaks], "x")
    # plt.show()

    if r < 0.5:
        return None
    else:
        return lag


def get_depth_zeros(depth_range, img_arr):
    weights = np.array([[1, 1, 1],
                        [1, 2, 1],
                        [1, 1, 1]], dtype=np.float)
    weights = weights / np.sum(weights[:])

    for shift_idx, depth in enumerate(depth_range):
        print(shift_idx)
        diff_zeros = (img_arr - np.roll(img_arr, -shift_idx, axis=1)) == 0
        diff_zeros_smoothed = convolve(diff_zeros, weights, mode='constant')
        yield shift_idx, diff_zeros_smoothed


def autocorr(x):
    n = x.size
    norm = (x - np.mean(x))
    result = np.correlate(norm, norm, mode='same')
    acorr = result[n//2 + 1:] / (x.var() * np.arange(n-1, n//2, -1))
    lag = np.abs(acorr).argmax() + 1
    r = acorr[lag-1]
    if np.abs(r) > 0.5:
      print('Appears to be autocorrelated with r = {}, lag = {}'. format(r, lag))
    else:
      print('Appears to be not autocorrelated')
    return r, lag