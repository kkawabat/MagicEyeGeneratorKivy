import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import cProfile
import pstats


def gen_sis(depth_map_path, texture_map_path, depth_factor=.1, num_strips=10, texture_fixed_width=100):
    texture_map_im = Image.open(texture_map_path)
    depth_map_im = Image.open(depth_map_path).convert('L')

    texture_map_im, depth_map_im = resize_texture_n_depth_map(texture_map_im, depth_map_im, num_strips,
                                                              texture_fixed_width)
    texture_map_data = np.array(texture_map_im)
    depth_map_data = np.array(depth_map_im) / 255

    result_map = gen_depth_offset_map(texture_map_data, depth_map_data, num_strips, depth_factor)
    return result_map


def resize_texture_n_depth_map(texture_map_im, depth_map_im, num_strips, texture_fixed_width):
    texture_width, texture_height = texture_map_im.size
    texture_map_ratio = texture_height / texture_width
    texture_map_resized = texture_map_im.resize((texture_fixed_width,
                                                 int(texture_fixed_width * texture_map_ratio)))

    depth_map_width, depth_map_height = depth_map_im.size
    depth_map_ratio = depth_map_height / depth_map_width
    depth_map_resized = depth_map_im.resize((texture_fixed_width * num_strips,
                                             int(texture_fixed_width * num_strips * depth_map_ratio)),
                                            resample=Image.BOX)
    return texture_map_resized, depth_map_resized


def gen_depth_offset_map(texture_map_data, depth_map_data, num_strips, depth_factor):
    if len(texture_map_data.shape) == 2:
        texture_channels = 1
    elif len(texture_map_data.shape) == 3:
        texture_channels = texture_map_data.shape[2]
    else:
        raise ValueError("expected at most 3 dimension for texture_map (width, height, #channel)")

    texture_height, texture_width = texture_map_data.shape[0:2]
    depth_map_height, depth_map_width = depth_map_data.shape[0:2]
    depth_normed = (depth_map_data * depth_factor * texture_width).astype(int)
    tile_range_x = np.tile(range(texture_width), (depth_map_height, 1))

    tile_range_y = np.tile(range(texture_height),
                           (texture_width, int(depth_map_height / texture_height) + 1)).T[:depth_map_height, :]

    result_map = np.empty((depth_map_height, texture_width * (num_strips + 1), texture_channels))
    tile_range_x_tmp = np.tile(range(result_map.shape[1]), (depth_map_height, 1))
    tmp = np.empty((depth_map_height, texture_width * (num_strips + 1)))
    result_map[:, :texture_width, :] = texture_map_data[tile_range_y, tile_range_x, :]

    row_idc = np.arange(result_map.shape[0])

    for i in range(depth_map_width):
        result_map[row_idc, i + texture_width, :] = result_map[row_idc, i + depth_normed[:, i], :].reshape(-1,
                                                                                                           texture_channels)
        tmp[row_idc, i + texture_width] = tile_range_x_tmp[row_idc, i + depth_normed[:, i]]
    return result_map


def test():
    texture_map_path_ = r"C:\Users\kkawa\PycharmProjects\pythonarcade\codejam\data\texture\flower.PNG"
    depth_map_path_ = r"C:\Users\kkawa\PycharmProjects\pythonarcade\codejam\data\depth_map\squirrel.png"

    depth_factor_ = .05
    num_strips_ = 10

    result_map_ = gen_sis(depth_map_path_, texture_map_path_, depth_factor_, num_strips_)
    result_img = Image.fromarray(result_map_.astype(np.uint8), mode="RGBA")
    result_img.show()
    result_img.save(r"C:\Users\kkawa\PycharmProjects\pythonarcade\codejam\data\result\Capture2.PNG")


def main():
    profile = cProfile.Profile()
    profile.runcall(test)
    ps = pstats.Stats(profile)
    ps.sort_stats('cumtime')
    ps.print_stats()


if __name__ == '__main__':
    main()
