import cProfile
import os
import pstats
from PIL import Image
import numpy as np

from magic_eye_generator.sis_generator import gen_sis


def test_sis():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    texture_map_path_ = os.path.join(data_dir, 'texture', 'flower.PNG')
    depth_map_path_ = os.path.join(data_dir, 'depth_map', 'squirrel.png')
    depth_factor_ = .05
    num_strips_ = 10

    result_map_ = gen_sis(depth_map_path_, texture_map_path_, depth_factor_, num_strips_)
    result_img = Image.fromarray(result_map_.astype(np.uint8), mode="RGBA")
    result_img.show()


def profile_sis():
    profile = cProfile.Profile()
    profile.runcall(test_sis)
    ps = pstats.Stats(profile)
    ps.sort_stats('cumtime')
    ps.print_stats()


if __name__ == '__main__':
    test_sis()
    # profile_sis()
