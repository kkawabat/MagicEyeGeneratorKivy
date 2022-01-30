import os

from magic_eye_generator.sis_degenerator import degen_sis


def test_desis():
    sample_magic_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'doc', 'squirrel_magic_eye.png')
    result_depth_map_ = degen_sis(sample_magic_image_path)
    result_depth_map_.show()


if __name__ == '__main__':
    test_desis()

