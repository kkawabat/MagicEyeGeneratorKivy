import os

from magic_eye_generator.sis_degenerator import degen_sis


def test_desis():
    sample_magic_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'doc', 'squirrel_magic_eye.png')
    result_depth_map_ = degen_sis(sample_magic_image_path)
    result_depth_map_.show()


def test_desis2():
    sample_magic_image_path = r'C:\Users\kkawa\PycharmProjects\magic_eye_generator\data\depth_map\aiga-eod-magiceye1.jpg'
    result_depth_map_ = degen_sis(sample_magic_image_path)
    result_depth_map_.show()


if __name__ == '__main__':
    test_desis2()
    # test_desis()

